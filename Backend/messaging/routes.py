from flask import *
from flask_login import login_required
from Backend.models import *
from Backend import db, bcrypt
from flask_cors import cross_origin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Backend.config import Config
from Backend.ext import token_required, check_confirmed

msg = Blueprint('msg', __name__)




