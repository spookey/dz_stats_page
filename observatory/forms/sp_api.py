from string import digits, hexdigits

from flask_wtf import FlaskForm
from iso_4217 import Currency
from pytz import common_timezones
from wtforms import (
    BooleanField,
    DecimalField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    URL,
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
)

from observatory.forms.extra.validators import NeedInner, NeedStart
from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.models.values import Values
from observatory.shared import SPACE_API
from observatory.start.environment import SP_API_PREFIX

# pylint: disable=arguments-differ
# pylint: disable=no-member


class SpaceForm(FlaskForm):
    KEYS = {}
    ANY_OF = {}

    def __init__(self, *args, idx=0, **kwargs):
        super().__init__(
            *args,
            data={
                field: Values.get(key=f'{SP_API_PREFIX}.{key}', idx=idx)
                for field, key in self.KEYS.items()
            },
            **kwargs,
        )
        self.idx = idx

    def validate(self):
        if not super().validate():
            return False

        fields = [
            field
            for field in [getattr(self, name, None) for name in self.ANY_OF]
            if field is not None
        ]
        if fields and any(
            field.data is None or not str(field.data).strip()
            for field in fields
        ):
            disp = '", "'.join(self.ANY_OF.values())
            for field in fields:
                field.errors.append(
                    f'Need at least one of the "{disp}" fields'
                )
            return False

        return True

    def action(self):
        if not self.validate():
            return None

        for form_key, space_key in self.KEYS.items():
            field = self._fields.get(form_key, None)
            if field is not None:
                value = field.data
                if isinstance(field, DecimalField):
                    value = float(value)
                if value is None or not str(value).strip():
                    value = None

                Values.set(
                    key=f'{SP_API_PREFIX}.{space_key}',
                    idx=self.idx,
                    value=value,
                )

        return SPACE_API.reset()


class SpaceInfoForm(SpaceForm):
    KEYS = dict(
        space='space',
        logo='logo',
        url='url',
    )
    space = StringField(
        'Space',
        validators=[DataRequired()],
        description='The name of your space',
    )
    logo = StringField(
        'Logo',
        validators=[DataRequired(), URL()],
        description='URL to your space logo',
    )
    url = StringField(
        'URL',
        validators=[DataRequired(), URL()],
        description='URL to your space website',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceLocationForm(SpaceForm):
    KEYS = dict(
        address='location.address',
        lat='location.lat',
        lon='location.lon',
        timezone_sel='location.timezone',
    )
    address = StringField(
        'Address',
        validators=[Optional()],
        description='The postal address of your space',
    )
    lat = DecimalField(
        'Latitude',
        default=0.0,
        places=6,
        validators=[DataRequired(), NumberRange(min=-90, max=90)],
        description=(
            'Latitude of your space location, in degree with decimal places'
        ),
    )
    lon = DecimalField(
        'Longitude',
        default=0.0,
        places=6,
        validators=[DataRequired(), NumberRange(min=-180, max=180)],
        description=(
            'Longitude of your space location, in degree with decimal places'
        ),
    )
    timezone_sel = SelectField(
        'Timezone',
        coerce=str,
        description='The timezone the space is located in',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    @staticmethod
    def _timezone_choices():
        return [(None, '—'), *[(ctz, ctz) for ctz in common_timezones]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.timezone_sel.choices = self._timezone_choices()


class SpaceSpaceFedForm(SpaceForm):
    KEYS = dict(
        spacenet='spacefed.spacenet',
        spacesaml='spacefed.spacesaml',
    )
    spacenet = BooleanField(
        'SpaceNET',
        default=False,
        description='SpaceNET support',
    )
    spacesaml = BooleanField(
        'SpaceSAML',
        default=False,
        description='SpaceSAML support',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceCamForm(SpaceForm):
    KEYS = dict(cam='cam')
    cam = StringField(
        'Webcam URL',
        validators=[DataRequired(), URL()],
        description='Webcam URLs in your space',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)


class SpaceContactForm(SpaceForm):
    KEYS = dict(
        phone='contact.phone',
        sip='contact.sip',
        irc='contact.irc',
        twitter='contact.twitter',
        mastodon='contact.mastodon',
        facebook='contact.facebook',
        identica='contact.identica',
        foursquare='contact.foursquare',
        email='contact.email',
        mailinglist='contact.ml',
        xmpp='contact.xmpp',
        issue_mail='contact.issue_mail',
        gopher='contact.gopher',
        matrix='contact.matrix',
        mumble='contact.mumble',
    )
    ANY_OF = dict(
        email='E-Mail',
        issue_mail='Issue Mail',
        twitter='Twitter',
        mailinglist='Mailinglist',
    )
    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            NeedStart('+'),
            NeedInner(f' +{digits}', only=True),
        ],
        description=(
            'Phone number, including country code with a leading plus sign'
        ),
    )
    sip = StringField(
        'SIP',
        validators=[Optional(), NeedStart('sip:'), NeedInner('@')],
        description='URI for Voice-over-IP via SIP',
    )
    irc = StringField(
        'IRC',
        validators=[Optional(), URL(), NeedStart('irc://'), NeedInner('#')],
        description='URL of the IRC channel',
    )
    twitter = StringField(
        'Twitter',
        validators=[Optional(), NeedStart('@')],
        description='Twitter handle, with leading @',
    )
    mastodon = StringField(
        'Mastodon',
        validators=[Optional(), NeedStart('@'), NeedInner('@')],
        description='Mastodon username',
    )
    facebook = StringField(
        'Facebook',
        validators=[Optional(), URL()],
        description='Facebook account URL',
    )
    identica = StringField(
        'Identica',
        validators=[Optional(), Email()],
        description='Identi.ca or StatusNet account',
    )
    foursquare = StringField(
        'Foursquare',
        validators=[
            Optional(),
            Length(min=24, max=24),
            NeedInner(hexdigits, only=True),
        ],
        description='Foursquare ID',
    )
    email = StringField(
        'E-Mail',
        validators=[Optional(), Email()],
        description='E-Mail address for contacting your space',
    )
    mailinglist = StringField(
        'Mailinglist',
        validators=[Optional(), Email()],
        description='The e-mail address of your mailing list',
    )
    xmpp = StringField(
        'XMPP',
        validators=[Optional(), Email()],
        description='A public Jabber/XMPP multi-user chatroom',
    )
    issue_mail = StringField(
        'Issue Mail',
        validators=[Optional(), Email()],
        description='A separate email address for issue reports',
    )
    gopher = StringField(
        'Gopher',
        validators=[Optional(), URL(), NeedStart('gopher://')],
        description=(
            'A URL to find information about the Space in the Gopherspace'
        ),
    )
    matrix = StringField(
        'Matrix',
        validators=[Optional(), NeedStart('#', '+'), NeedInner(':')],
        description='Matrix channel/community for the Hackerspace',
    )
    mumble = StringField(
        'Mumble',
        validators=[Optional(), URL(), NeedStart('mumble://')],
        description='URL to a Mumble server/channel',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )


class SpaceKeymastersForm(SpaceForm):
    KEYS = dict(
        name='contact.keymasters.name',
        irc_nick='contact.keymasters.irc_nick',
        phone='contact.keymasters.phone',
        email='contact.keymasters.email',
        twitter='contact.keymasters.twitter',
        xmpp='contact.keymasters.xmpp',
        mastodon='contact.keymasters.mastodon',
        matrix='contact.keymasters.matrix',
    )
    ANY_OF = dict(
        irc_nick='IRC Nick',
        phone='Phone',
        email='E-Mail',
        twitter='Twitter',
    )
    name = StringField(
        'Name',
        validators=[Optional()],
        description='Real name',
    )
    irc_nick = StringField(
        'IRC Nick',
        validators=[Optional()],
        description='Contact the person with this nickname directly in IRC',
    )
    phone = StringField(
        'Phone',
        validators=[
            Optional(),
            NeedStart('+'),
            NeedInner(f' +{digits}', only=True),
        ],
        description=(
            'Phone number, including country code with a leading plus sign'
        ),
    )
    email = StringField(
        'E-Mail',
        validators=[Optional(), Email()],
        description='E-Mail address',
    )
    twitter = StringField(
        'Twitter',
        validators=[Optional(), NeedStart('@')],
        description='Twitter handle, with leading @',
    )
    xmpp = StringField(
        'XMPP',
        validators=[Optional(), Email()],
        description='XMPP JID',
    )
    mastodon = StringField(
        'Mastodon',
        validators=[Optional(), NeedStart('@'), NeedInner('@')],
        description='Mastodon username',
    )
    matrix = StringField(
        'Matrix',
        validators=[Optional(), NeedStart('@'), NeedInner(':')],
        description='Matrix username',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)


class SpaceFeedForm(SpaceForm):
    KEYS = {}

    type_sel = SelectField(
        'Type',
        coerce=str,
        description='Type of the feed',
    )
    url = StringField(
        'URL', validators=[DataRequired(), URL()], description='Feed URL'
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    @staticmethod
    def _type_choices():
        return [
            (None, '—'),
            ('rss', 'RSS'),
            ('atom', 'Atom'),
            ('ical', 'iCal'),
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type_sel.choices = self._type_choices()


class SpaceFeedBlogForm(SpaceFeedForm):
    KEYS = dict(
        type_sel='feeds.blog.type',
        url='feeds.blog.url',
    )


class SpaceFeedWikiForm(SpaceFeedForm):
    KEYS = dict(
        type_sel='feeds.wiki.type',
        url='feeds.wiki.url',
    )


class SpaceFeedCalendarForm(SpaceFeedForm):
    KEYS = dict(
        type_sel='feeds.calendar.type',
        url='feeds.calendar.url',
    )


class SpaceFeedFlickrForm(SpaceFeedForm):
    KEYS = dict(
        type_sel='feeds.flickr.type',
        url='feeds.flickr.url',
    )


class SpaceProjectsForm(SpaceForm):
    KEYS = dict(projects='projects')
    projects = StringField(
        'Projects',
        validators=[DataRequired(), URL()],
        description='Your project sites',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)


class SpaceLinksForm(SpaceForm):
    KEYS = dict(
        name='links.name',
        description='links.description',
        url='links.url',
    )
    name = StringField(
        'Name',
        validators=[DataRequired()],
        description='The link name',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='A more detailed description of the link',
    )
    url = StringField(
        'URL',
        validators=[DataRequired(), URL()],
        description='The URL',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)


class SpaceMembershipPlansForm(SpaceForm):
    KEYS = dict(
        name='membership_plans.name',
        value='membership_plans.value',
        currency_sel='membership_plans.currency',
        billing_interval_sel='membership_plans.billing_interval',
        description='membership_plans.description',
    )
    name = StringField(
        'Name',
        validators=[DataRequired()],
        description='The name of the membership plan',
    )
    value = DecimalField(
        'Value',
        places=2,
        validators=[DataRequired(), NumberRange(min=0)],
        description='How much does this plan cost?',
    )
    currency_sel = SelectField(
        'Currency',
        coerce=str,
        description='What\'s the currency?',
    )
    billing_interval_sel = SelectField(
        'Billing interval',
        coerce=str,
        description='How often is the membership billed?',
    )
    description = TextAreaField(
        'Description',
        validators=[Optional()],
        description='A free form string',
    )
    submit = SubmitField(
        'Save',
        description='Submit',
        widget=SubmitButtonInput(icon='ops_submit'),
    )

    @staticmethod
    def _currency_choices():
        return [
            (curr.name, f'{curr.name} — {curr.full_name}') for curr in Currency
        ]

    @staticmethod
    def _billing_interval_choices():
        return [
            ('yearly', 'Yearly'),
            ('monthly', 'Monthly'),
            ('weekly', 'Weekly'),
            ('daily', 'Daily'),
            ('hourly', 'Hourly'),
            ('other', 'Other'),
        ]

    def __init__(self, idx, *args, **kwargs):
        super().__init__(*args, idx=idx, **kwargs)

        self.currency_sel.choices = self._currency_choices()
        self.billing_interval_sel.choices = self._billing_interval_choices()
