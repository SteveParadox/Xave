import datetime
import jwt
import json
from flask import *
from flask_login import login_required, current_user, login_user, logout_user
from Backend import db, bcrypt
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required, check_confirmed
from Backend.models import *
from Backend.admin.form import *
from Backend.student.form import *
from Backend.admin.decorator import *

lecturer= Blueprint('lecturer', __name__)


@lecturer.route('/lecturer/login/portal', methods=['GET', 'POST'])
def lecturerloginPortal():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
    form = LoginLecturerForm()
    if form.validate_on_submit():
        lecturer = Lecturer.query.filter_by(email=form.email.data).first()
        if lecturer and bcrypt.check_password_hash(lecturer.password, form.password.data):
            login_user(lecturer, remember=form.remember.data)
            next_page = request.args.get('next')
            session['account_type'] = 'Lecturer'
            return redirect(next_page) if next_page else redirect(url_for('lecturer.lecturerdashboard'))
            
        else:
            pass
    else:
        redirect(url_for('student.loginPortal'))
    return render_template('lecturerlogin.html', title="Login to Portal", form=form)


@lecturer.route('/logout/lecturer')
@login_required
@lectureR
def logoutLecturer():
    logout_user()
    session.pop('account_type', None)
    return redirect(url_for('lecturer.lecturerloginPortal'))

  
@lecturer.route('/lecturer/data/<string:unique_id>', methods=['GET'])
@login_required
@lectureR
def lecturerData(unique_id):
    datalist= []
    lect = Lecturer.query.filter_by(unique_id=unique_id).first()
    return render_template('', lect=lect)


@lecturer.route('/lecturer/mail')
@login_required
@lectureR
def lecturerMail():
    message = LecturerMessage.query.all()
    return render_template('lecturermessage.html', message=message)


@lecturer.route('/lecturer/dashboard')
@login_required
@lectureR
def lecturerdashboard():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    return render_template('lecturerDashboard.html')


@lecturer.route('/leturer/student/message', methods=['GET','POST'])
@login_required
@lectureR
def bulkStudentMail():
    dept =Department.query.filter_by(name=current_user.department).first()
    form = MailForm()
    if form.validate_on_submit():
        message = Message()
        message.title = form.title.data
        message.mail = form.mail.data
        message.from_ = current_user.name
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('admin.AdminDashboard'))

    return render_template('stulect.html', form=form)
    

@lecturer.route('/leturer/message/<int:msg_id>', methods=['GET','POST'])
@login_required
@lectureR
def messageDetail(msg_id):
    msg = LecturerMessage.query.filter_by(id=msg_id).first()

    return render_template('msgDetail.html', msg=msg)


@lecturer.route('/lecturer/course')
@login_required
@lectureR
def courseHandled():
    lecturer = Lecturer.query.filter_by(id=current_user.id).first()
    dept= Department.query.filter_by(id=current_user.department_id).first()
    course1=''
    course2=''
    course3=''
    course4=''
    course5=''
    course6=''
    course7=''
    if current_user.one == True:
        course1= Courses.query.filter_by(department_id= dept.id).filter_by(level=1).all()
    if current_user.two == True:
        course2= Courses.query.filter_by(department_id= dept.id).filter_by(level=2).all()
    if current_user.three == True:
        course3= Courses.query.filter_by(department_id= dept.id).filter_by(level=3).all()
    if current_user.four == True:
        course4= Courses.query.filter_by(department_id= dept.id).filter_by(level=4).all()
    if current_user.five == True:
        course5= Courses.query.filter_by(department_id= dept.id).filter_by(level=5).all()
    if current_user.six == True:
        course6= Courses.query.filter_by(department_id= dept.id).filter_by(level=6).all()
    if current_user.seven == True:
        course7= Courses.query.filter_by(department_id= dept.id).filter_by(level=7).all()
  
    return render_template('courseHandled.html', course1=course1, course2=course2, course3=course3, course4=course4, course5=course5, course6=course6, course7=course7 )
    

@lecturer.route('/lecturer/level')
@login_required
@lectureR
def levelHandled():
    lecturer = Lecturer.query.filter_by(id=current_user.id).first()
    
    return render_template('levelHandled.html', lecturer=lecturer)
        
@lecturer.route('/lecturer/department')
@login_required
@lectureR
def departmentHandled():
    dept= Department.query.filter_by(id=current_user.department_id).all()
    
    #student= Student.query.filter_by(department=dept.name).filter_by(level=form.level.data).all()
    return render_template('departmentHandled.html', dept=dept, g=g)
    
    
@lecturer.route('/student/<string:dept>',methods=['GET','POST'])
@login_required
@lectureR
def getStudent(dept):
    form = LevelForm()
    student=""
    if form.validate_on_submit():
        formlevel = form.levels.data
        dept= Department.query.filter_by(name=dept).first()
       
        if formlevel =="one":
            student= Student.query.filter_by(department=dept.name).filter_by(level=1).all()
           
        if formlevel =="two":
            student= Student.query.filter_by(department=dept.name).filter_by(level=2).all()
        if formlevel =="three":
            student= Student.query.filter_by(department=dept.name).filter_by(level=3).all()
        if formlevel =="four":
            student= Student.query.filter_by(department=dept.name).filter_by(level=4).all()
        if formlevel =="five":
            student= Student.query.filter_by(department=dept.name).filter_by(level=5).all()
        if formlevel =="six":
            student= Student.query.filter_by(department=dept.name).filter_by(level=6).all()
        if formlevel =="seven":
            student= Student.query.filter_by(department=dept.name).filter_by(level=7).all()
        
    return render_template("getDept.html", student=student, form=form)


  
@lecturer.route('/student/<string:level>',methods=['GET','POST'])
@login_required
@lectureR
def getLevel(level):
    dept= Department.query.filter_by(name=current_user.department).first()
    
    student= Student.query.filter_by(department=dept.name).filter_by(level=1).all()
    return render_template("getDept.html", student=student)


    
    
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, IntegerField, StringField, RadioField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class UploadResultForm(FlaskForm):
    semester = RadioField('Semester', choices= [("one","First Semester"),("Two", 'Second Semester')])
    grade = IntegerField('Grade')
    submit = SubmitField('Send Result')

 
@lecturer.route('/upload/result/<string:student>/<string:dept>', methods=['GET', 'POST'])
@login_required
@lectureR
def uploadResult(student, dept):
    
    form=UploadResultForm()
    student = Student.query.filter_by(name=student).first()
    dept= Department.query.filter_by(name=dept).first()
    courses = Courses.query.filter_by(level=student.level).filter_by(subject=dept).all()
    
    if form.validate_on_submit():
        for i in courses:
            upload = Result(student_id=student.id)
            upload.grade = form.grade.data
            upload.course = "Mathematics"
            upload.semester = form.semester.data
            db.session.add(upload)
            db.session.commit()
        return redirect(url_for('lecturer.uploadResult', student=student.name, dept= dept.name))
    return render_template('uploadResult.html', student=student, dept=dept, form=form, courses=courses)