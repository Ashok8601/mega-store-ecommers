from flask import redirect,render_template,url_for,session, request, Blueprint
from . import db
from models import User
main=Blueprint('main',__name__)

@main.route('/')
def home():
    return render_template("home.html")
    
@main.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name=request.form.get("name")
        mobile=request.form.get("mobile")
        email=request.form.get("email")
        password=request.form.get("password")
        user=User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return "signup success"
    return render_template("signup.html")
    
    