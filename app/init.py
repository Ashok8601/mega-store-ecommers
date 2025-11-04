from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # top-level, function के बाहर

def create_app():
    app = Flask(__name__)
    app.secret_key = "secretkey"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db bind with app
    db.init_app(app)

    # import routes inside function
    from .routes import main
    app.register_blueprint(main)

    # create tables
    with app.app_context():
        from .models import User
        db.create_all()

    return app