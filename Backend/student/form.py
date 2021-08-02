from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class StudentRegistrationForm(FlaskForm):    
    name = StringField('Matriculation Number',
                           validators=[DataRequired()])
    matricNo = StringField('Matriculation Number',
                           validators=[DataRequired()])
    date_of_birth = StringField('Matriculation Number',
                           validators=[DataRequired()])
    gender = StringField('Matriculation Number',
                           validators=[DataRequired()])
    nationality = StringField('Matriculation Number',
                           validators=[DataRequired()])
    state_of_origin = StringField('Matriculation Number',
                           validators=[DataRequired()])
    local_government = StringField('Matriculation Number',
                           validators=[DataRequired()])
    hometown = StringField('Matriculation Number',
                           validators=[DataRequired()])
                           
    address1 = StringField('Matriculation Number',
                           validators=[DataRequired()])
    address2 = StringField('Matriculation Number',
                           validators=[DataRequired()])
    marital_status = StringField('Matriculation Number',
                           validators=[DataRequired()])
    religion = StringField('Matriculation Number',
                           validators=[DataRequired()])
    phone_number = IntegerField('Matriculation Number',
                           validators=[DataRequired()])
    registration_number = StringField('Matriculation Number',
                           validators=[DataRequired()])
    faculty = StringField('Matriculation Number',
                           validators=[DataRequired()])
    department = StringField('Matriculation Number',
                           validators=[DataRequired()])
    
    addmission_year = IntegerField('Matriculation Number',
                           validators=[DataRequired()])
    programme_type = StringField('Matriculation Number',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email('Invalid Email')])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Portal For Student?')


class LoginForm(FlaskForm):
    matriculation_number = StringField('Matriculation Number',
                        validators=[DataRequired()])
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class LoginLecturerForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateDetailForm(FlaskForm):
    address1 = StringField('Address')
    marital_status = StringField('Marital Status')
    email = StringField('Email Address')
    phone_number = StringField('Phone Number')
    religion = StringField('Religion')
    submit = SubmitField('Update Info')


class RegisterCoursesForm(FlaskForm):
    registered = BooleanField()
    submit = SubmitField('Register Courses')