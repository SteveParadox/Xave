from flask import *
from flask_login import login_required
from Backend.models import *
from Backend import *
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required, check_confirmed

records = Blueprint('records', __name__)


@records.route('/registered/courses/<string:student_id>', methods=['GET'])
@login_required
@check_confirmed
def registeredCourses(student_id):
    detail = Student.query.filter_by(unique_id=unique_id).first()
    record = Records.query.filter_by(author=detail).first()
    return render_template('', record=record)

@records.route('/view/result/<string:student_id>', methods=['GET'])
@login_required 
@check_confirmed
def viewResult(student_id):
    detail = Student.query.filter_by(unique_id=unique_id).first()
    record = Records.query.filter_by(author=detail).first()
    return render_template('', record=record)


@records.route('/clear/db')
def clear():
    #db.drop_all(app=create_app())
    db.create_all(app=create_app())
    return redirect(url_for('student.home'))


@records.route('/faculty/add/science')
def facultyAddScience():
    faculty = Faculty()
    faculty.sciences_id= 1
    data = {"name":["SSLT","Sciences","Engineering", "Basic Medical Sciences"]}
    for i in data['name']:
        faculty.name=i
        db.session.add(faculty)
    db.session.commit()
    return redirect(url_for('student.home'))

@records.route('/faculty/add/socialscience')
def facultyAddSocialScience():
    faculty = Faculty()
    faculty.socialsciences_id= 1
    data = {"name":["Marketting","Management Sciences","Finance and Banking", "Accounting"]}
    for i in data['name']:
        faculty.name=i
        db.session.add(faculty)
    db.session.commit()
    return redirect(url_for('student.home'))

@records.route('/faculty/add/art')
def facultyAddArt():
    faculty = Faculty()
    faculty.art_id= 1
    data = {"name":["Law","Theatre Art","Linguistics and Communication studies", "Adult and non-formal Education"]}
    for i in data['name']:
        faculty.name=i
        db.session.add(faculty)
    db.session.commit()
    return redirect(url_for('student.home'))

@records.route('/dept/add/<string:name>')
def facultyAddname(name):
    faculty = Faculty()
    faculty.art_id= 1
    data = {"name":["Law","Theatre Art","Linguistics and Communication studies", "Adult and non-formal Education"]}
    for i in data['name']:
        faculty.name=i
        db.session.add(faculty)
    db.session.commit()
    return redirect(url_for('student.home'))