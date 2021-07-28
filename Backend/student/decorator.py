from functools import wraps
from Backend.ext import token_required
from flask import jsonify
from flask_login import login_required



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
