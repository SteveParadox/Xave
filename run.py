#!/usr/bin/python3
from Backend import create_app, db
from Backend.models import Student, Admin

app = create_app()
app.app_context().push()


ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    threaded = True
else:
    app.debug = False
    threaded = True


if __name__ == '__main__':
    app.run(port=5001)
    #db.drop_all(app=create_app())
    #db.create_all(app=create_app())