import datetime
from flask import *
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from Backend.config import Config
from flask_profiler import Profiler
from flask_login import LoginManager

app= Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['flask_profiler']={
	"enabled":app.config['DEBUG'],
	"storage":{
		"engine": "postgresql"	
	},
	"basicAuth":{
	"enabled": True,
	"username": "admin",
	"password": "admin"
	}
}

bcrypt= Bcrypt()
jwt= JWTManager()
mail = Mail()
ma = Marshmallow()
db = SQLAlchemy()
profiler = Profiler()
login_manager = LoginManager()
login_manager.login_view = 'student.loginPortal'
login_manager.login_message = None
login_manager.session_protection = "strong"
REMEMBER_COOKIE_NAME= 'remember_token'
REMEMBER_COOKIE_DURATION=datetime.timedelta(days=64, seconds=29156, microseconds=10)
REMEMBER_COOKIE_REFRESH_EACH_REQUEST=False


def create_app(config_class=Config):
    db.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    #profiler.init_app(app)
    login_manager.init_app(app)


    from Backend.admin.routes import admin
    from Backend.financial.routes import financial
    from Backend.lecturer.routes import lecturer
    from Backend.student.routes import student
    from Backend.records.routes import records
    from Backend.messaging.routes import msg

    app.register_blueprint(admin)
    app.register_blueprint(financial)
    app.register_blueprint(lecturer)
    app.register_blueprint(records)
    app.register_blueprint(student)
    app.register_blueprint(msg)

    @app.cli.command()
    def routes():
        """'Display registered routes"""
        rules = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(sorted(rule.methods))
            rules.append((rule.endpoint, methods, str(rule)))

        sort_by_rule = operator.itemgetter(2)
        for endpoint, methods, rule in sorted(rules, key=sort_by_rule):
            route = '{:50s} {:25s} {}'.format(endpoint, methods, rule)
            print(route)
        

    return app





