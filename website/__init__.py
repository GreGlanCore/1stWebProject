from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os



db              = SQLAlchemy()
basedir         = os.path.abspath(os.path.dirname(__file__))    # pagkuha sa directory.
database_folder = os.path.join(basedir, 'instance')             # Define sa data path sod sa 'instance' folder.
db_path         = os.path.join(database_folder, 'database.db')  # Set the URI for SQLAlchemy





def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "GregRasonabe"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)




    from .views import views                        # gikan ni sa views.py
    from .auth import auth                          # gikan ni sa auth.py

    app.register_blueprint(views, url_prefix='/')   # ang naka register ray maka access sa ilang ka ugalingon nga records.
    app.register_blueprint(auth, url_prefix='/')    # e register nato ang mga account nga naka login while running ang
                                                    # system kay naka register man sila ani nga system. otherwise deli ka access sa system.


    from .models import User, Note                  # gikan ni sa models.py


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists(database_folder):         # e sure and 'instance' folder nga naa gyud.
        os.makedirs(database_folder)

        with app.app_context():
            db.create_all()
            print('Created Database!')

