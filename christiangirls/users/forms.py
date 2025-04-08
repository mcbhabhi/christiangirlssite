from flask_wtf import  FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from christiangirls.models import User


class Baptism(FlaskForm):
    username = StringField('Author', 
                           validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired()])
    password = PasswordField('Favourite christ moment', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm favourite christ moment', 
                             validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Convert!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Author already baptised!')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Author already baptised!')
    

    
class EdenGarden(FlaskForm):
    username = StringField('Author', 
                           validators = [DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Favourite christ moment', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Walk')


class UpdateAuthor(FlaskForm):
    username = StringField('Author', 
                           validators = [DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    email = StringField('Email', validators = [DataRequired()])
    update = SubmitField('Update')

    def validate_username(self, username):
            if username.data != current_user.username:
                user = User.query.filter_by(username=username.data).first()
                if user:
                     raise ValidationError('Author already baptised!')
                
    def validate_email(self, email):
            if email.data != current_user.email:
                user = User.query.filter_by(username=email.data).first()
                if user:
                     raise ValidationError('Email already baptised!')
                

class RequestResetForm(FlaskForm):
     email =  StringField('Email', validators=[DataRequired(), Email()])
     submit = SubmitField('Request Password Reset')
     
     def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None: 
                    raise ValidationError('Email not baptised! Become the son of christ first')
                

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Favourite christ moment', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm favourite christ moment', 
                             validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')