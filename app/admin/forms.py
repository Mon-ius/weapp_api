from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l




# ...
# wtforms.fields.(default field arguments, choices=[], coerce=unicode, option_widget=None)


class LoginForm(FlaskForm):
    username = StringField(_l('Password'), validators=[DataRequired()])
    password = PasswordField(_l('UserName'), validators=[DataRequired()])
    remember_me = BooleanField(_l('FuckMe?'))
    submit = SubmitField(_l('Submit'))


