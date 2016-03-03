from flask.ext.wtf import Form
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired
from .models import User

class LoginForm(Form):

    userID = TextField("Nickname",  [validators.Required("Please enter a nickname.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
          return False
         
        user = User.query.filter_by(userID = self.userID.data).first()

        if user and user.check_password(self.password.data):
          login_user(user, True)
          return True
        else:
          self.userID.errors.append("Invalid user ID or password")
          return False

class RegistrationForm(Form):
    userID = StringField('Nickname', [validators.Required("Please enter a nickname.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."),
                                 validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [
        validators.Required("Please enter a password."),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField("Create account")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
          return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
          self.email.errors.append("That email is already taken")
          return False
        else:
          return True
