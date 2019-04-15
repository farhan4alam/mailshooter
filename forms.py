from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Length,Email
from wtforms.widgets import TextArea

class mailingform(FlaskForm):
    mail=StringField('Email-Id', validators=[ DataRequired(), Length(min=5,max=51), Email(message='Email is not valid!!')])
    password=PasswordField('Password', validators=[ DataRequired() ])
    subject=StringField('Subject', validators=[ DataRequired() ])
    content=StringField('Content', widget=TextArea(), validators= [ DataRequired() ])
    file=FileField('Upload Excel (.xls) file to Shoot Mails:', validators=[FileAllowed(['xlsx']), DataRequired()])
    submit=SubmitField('Send Mail')
