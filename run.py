#!/usr/bin/python3
from Backend import create_app, db
from Backend.models import Student, Admin
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

app = create_app()
app.app_context().push()

manager = Manager(app)
migrate = Migrate(app, db)


ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    threaded = True
else:
    app.debug = False
    threaded = True

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)



@manager.command
def create_tables():
    db.create_all()

@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    Admin.generate_fake(count=number_users)


if __name__ == '__main__':
    app.run(port=5001)
    #db.drop_all(app=create_app())
    #db.create_all(app=create_app())