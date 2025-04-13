from flask_wtf import  FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Create(FlaskForm):
     title = StringField('Title', validators=[DataRequired()])
     content = PageDownField('Content', validators=[DataRequired()], render_kw={"rows": 10})
     bibliography = StringField('Bibliography')
     image = FileField('Add Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
     submit = SubmitField('Create')