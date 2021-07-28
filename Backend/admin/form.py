from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, StringField, PasswordField, SubmitField, BooleanField, DateField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class StudentRegistrationForm(FlaskForm):    
    name = StringField('Name',
                           validators=[DataRequired()])
    matricNo = StringField('Matriculation Number',
                           validators=[DataRequired()])
    date_of_birth = StringField('Date Of Birth',
                           validators=[DataRequired()])
    gender = StringField('Gender',
                           validators=[DataRequired()])
    nationality = StringField('Nationality',
                           validators=[DataRequired()])
    state_of_origin = StringField('State Of Origin',
                           validators=[DataRequired()])
    local_government = StringField('Local Government',
                           validators=[DataRequired()])
    hometown = StringField('Hometown',
                           validators=[DataRequired()])
                           
    address1 = StringField('Address',
                           validators=[DataRequired()])
    address2 = StringField('Matriculation Number',
                           validators=[DataRequired()])
    marital_status = StringField('Marital Status',
                           validators=[DataRequired()])
    religion = StringField('Religion',
                           validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',
                           validators=[DataRequired()])
    registration_number = StringField('Registration Number',
                           validators=[DataRequired()])
    faculty = StringField('Faculty',
                           validators=[DataRequired()])
    department = StringField('Department',
                           validators=[DataRequired()])
    
    admission_year = IntegerField('Admission Year',
                           validators=[DataRequired()])
    programme_type = StringField('Programme Type',
                           validators=[DataRequired()])

    degree = StringField('Degree',
                           validators=[DataRequired()])

    email = StringField('Email',
                        validators=[DataRequired(), Email('Invalid Email')])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Portal For Student?')

class StudentEditForm(FlaskForm):    
    name = StringField('Name')
    matricNo = StringField('Matriculation Number')
    date_of_birth = StringField('Date Of Birth')
    gender = StringField('Gender')
    nationality = StringField('Nationality')
    state_of_origin = StringField('State Of Origin')
    local_government = StringField('Local Government')
    hometown = StringField('Hometown')     
    address1 = StringField('Address')
    address2 = StringField('Matriculation Number')
    marital_status = StringField('Marital Status')
    religion = StringField('Religion')
    phone_number = IntegerField('Phone Number')
    registration_number = StringField('Registration Number')
    faculty = StringField('Faculty')
    department = StringField('Department')
    
    admission_year = IntegerField('Admission Year')
    programme_type = StringField('Programme Type')

    degree = StringField('Degree')

    email = StringField('Email')

    password = PasswordField('Password',)

    confirm_password = PasswordField('Confirm password')
    submit = SubmitField('Change Details?')


class LecturerRegistrationForm(FlaskForm):    
    name = StringField('Name',
                           validators=[DataRequired()])
    date_of_birth = StringField('Date Of Birth',
                           validators=[DataRequired()])
    gender = StringField('Gender',
                           validators=[DataRequired()])
                           
    address1 = StringField('Address',
                           validators=[DataRequired()])

    marital_status = StringField('Marital Status',
                           validators=[DataRequired()])

    phone_number = IntegerField('Phone Number',
                           validators=[DataRequired()])
    faculty = StringField('Faculty',
                           validators=[DataRequired()])
    department = StringField('Department',
                           validators=[DataRequired()])
                           
    
    courses = StringField('Course Handled',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email('Invalid Email')])

    password = PasswordField('Password',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register?')


class LoginAdminForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Change Password')


class MailForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    mail = TextAreaField('Mail',
                        validators=[DataRequired()])
    submit = SubmitField('Send')
    
class AddCourseForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired()])
    level = IntegerField('Level',
                        validators=[DataRequired()])
    faculty = StringField('Faculty',
                        validators=[DataRequired()])
    lecturer = StringField('Lecturer',
                        validators=[DataRequired()])
    semester = IntegerField('Semester',
                        validators=[DataRequired()])
    submit = SubmitField('Add')