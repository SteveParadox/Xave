from functools import wraps
from Backend.ext import token_required
from flask import jsonify
from flask_login import login_required, current_user
from Backend.models import *


def check_confirmed(func):
    @login_required
    @wraps(func)
    def decorated_function(current_user, *args, **kwargs):
        if current_user.confirmed is False:
            return jsonify({
                "message": 'Please confirm your account!'
            })
        return func(*args, **kwargs)

    return decorated_function


def studenT(func):
    @login_required
    @wraps(func)
    def decorated_function(*args, **kwargs):
        student = Student.query.filter_by(unique_id=current_user.unique_id).first()
        if not student:
            return jsonify({
                "message": 'Student access is required for this operation'
            })
        return func(*args, **kwargs)

    return decorated_function
