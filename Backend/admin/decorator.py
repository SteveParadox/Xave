from functools import wraps
from Backend.ext import token_required
from flask import jsonify
import random
from flask import *
from Backend import *
from Backend.models import Admin
from flask_cors import cross_origin
from functools import wraps
import jwt






def portal_toggle(func):
    @token_required
    @wraps(func)
    def decorated_function(*args, **kwargs):
        school = School.query.first()
        if not school.portal_toggle==True:
            return jsonify({
                "message": 'Portal is currently closed'
            })
        return func(*args, **kwargs)

    return decorated_function





def check_confirmed(func):
    @token_required
    @wraps(func)
    def decorated_function(current_user, *args, **kwargs):
        admin = Admin.query.filter_by(unique_id=current_user.unique_id).first()
        if not admin:
            return jsonify({
                "message": 'Admin access is required for this operation'
            })
        return func(*args, **kwargs)

    return decorated_function




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            # Get token from header here
            incoming = request.get_json()
            token = incoming['token']
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

