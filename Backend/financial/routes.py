import datetime
import os
from flask import *
from flask_login import login_required
from Backend.models import *
from Backend import db, bcrypt
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required, check_confirmed

financial = Blueprint('financial', __name__)

@financial.route('/fees/history/<string:student_id>', methods=['GET'])
@login_required
@check_confirmed
def feesHistory():
    detail = Student.query.filter_by(unique_id=unique_id).first()
    history= Financial.query.filter_by(payment=detail).all()
    return render_template('', history=history)
    