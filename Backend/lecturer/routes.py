import datetime
import jwt
import json
from flask import *
from flask_login import login_required, current_user
from Backend import db, bcrypt
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required, check_confirmed
from Backend.models import *
from Backend.admin.form import *

lecturer= Blueprint('lecturer', __name__)


@lecturer.route('/lecturer/login/portal', methods=['GET', 'POST'])
def lecturerloginPortal():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).filter_by(matriculation_number=form.matriculation_number.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('student.myProfile'))
        else:
            pass
        if not student:
            lecturer = Lecturer.query.filter_by(email=form.email.data).first()
            if lecturer and bcrypt.check_password_hash(lecturer.password, form.password.data):
                login_user(lecturer, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for(''))
            else:
                pass
        else:
            redirect(url_for('student.loginPortal'))
    return render_template('login.html', title="Login to Portal", form=form)

  
@lecturer.route('/lecturer/data/<string:unique_id>', methods=['GET'])
@login_required
@check_confirmed
def lecturerData(unique_id):
    datalist= []
    lect = Lecturer.query.filter_by(unique_id=unique_id).first()
    return render_template('', lect=lect)


@lecturer.route('/lecturer/mail')
@login_required
#@check_confirmed
def lecturerMail():
    message = LecturerMessage.query.all()
    return render_template('message.html', message=message)


@lecturer.route('/lecturer/dashboard')
@login_required
#@check_confirmed
def lecturerdashboard():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    return render_template('lecturerDashboard.html')
    

@lecturer.route('/leturer/student/message', methods=['GET','POST'])
def bulkStudentMail():
    form = MailForm()
    if form.validate_on_submit():
        message = Message()
        message.title = form.title.data
        message.mail = form.mail.data
        message.from_ = 'lecturer'
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('admin.AdminDashboard'))

    return render_template('stulect.html', form=form)


@lecturer.route('/lecturer/course')
def courseHandled():
    g=[]
    lecturer = Lecturer.query.filter_by(id=current_user.id).first()
    course= Courses.query.filter_by(exam=lecturer).all()
    for i in course:
        g.append(i.name)
    tuple(g)
    print (g)
    return render_template('courseHandled.html', course=course, g=g)
    

@lecturer.route('/lecturer/level')
def levelHandled():
    g=[]
    lecturer = Lecturer.query.filter_by(id=current_user.id).first()
    course= Courses.query.filter_by(exam=lecturer).all()
    for i in course:
        g.append(i)
    tuple(g)
    
    return render_template('levelHandled.html', course=course, g=g)
        
@lecturer.route('/lecturer/department')
def departmentHandled():
    #dept= Department.query.filter_by(id=current_user.department_id).all()
    # to change
    dept= Department.query.filter_by(id=current_user.id).all()
    #student= Student.query.filter_by(department=dept.name).filter_by(level=form.level.data).all()
    return render_template('departmentHandled.html', dept=dept, g=g)
    
    
@lecturer.route('/student/<string:dept>')
def getStudent(dept):
    dept= Department.query.filter_by(name=dept).first()
    student= Student.query.filter_by(department=dept.name).filter_by(level=1).all()
    return render_template("getDept.html", student=student)
    
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class UploadResultForm(FlaskForm):
    semester = StringField('Semester')
    grade = IntegerField('Grade')
    submit = SubmitField('Send Result')

 
@lecturer.route('/upload/result/<string:student>/<string:dept>', methods=['GET', 'POST'])
def uploadResult(student, dept):
    form=UploadResultForm()
    student = Student.query.filter_by(name=student).first()
    dept= Department.query.filter_by(name=dept).first()
    courses = Courses.query.filter_by(level=student.level).filter_by(subject=dept).all()
    if form.validate_on_submit():
        for i in courses:
            upload = Result(student_id=student.id)
            upload.grade = form.grade.data
            upload.course = i.name
            upload.semester = form.semester.data
            db.session.add(upload)
            db.session.commit()
        return redirect(url_for('lecturer.uploadResult', student=student.name, dept= dept.name))
    return render_template('uploadResult.html', student=student, dept=dept, form=form, courses=courses)