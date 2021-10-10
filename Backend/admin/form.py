from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, StringField, PasswordField, SubmitField,RadioField, BooleanField, DateField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileAllowed
from wtforms import FileField


class StudentRegistrationForm(FlaskForm):    
    name = StringField('Name',
                           validators=[DataRequired()])
    matricNo = StringField('Matriculation Number')
    date_of_birth = StringField('Date Of Birth',
                           validators=[DataRequired()])
    gender = SelectField('Gender', choices= [("Male","Male"),("Female", 'Female'),("None", "Can't Say")], validators=[DataRequired()])

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
    photo = FileField('profile', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    address2 = StringField('Matriculation Number',
                           validators=[DataRequired()])
    marital_status = SelectField('Marital Status', choices= [("Single","Single"),("Married", 'Married'), ("Complicated", "Its Complicated")], validators=[DataRequired()])

    religion = SelectField('Religion ', choices= [("Christianity","Christianity"),("Muslim", 'Musilm'), ("Others", "Others")], validators=[DataRequired()])

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
    programme_type = SelectField('Programme Type', choices= [("regular","Regular"),("part-time", 'Part-Time')], validators=[DataRequired()])


    degree = SelectField('Degree', choices= [("Bachelor's Degree","Bachelor"),("Masters", 'Masters'), ("PhD", "PhD")], validators=[DataRequired()])

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
    gender = SelectField('Gender', choices= [("male","Male"),("female", 'Female'),("none", "Can't Say")])
    nationality = StringField('Nationality')
    state_of_origin = StringField('State Of Origin')
    local_government = StringField('Local Government')
    hometown = StringField('Hometown')     
    address1 = StringField('Address')
    address2 = StringField('Matriculation Number')
    marital_status = SelectField('Marital Status', choices= [("Single","Single"),("Married", 'Married'), ("Complicated", "Its Complicated")])
    religion = SelectField('Religion ', choices= [("Christianity","Christianity"),("Muslim", 'Muslim'), ("Others", "Others")])
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
    gender = SelectField('Gender', choices= [("Male","Male"),("Female", 'Female'),("None", "Can't Say")], validators=[DataRequired()])

                           
    address1 = StringField('Address',
                           validators=[DataRequired()])

    marital_status = SelectField('Marital Status', choices= [("Single","Single"),("Married", 'Married'), ("Complicated", "Its Complicated")], validators=[DataRequired()])

    nationality = StringField('Nationality',
                           validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',
                           validators=[DataRequired()])
    faculty = StringField('Faculty',
                           validators=[DataRequired()])
    department = StringField('Department',
                           validators=[DataRequired()])
                           
    course_adviser = BooleanField('Adviser')                       
    photo = FileField('profile', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    document = FileField('Document', validators=[FileAllowed(['pdf', 'txt', 'docx'])])
    email = StringField('Email',
                        validators=[DataRequired(), Email('Invalid Email')])
    level = StringField('Level',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    
    position = StringField('Position',
                             validators=[DataRequired()])
    one = BooleanField('One')
    two = BooleanField('Two')
    three = BooleanField('Three')
    four = BooleanField('Four')
    five = BooleanField('Five')
    six = BooleanField('Six')
    seven = BooleanField('Seven')
    confirm_password = PasswordField('Confirm password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register?')

class AddAdminForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])            
    gender = SelectField('Gender', choices= [("Male","Male"),("Female", 'Female'),("None", "Can't Say")], validators=[DataRequired()])
    position = StringField('Position',
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
    remember = BooleanField('Remeber Me')
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
    faculty = StringField('Faculty',
                        validators=[DataRequired()])
                        
    department = StringField('Department')
    lecturer = StringField('Lecturer')
    semester = RadioField('Semester', choices= [("one","First Semester"),("Two", 'Second Semester')],
                        validators=[DataRequired()])
    levels = RadioField('Level', choices= [("one","Level One"),("two", 'Level Two'),("three", "Level Three"),("four", "Level Four"),("five", "Level Five"),("six", "Level Six"),("seven", "Level Seven")],
                        validators=[DataRequired()])
    submit = SubmitField('Add')
    


class LevelForm(FlaskForm):
    levels = RadioField('Level', choices= [("one","Level One"),("Two", 'Level Two'),("three", "Level Three"),("four", "Level Four"),("five", "Level Five"),("six", "Level Six"),("seven", "Level Seven")],
                        validators=[DataRequired()])
   
    submit = SubmitField('View')
    
    
class SemesterForm(FlaskForm):
    semester =  SelectField('Semester', choices= [(1,"First Semester"),(2, 'Second Semester')])
    week = SelectField('Semester', choices= [   (1, "1"),
                                                (2, '2'),
                                                (3, '3'),
                                                (4, '4'),
                                                (5, '5'),
                                                (6, '6'),
                                                (7, '7'),
                                                (8, '8'),
                                                (9, '9'),
                                                (10, '10'),
                                                (11, '11'),
                                                (12, '12'),
                                                (13, '13'),
                                                (14, '14'),
                                                (15, '15'),
                                                (16, '16'),
                                                (17, '17'),
                                                (18, '18'),
                                                (19, '19'),
                                                (20, '20'),
                                                (21, "21"),
                                                (22, '22'),
                                                (23, '23'),
                                                (24, '24'),
                                                (25, '25'),
                                                (26, '26'),
                                                (27, '27'),
                                                (28, '28'),
                                                (29, '29'),
                                                (30, '30'),
                                                (31, '31'),
                                                (32, '32'),
                                                (33, '33'),
                                                (34, '34'),
                                                (35, '35'),
                                                (36, '36'),
                                                (37, '37'),
                                                (38, '38'),
                                                (39, '39'),
                                                (40, '40'),
    
    
                                        ])
                        
    submit = SubmitField('Update')