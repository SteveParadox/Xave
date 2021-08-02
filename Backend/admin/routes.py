from flask import *
from Backend.models import *
import uuid 
from Backend import db, bcrypt
from flask_login import login_required, current_user, login_user,logout_user, decode_cookie
from Backend.config import Config
from flask_cors import cross_origin
from Backend.ext import token_required
from Backend.utils import save_img
from Backend.admin.form import *
from Backend.admin.decorator import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from datetime import date
import jwt
admin = Blueprint('admin', __name__)


@admin.route('/search', methods=['POST'])
@login_required
@admiN
def search():
    data = request.form.get('text')
    results = Student.query.filter_by(matriculation_number=data).all()
    if not results:
        results = Student.query.filter_by(name=str(data).lower()).all()
    student_schema = StudentSchema(many=True)
    res = student_schema.dump(results)
    return jsonify(res)

@admin.route('/search/lecturer', methods=['POST'])
@login_required
@admiN
def searchLecturer():
    data = request.form.get('text')
    print(str(data).lower())
    results = Lecturer.query.filter_by(email=data).all()
    if not results:
        results = Lecturer.query.filter_by(name=str(data).lower()).all()
    lecturer_schema = LecturerSchema(many=True)
    res = lecturer_schema.dump(results)
    return jsonify(res)




@admin.route('/all/admin', methods=['GET'])
@login_required
@admiN
def allAdmin():
    admin = Admin.query.all()
    hashed_password = bcrypt.generate_password_hash('stephen').decode('utf-8')
    print(hashed_password)
    return render_template('admin.html', admin=admin)


@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
@admiN
def AdminDashboard():
    admin = Admin.query.all()
    student = Student.query.all()
    length= len(student)
    lecturer = Lecturer.query.all()
    lengthLecturer= len(lecturer)
    faculty = Faculty.query.all()
    lengthFaculty= len(faculty)
    department = Department.query.all()
    lengthDepartment= len(department)
    return render_template("adminDashboard.html", lengthDepartment=length, lengthFaculty=lengthFaculty, admin=admin, length=length, lengthLecturer=lengthLecturer)

@admin.route('/login/admin', methods=['GET', 'POST'])
def loginAdmin():
    form = LoginAdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=True)
            next_page = request.args.get('next')
            session['account_type'] = 'Admin'
           
            return redirect(next_page) if next_page else redirect(url_for('admin.AdminDashboard'))
        else:
            redirect(url_for('admin.loginAdmin'))
    else:
        redirect(url_for('admin.loginAdmin'))
    return render_template('loginAdmin.html', title="Login to Portal", form=form)

@admin.route('/admin/lecturer/details', methods=['GET'])
@login_required
@admiN
def lecturerDashboard():
    d=bcrypt.generate_password_hash('admin').decode('utf-8')
    print(d)
    return render_template('lecturer.html')

@admin.route('/admin/lecturer/data/<string:unique_id>', methods=['GET'])
@login_required
@admiN
def lecturerData(unique_id):
    detail = Lecturer.query.filter_by(unique_id=unique_id).first()
    return render_template('lecturerdata.html', detail=detail)


@admin.route('/departments/<string:name>', methods=['GET'])
@login_required
@admiN
def department(name):
    data =[]
    faculty = Faculty.query.filter_by(name = name).first()
    dept= Department.query.filter_by(child=faculty).all()
    for i in dept:
        student = Student.query.filter_by(department=i.name).all()
        data.append(student)
    return render_template('department.html', faculty=faculty, dept=dept, data=data)



@admin.route('/department/level/<string:name>', methods=['GET'])
@login_required
@admiN
def level(name):
    data =[]
    faculty = Faculty.query.filter_by(name = name).first()
    dept= Department.query.filter_by(child=faculty).all()
    for i in dept:
        student = Student.query.filter_by(department=i.name).all()
        data.append({"name": i.name})
    return jsonify({"data": data})
##########################################################
@admin.route('/admin/log', methods=['GET'])
@login_required
@admiN
def log():

    return render_template('log.html')


@admin.route('/admin/add', methods=['GET'])
def addAdmin():
    form= AddAdminForm()
    if form.validate_on_submit():
        admin= Admin()
        admin.name= form.name.data
        admin.unique_id= str(uuid.uuid4())
        admin.gender = form.gender.data
        admin.position= form.position.data
        admin.email=form.email.data
        admin.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.sessiom.add(admin)
        db.session.commit()
        return redirect(url_for('admin.AdminDashboard'))


    return render_template('addAdmin.html', form=form)


@admin.route('/admin/message', methods=['GET','POST'])
@login_required
@admiN
def bulkMail():
    form = MailForm()
    if form.validate_on_submit():
        message = Message()
        message.title = form.title.data
        message.mail = form.mail.data
        message.from_ = 'school'
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('admin.AdminDashboard'))

    return render_template('mail.html', form=form)

@admin.route('/admin/message/lecturer', methods=['GET','POST'])
@login_required
@admiN
def bulkLecturerMail():
    form = MailForm()
    if form.validate_on_submit():
        message = LecturerMessage()
        message.title = form.title.data
        message.mail = form.mail.data
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('admin.AdminDashboard'))
    return render_template('lecturermail.html', form=form)

@admin.route('/admin/logout', methods=['GET'])
@login_required
@admiN
def logoutAdmin():
    logout_user()
    session.pop('account_type', None)
    return redirect(url_for('admin.loginAdmin'))

##############################################################

@admin.route('/admin/student/detail', methods=['GET'])
@login_required
@admiN
def studentDetail():

    return render_template('studentDetail.html')

@admin.route('/admin/control', methods=['GET'])
@login_required
@admiN
def adminControl():

    return render_template('adminControl.html')

@admin.route("/delete/student/<string:unique_id>", methods=['GET','POST'])
@login_required
@admiN
#@check_confirmed
def deleteStudent(unique_id):
    student = Student.query.filter_by(unique_id=unique_id).first()
    #if post.author != current_user:
        #abort(403)    
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('admin.AdminDashboard'))

@admin.route("/delete/lecturer/<string:unique_id>", methods=['GET','POST'])
@login_required
@admiN
#@check_confirmed
def deleteLecturer(unique_id):
    lecturer = Lecturer.query.filter_by(unique_id=unique_id).first()
    #if post.author != current_user:
        #abort(403)    
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('admin.AdminDashboard'))

@admin.route('/admin/student/data/<string:unique_id>', methods=['GET','POST'])
@login_required
@admiN
#@check_confirmed
def studentData(unique_id):
    detail = Student.query.filter_by(unique_id=unique_id).first()
    form = StudentPasswordForm()
    if form.validate_on_submit():
        detail.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        return redirect(url_for('admin.studentData', unique_id=detail.unique_id))

    return render_template('studentInfo.html', detail=detail, form=form)

today_date =date.today()
@admin.route('/student/register', methods=['GET','POST'])
@login_required
@admiN
def registerStudent():
    form = StudentRegistrationForm()
    if form.is_submitted():
      
        student = Student()
        student.unique_id = str(uuid.uuid4())
        student.name = str(form.name.data[0]).upper() +  str(form.name.data[1:]).lower()
        student.email = form.email.data
        student.password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student.nationality = form.nationality.data
        student.gender = form.gender.data
        student.date_of_birth =form.date_of_birth.data
        student.state_of_origin = form.state_of_origin.data
        student.local_government = form.local_government.data
        student.hometown = form.hometown.data
        student.address1 = form.address1.data
        student.marital_status = form.marital_status.data
        student.religion = form.religion.data
        student.photo = save_img(form.photo.data)
        student.phone_number = form.phone_number.data
        student.registration_number = form.registration_number.data
        student.matriculation_number = str(form. matricNo.data[0]).upper() + str(form. matricNo.data[1:]).lower()
        student.faculty = form.faculty.data
        student.department = form.department.data
        student.admission_year= form.admission_year.data
        student.programme_type = form.programme_type.data
        student.degree= form.degree.data
        student.passport= form.name.data
        student.level = today_date.year - form.admission_year.data
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("admin.studentDetail"))
    return render_template('studentReg.html', form=form)



@admin.route('/student/edit/<string:unique_id>', methods=['GET','POST'])
@login_required
@admiN
def editStudent(unique_id):
    form = StudentEditForm()
    if form.is_submitted():
        student = Student.query.filter_by(unique_id=unique_id).first()
        try:
            student.name = str(form.name.data[0]).upper() +  str(form.name.data[1:]).lower()
        except:
            pass
        student.email = form.email.data
        try:
            student.password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        except:
            pass
        
        student.nationality = form.nationality.data
        student.gender = form.gender.data
        student.date_of_birth =form.date_of_birth.data
        student.state_of_origin = form.state_of_origin.data
        student.local_government = form.local_government.data
        student.hometown = form.hometown.data
        student.address1 = form.address1.data
        student.marital_status = form.marital_status.data
        student.religion = form.religion.data
        student.phone_number = form.phone_number.data
        student.registration_number = form.registration_number.data
        try:
            student.matriculation_number = str(form. matricNo.data[0]).upper() + str(form. matricNo.data[1:]).lower()
        except:
            pass
        student.faculty = form.faculty.data
        student.department = form.department.data
        student.admission_year= form.admission_year.data
        student.programme_type = form.programme_type.data
        student.degree= form.degree.data
        student.passport= form.name.data
        #student.level = today_date.year - form.admission_year.data
        db.session.commit()
        return redirect(url_for("admin.studentDetail"))
    return render_template('editStudent.html', form=form)


@admin.route('/lecturer/register', methods=['GET','POST'])
@login_required
@admiN
def registerLecturer():
    form =LecturerRegistrationForm()
    if form.is_submitted():
        lecturer = Lecturer()
        lecturer.unique_id = str(uuid.uuid4())
        lecturer.name = str(form.name.data[0]).upper() +  str(form.name.data[1:]).lower()
        lecturer.email = form.email.data
        lecturer.password= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        lecturer.gender = form.gender.data
        lecturer.address= form.address1.data
        lecturer.date_of_birth =form.date_of_birth.data
        lecturer.marital_status = form.marital_status.data
        lecturer.phone_no = form.phone_number.data
        lecturer.faculty = form.faculty.data
        lecturer.department = form.department.data
        dept= Department.query.filter_by(name=form.department.data).first()
        if dept:
            lecturer.department_id = dept.id
        else:
            pass
        lecturer.cv = "Product Keys.txt"
        lecturer.one  = form.one.data
        lecturer.two  = form.two.data
        lecturer.three  = form.three.data
        lecturer.four  = form.four.data
        lecturer.five  = form.five.data
        lecturer.six  = form.six.data
        lecturer.seven  = form.seven.data
        
        lecturer.photo = save_img(form.photo.data)
        print(save_img(form.photo.data))
        lecturer.position = form.position.data
        #lecturer.course_handled= form.course_handled.data
        db.session.add(lecturer)
        db.session.commit()
        return redirect(url_for("admin.lecturerDashboard"))
    return render_template('lecturerReg.html', form=form)

#################### API ###################
@admin.route('/api/register/admin')
def regAdmin():
    data = request.get_json()
    name = data['name']
    email = str(data['email']).lower()
    gender = data['gender']
    password = data['password']
    try:
        admin = Admin()
        admin.company_name = str(name[0]).upper()+name[1:]
        admin.email = email
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        admin.password = hashed_password
        admin.country= country
        admin.confirmed = False
        db.session.add(admin)
        db.session.commit()
    except:
        return jsonify({
            "message": "Problem adding information to database, if such error persists, send message to fordstphn@gmail.com to lay complaint"
        })
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('registration.confirm_email', current_user=token, _external=True)
    html = render_template('confirm_url.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)
    
    return jsonify({
        "status ": "success",
        "message": "User added successfully, Please Verify Account",
        "token": token,
        "url": confirm_url,
        "verify Mail": 'A confirmation email has been sent via email.'
    
    }), 201


@admin.route('/api/login/admin', methods=['POST'])
@cross_origin()
def logInAdmin(expires_sec=30):
    data = request.get_json()
    try:
        email = data['email']
        admin = Admin.query.filter_by(email=email).first()
        if admin and bcrypt.check_password_hash(admin.password, data['password']):
            admin.logged_in =  admin.logged_in + 1
            db.session.commit()
            payload= {
                    "id": admin.id,  
                    "name": admin.company_name,
                    'exp' : datetime.datetime.now() + datetime.timedelta(minutes = 1),
                    "email": admin.email
                }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
            data = jwt.decode(token, Config.SECRET_KEY, algorithms="HS256")
            return jsonify({'token' : token.decode('UTF-8'),
            "name":data['name'], "email": data['email'], "expires": data['exp']} ), 201
        return jsonify({
            "message":
                'Could not verify user'}, 401)
    except:
        return jsonify({
            "message": 'Sorry there is error on our end'},
                500)
   
   
   
@admin.route('/open/portal')
@login_required
@admiN
def openPortal():
    portal= School.query.filter_by(id=1).first()
    if not portal:
        portal= School()
        portal.portal_toggle = True
        db.session.add(portal)
        db.session.commit()

    return redirect(url_for('admin.AdminDashboard'))
    
    
@admin.route('/close/portal')
@login_required
@admiN
def closePortal():
    portal= School.query.filter_by(id=1).first()
    if not portal:
        portal= School()
        portal.portal_toggle = False
        db.session.add(portal)
        db.session.commit()
    return redirect(url_for('admin.AdminDashboard'))
    

@admin.route('/add/course', methods=['GET','POST'])
@login_required
@admiN
def addCourse():
    form = AddCourseForm()
    if form.validate_on_submit():
        course = Courses()
        #result= Result()
        fdata=form.levels.data 
        sdata= form.semester.data
        print(fdata)
        if fdata == "one":
            eng = Faculty.query.filter_by(name=form.faculty.data).first()
            lecturer = Lecturer.query.filter_by(name=form.name.data).first()
            if sdata == 'one':
                course.semester = 1
            else:
                course.semester= 2
            try:
                course.lecturer_id= lecturer.id
            except:
                pass
            course.level= 1
            course.name = str(form.name.data[0]).upper()+str(form.name.data[1:]).lower()
            #result.course = str(form.name.data[0]).upper()+str(form.name.data[1:]).lower()
            db.session.add(course)
            #db.session.add(result)
            db.session.commit()
            return jsonify({"message":"course added"})
        else:
            eng = Faculty.query.filter_by(name=form.faculty.data).first()       
            dept= Department.query.filter_by(child=eng).filter_by(name=form.department.data).first()
            lecturer = Lecturer.query.filter_by(name=form.name.data).first()
            course = Courses()
            #result= Result()
            try:
                course.lecturer_id= lecturer.id
            except:
                pass
            course.department_id=dept.id
            course.name = str(form.name.data[0]).upper()+str(form.name.data[1:]).lower()
            if form.levels.data == "two":
                course.level = 2
            elif form.levels.data == "three":
                course.level = 3
            elif form.levels.data == "four":
                course.level = 4
            elif form.levels.data == "five":
                course.level = 5
            elif form.levels.data == "six":
                course.level = 6
            elif form.levels.data == "seven":
                course.level = 7
            if form.semester.data == "one":
                course.semester =1
            else:
                course.semester =2
            db.session.add(course)
            db.session.commit()
            return jsonify({"message":"course added"})
    return render_template('addcourse.html', form=form)

