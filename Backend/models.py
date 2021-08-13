from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from marshmallow_sqlalchemy import ModelSchema
import uuid 
from flask import session, redirect, url_for

from Backend import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
    try:
        if session['account_type'] == 'Admin':
            return Admin.query.get(int(user_id))
        elif session['account_type'] == 'Lecturer':
            return Lecturer.query.get(int(user_id))
        else:
            student = Student.query.filter_by(email=user_id).first()
            return Student.query.get(student.id)
        
    except:
        session.pop('account_type', None)
        return redirect(url_for('student.loginPortal'))
'''
      
      
@login_manager.user_loader
def load_user(user_id):
    student = Student.query.filter_by(email=user_id).first()
    return Student.query.get(student.id)
'''
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portal_toggle = db.Column(db.Boolean, default=False)
 
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100),unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(160), nullable=False)

    @staticmethod
    def generate_fake(count=100, **kwargs):
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker

        fake = Faker()
        for i in range(count):
            u = Admin(
                unique_id= str(uuid.uuid4()),
                name=fake.name(),
                email=fake.email(),
                position="CEO",
                gender="male",
                password = fake.password(),
                **kwargs)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
               

class Art(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculties = db.relationship('Faculty', backref='artfaculty', lazy=True)
    
class Sciences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculties = db.relationship('Faculty', backref='sciencefaculty', lazy=True)

class Socialsciences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculties = db.relationship('Faculty', backref='ssciencefaculty', lazy=True)
    
class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    sciences_id = db.Column(db.Integer, db.ForeignKey('sciences.id'))
    socialsciences_id = db.Column(db.Integer, db.ForeignKey('socialsciences.id'))
    name = db.Column(db.String(100), nullable=False)
    departments = db.relationship('Department', backref='child', lazy=True)



class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    total_levels = db.Column(db.Integer, default=0)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    courses = db.relationship('Courses', backref='subject', lazy=True)
    lecturer = db.relationship('Lecturer', backref='prof', lazy=True)



class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100),unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    passport = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    state_of_origin = db.Column(db.String(100), nullable=False)
    local_government = db.Column(db.String(100), nullable=False)
    hometown = db.Column(db.String(100), nullable=False)
    address1 = db.Column(db.String(200), nullable=False)
    address2 = db.Column(db.String(200))
    marital_status = db.Column(db.String(20), nullable=False)
    religion = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    school_email = db.Column(db.String(120))
    password = db.Column(db.String(160), nullable=False)
    registration_number = db.Column(db.String(20), nullable=False)
    matriculation_number = db.Column(db.String(20))
    faculty = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    admission_year = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    programme_type = db.Column(db.String(20), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    on_campus = db.Column(db.Boolean, default=False)
    off_campus = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    student_payment = db.relationship('Financial', backref='payment', lazy=True)
    student_registered = db.relationship('Registered', backref='pick', lazy=True)
    logged_in = db.Column(db.Integer, default=0)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id, 'user_email': self.email}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            student_id = s.loads(token)['user_id']
        except:
            return None
        return Student.query.get(user_id)
    
    def is_active(self):
        """True, as all users are active."""
        return True
        
        
    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email


    def __repr__(self):
        return f"User('{self.company_name}','{self.email}'),'{self.confirmed}')"

class Lecturer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    phone_no = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    school_email = db.Column(db.String(120))
    password = db.Column(db.String(160), nullable=False)
    faculty = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    course_handled = db.Column(db.JSON)
    course_adviser = db.Column(db.Boolean,  default=False)
    is_verified = db.Column(db.Boolean, default=False)
    one = db.Column(db.Boolean,  default=False)
    two = db.Column(db.Boolean,  default=False)
    three = db.Column(db.Boolean,  default=False)
    four = db.Column(db.Boolean,  default=False)
    five = db.Column(db.Boolean,  default=False)
    six = db.Column(db.Boolean,  default=False)
    seven = db.Column(db.Boolean,  default=False)
    logged_in = db.Column(db.Integer, default=0)
    cv = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    course = db.relationship('Courses', backref='exam', lazy=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'))
    sciences_id = db.Column(db.Integer, db.ForeignKey('sciences.id'))
    socialsciences_id = db.Column(db.Integer, db.ForeignKey('socialsciences.id'))
    art_id = db.Column(db.Integer, db.ForeignKey('art.id'))
    level = db.Column(db.Integer, default=0)
    semester = db.Column(db.Integer, default=0)
    course_registered = db.relationship('Registered', backref='picked', lazy=True)
    
    
class Registered(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    register = db.Column(db.Boolean, default=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)




class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100))
    semester = db.Column(db.Integer, default=0)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)


class Financial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_status = db.Column(db.Boolean, default=False)
    fees_history = db.Column(db.String(100), nullable=False)
    outstanding_fees = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    from_ = db.Column(db.String(100), nullable=False)
    to_ = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)



class LecturerMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(1000), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)



class StudentSchema(ModelSchema):
    class Meta:
        model = Student

class LecturerSchema(ModelSchema):
    class Meta:
        model = Lecturer


class FinancialSchema(ModelSchema):
    class Meta:
        model = Financial