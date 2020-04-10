from logging import getLogger

from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from observatory.forms.extra.widgets import SubmitButtonInput
from observatory.models.user import User

LOG = getLogger(__name__)


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()],
        description='The name',
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        description='The secret',
    )
    remember = BooleanField(
        'Remember',
        description='Set cookie',
    )
    submit = SubmitField(
        'Login',
        description='Submit',
        widget=SubmitButtonInput(icon='user_enter'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        if not super().validate():
            return False

        self.user = User.by_username(self.username.data)
        if not self.user:
            self.username.errors.append('Username unknown...')
            self.password.errors.append('...or wrong password!')
            return False

        if not self.user.check_password(self.password.data):
            self.username.errors.append('Username unknown...')
            self.password.errors.append('...or wrong password!')
            return False

        if not self.user.is_active:
            self.username.errors.append('Username is blocked...')
            self.password.errors.append('...but the password is correct!')
            return False

        return True

    def action(self):
        if self.validate():

            LOG.info('login for user "%s"', self.user.username)
            if login_user(self.user, remember=self.remember.data):
                return self.user.refresh()

        return None
