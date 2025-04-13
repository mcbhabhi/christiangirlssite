from flask_wtf import  FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class Create(FlaskForm):
     title = StringField('Title', validators=[DataRequired()])
     content = PageDownField('Content', validators=[DataRequired()], render_kw={"class": "custom-content-box"})
     image = FileField('Add Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
     submit = SubmitField('Create')