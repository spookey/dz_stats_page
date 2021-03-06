from random import choice

from pytest import mark
from wtforms import DecimalField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional

from observatory.forms.space_edit import SpaceEditForm
from observatory.models.value import Value
from observatory.start.environment import SP_API_PREFIX


class PhonyForm(SpaceEditForm):
    KEYS = dict(
        string='test.string',
        number='test.number',
        cstory='test.cstory',
        sensor='test.sensor',
        wrong='checks for wrong access',
    )
    ONE_OF = ['string', 'cstory', 'this_checks_for_wrong_access']
    SENSORS = ['sensor']

    string = StringField('String')
    number = DecimalField(
        'Number',
        places=2,
        validators=[DataRequired(), NumberRange(min=0, max=1337)],
    )
    cstory = TextAreaField('Cool story, bro!')
    sensor = SelectField(
        'Sensor',
        coerce=int,
        validators=[Optional()],
    )


@mark.usefixtures('session', 'ctx_app')
class TestSpaceEditBase:
    @staticmethod
    def test_basic_fields():
        idx = choice(range(23, 42))
        form = PhonyForm(idx=idx)
        assert form.string is not None
        assert form.number is not None
        assert form.cstory is not None
        assert form.sensor is not None

        assert getattr(form, 'data', 'error') == dict(
            string=None, number=None, cstory=None, sensor=None
        )

    @staticmethod
    def test_form_idx():
        idx = choice(range(23, 42))
        form = PhonyForm(idx=idx)
        assert form.idx == idx

    @staticmethod
    def test_preloads_data(gen_sensor):
        idx = choice(range(23, 42))

        data = dict(
            string=Value.set(
                key=f'{SP_API_PREFIX}.test.string', idx=idx, elem='test'
            ).elem,
            number=Value.set(
                key=f'{SP_API_PREFIX}.test.number', idx=idx, elem=1234.5
            ).elem,
            cstory=Value.set(
                key=f'{SP_API_PREFIX}.test.cstory', idx=idx, elem='more text'
            ).elem,
            sensor=Value.set(
                key=f'{SP_API_PREFIX}.test.sensor', idx=idx, elem=gen_sensor()
            ).elem.prime,
        )

        form = PhonyForm(idx=idx)
        assert getattr(form, 'data', 'error') == data

    @staticmethod
    def test_validation_fails():
        form = PhonyForm(idx=42)
        assert form.validate() is False
        assert form.action() is None

        assert ''.join(form.string.errors) == ''
        assert 'required' in ''.join(form.number.errors).lower()
        assert ''.join(form.cstory.errors) == ''

    @staticmethod
    def test_one_of_fails():
        form = PhonyForm(idx=23, string=None, number=2, cstory=None)
        assert form.validate() is False
        assert form.action() is None

        assert 'at least' in ''.join(form.string.errors).lower()
        assert ''.join(form.number.errors).lower() == ''
        assert 'at least' in ''.join(form.cstory.errors).lower()

    @staticmethod
    def test_action_creates(gen_sensor):
        assert Value.query.all() == []

        idx, string, number, cstory, sensor = (
            choice(range(23, 42)),
            'text',
            2.5,
            'more test',
            gen_sensor(),
        )
        form = PhonyForm(
            idx=idx,
            string=string,
            number=number,
            cstory=cstory,
            sensor=sensor.prime,
        )

        assert form.validate() is True
        assert form.action()

        assert Value.get(key=f'{SP_API_PREFIX}.test.string', idx=idx) == string
        assert Value.get(key=f'{SP_API_PREFIX}.test.number', idx=idx) == number
        assert Value.get(key=f'{SP_API_PREFIX}.test.cstory', idx=idx) == cstory
        assert Value.get(key=f'{SP_API_PREFIX}.test.sensor', idx=idx) == sensor

    @staticmethod
    def test_action_changes(gen_sensor):
        idx, string, number, cstory, sensor = (
            choice(range(23, 42)),
            None,
            42.0,
            'new story',
            gen_sensor('new sensor'),
        )

        string_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.string', idx=idx, elem='old text'
        )
        number_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.number', idx=idx, elem=23.5
        )
        cstory_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.cstory', idx=idx, elem='good old story'
        )
        sensor_obj = Value.set(
            key=f'{SP_API_PREFIX}.test.sensor',
            idx=idx,
            elem=gen_sensor('old sensor'),
        )
        assert Value.query.all() == [
            string_obj,
            number_obj,
            cstory_obj,
            sensor_obj,
        ]

        form = PhonyForm(
            idx=idx,
            string=string,
            number=number,
            cstory=cstory,
            sensor=sensor.prime,
        )

        assert form.validate() is True
        assert form.action()

        assert Value.get(key=f'{SP_API_PREFIX}.test.string', idx=idx) == string
        assert Value.get(key=f'{SP_API_PREFIX}.test.number', idx=idx) == number
        assert Value.get(key=f'{SP_API_PREFIX}.test.cstory', idx=idx) == cstory
        assert Value.get(key=f'{SP_API_PREFIX}.test.sensor', idx=idx) == sensor
