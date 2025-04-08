from flask_wtf import  FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class Create(FlaskForm):
     title = StringField('Title', validators=[DataRequired()])
     content = TextAreaField('Content', validators=[DataRequired()], render_kw={"rows": 10})
     bibliography = StringField('Bibliography')
     submit = SubmitField('Create')