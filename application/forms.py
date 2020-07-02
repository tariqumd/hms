from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email,Length,EqualTo, ValidationError

#from application.models import User

class Userfrom(FlaskForm):
    id= StringField('id', validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])

    submit=SubmitField('Login')



class Patient_Retr(FlaskForm):
    patient_id = StringField("Patient_id", validators=[DataRequired()])
    submit = SubmitField("submit")
