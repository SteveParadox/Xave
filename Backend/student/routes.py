from flask import *
import uuid 
from flask_login import login_required, current_user, login_user,logout_user
from Backend.models import *
from Backend import db, bcrypt
from Backend.config import Config
from flask_cors import cross_origin
from Backend.ext import token_required
from Backend.student.decorator import check_confirmed
from Backend.student.form import *
from Backend.student.decorator import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

student = Blueprint('student', __name__)



@student.route('/login/portal', methods=['GET', 'POST'])
def loginPortal():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).filter_by(matriculation_number=form.matriculation_number.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            next_page = request.args.get('next')
            session['account_type'] = 'Student'
            return redirect(next_page) if next_page else redirect(url_for('student.myProfile'))
            
  
        else:
            redirect(url_for('student.loginPortal'))
    return render_template('login.html', title="Login to Portal", form=form)


@student.route('/')
def home():

    return render_template('homepage.html')

@student.route('/dashboard/select')
@login_required
def selectDashboard():
    if current_user.is_authenticated:
        name = Student.query.filter_by(unique_id=current_user.unique_id).first()
        if name:
            return redirect(url_for('student.dashboard'))
        elif not name:
            name = Lecturer.query.filter_by(unique_id=current_user.unique_id).first()
            if name:
                return redirect(url_for('lecturer.lecturerdashboard'))
            elif not name:
                return redirect(url_for('admin.AdminDashboard'))
    return redirect(url_for('student.home'))


@student.route('/logout/select')
@login_required
def selectLogout():
    if current_user.is_authenticated:
        name = Student.query.filter_by(unique_id=current_user.unique_id).first()
        if name:
            return redirect(url_for('student.logoutStudent'))
        elif not name:
            name = Lecturer.query.filter_by(unique_id=current_user.unique_id).first()
            if name:
                return redirect(url_for('lecturer.logoutLecturer'))
            elif not name:
                return redirect(url_for('admin.logoutAdmin'))
    return redirect(url_for('student.home'))

@student.route('/test/profile')
@login_required
@studenT
def myProfile():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    return render_template('profile.html')


@student.route('/other')
@login_required

def _():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    return render_template('other.html')


@student.route('/student/mail')
@login_required
@studenT
def studentMail():
    message = Message.query.order_by(Message.created_on.desc()).all()
    return render_template('message.html', message=message)

@student.route('/student/mail/<int:msg_id>')
@login_required
@studenT
def messageDetail(msg_id):
    msg = Message.query.filter_by(id=msg_id).first()

    return render_template('msgDetailStudent.html', msg=msg)

@student.route('/update/profile', methods=['GET','POST'])
@login_required
@studenT
def updateProfile():
    form = UpdateDetailForm()
    detail = Student.query.filter_by(unique_id=current_user.unique_id).first()
    if form.validate_on_submit():
        detail.phone_number=form.phone_number.data
        detail.email = form.email.data
        detail.marital_status = form.marital_status.data
        detail.address1 = form.address1.data
        detail.religion = form.religion.data
        db.session.commit()
    elif request.method == 'GET':
        form.phone_number.data = detail.phone_number
        form.email.data = detail.email
        form.religion.data= detail.religion
        form.address1.data=detail.address1
        form.marital_status.data= detail.marital_status
        

    return render_template('updateProfile.html', detail=detail, form=form)

@student.route('/student/biodata')
@login_required
@studenT
def bioData():
    detail = Student.query.filter_by(unique_id=current_user.unique_id).first()
    
    return render_template('bioData.html', detail=detail)


@student.route('/student/dashboard')
@login_required
@studenT
def dashboard():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    semester = School.query.filter_by(name="semester").first()
    week = School.query.filter_by(name="week").first()
    return render_template('dashboard.html',semester=semester, week=week)


@student.route('/student/fees')
@login_required
@studenT
def feeStatus():
    #detail = Student.query.filter_by(unique_id=unique_id).first()
    portal = School.query.filter_by(id=1).first()
    return render_template('fees.html')


@student.route('/student/result')
@login_required
@studenT
def result():
    res =Result.query.filter_by(student_id=current_user.id).all()
    return render_template('result.html', res=res)



@student.route('/register/courses', methods=['GET','POST'])
@login_required
@studenT
def registerCourses():
    dept = Department.query.filter_by(name=current_user.department).first()
    if current_user.level == 1:
        pass
    else:
        courses = Courses.query.filter_by(level=current_user.level).filter_by(subject=dept).all()
        for i in courses:
            form = RegisterCoursesForm()
            if form.validate_on_submit():
                for i in courses:
                    register=Registered(student_id=current_user.id, course_id=i.id)
                    register.register = form.registered.data
                    db.session.add(register)
                    db.session.commit()
                return redirect(url_for('student.registerCourses'))
        
    return render_template('courses.html', courses=courses, dept=dept, form=form)


@student.route('/view/registered/courses')
@login_required
@studenT
def viewRegisteredCourses():
    f= []
    dept = Department.query.filter_by(name=current_user.department).first()
    courses = Courses.query.filter_by(level=current_user.level).filter_by(subject=dept).all()
    for i in courses:
        register = Registered.query.filter_by(course_id=i.id).filter_by(register=True).all()
        if register:
            f.append(i)
    return render_template('registeredCourses.html', courses=courses, dept=dept, f=f)



@student.route('/failed/courses')
@login_required
@studenT
def failedCourses():
    

    return render_template('')




@student.route('/logout')
@login_required
@studenT
def logoutStudent():
    logout_user()
    session.pop('account_type', None)
    return redirect(url_for('student.loginPortal'))


@student.route('/student/profile/<string:unique_id>', methods=['GET'])
@login_required
@studenT
def studentProfile(unique_id):
    datalist = []
    detail = Student.query.filter_by(unique_id=unique_id).first()
    for stud in detail:
        datalist.append({
            "name": stud.name,
            "gender": stud.gender,
            "date of birth": stud.date_of_birth,
            "nationality": stud.nationality,
            "state of origin": stud.state_of_origin,
            "local government": stud.local_government,
            "home town": stud.hometown,
            "address1": stud.address1,
            "address2": stud.address2,
            "marital status": stud.marital_status,
            "religion": stud.religion,
            "phone number": stud.phone_number,
            "email address" :stud.email
        })

    return render_template('profile.html', detail=detail)




############## api 

@student.route('/api/register', methods=['POST'])
def regPortal():
    data= request.get_json()
    student = Student()
    student.unique_id = str(uuid.uuid4())
    student.name = data['name']
    student.email = data['email']
    student.password= bcrypt.generate_password_hash(data['password']).decode('utf-8')
    student.nationality = data['nationality']
    student.gender = data['gender']
    student.date_of_birth =data['dob']
    student.state_of_origin = data['soo']
    student.local_government = data['lga']
    student.hometown = data['hometown']
    student.address1 = data['address1']
    student.marital_status =data['marital_status']
    student.religion = data['religion']
    student.phone_number = data['phone']
    student.registration_number = data['reg']
    student.matriculation_number = data['matric_no']
    student.faculty = data['faculty']
    student.department = data['department']
    student.admission_year= data['year']
    student.programme_type = data['programme']
    student.degree= data['degree']
    db.session.add(student)
    db.session.commit()
    return jsonify({
        "message": "student registered"
    })