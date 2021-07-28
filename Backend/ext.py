import random
from flask import *
from flask_login import login_required
from Backend import *
from Backend.models import *
from flask_cors import cross_origin
from functools import wraps
import jwt



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
        except:
            return jsonify({
                'message' : 'No Token sent, User not logged in'
            }), 401
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = Admin.query\
                .filter_by(email = data['email']).first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401 
        
        return  f(current_user, *args, **kwargs)
   
    return decorated

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
