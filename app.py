from flask import Flask, render_template, request, redirect,flash, session ,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.secret_key="ashokkumar"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    mobile = db.Column(db.String(16), nullable=False, unique=True)
    password=db.Column(db.String(200), nullable=False)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        
        if not all([name, email, mobile, password]):
            
            flash("Please fill in all the required fields.", "error") 
            return redirect(url_for('signup')) 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email is already registered. Please log in.", "warning")
            return redirect(url_for('signup'))

        
        hash_pass = generate_password_hash(password)
        user = User(name=name, email=email, mobile=mobile, password=hash_pass)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login')) 
        
        except Exception:
            
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "error")
            return redirect(url_for('signup'))

    
    return render_template("signup.html")
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        mobile=request.form.get('mobile')
        password=request.form.get('password')
        if not password or not mobile:
            flash("mobile and password required ","warning")
            return render_template("login.html"),400
        
        try:
            user=User.query.filter_by(mobile=mobile).first()
            if not user:
                flash(" user not registered to this mobile number"),405
                return render_template("login.html")
            if check_password_hash(user.password, password):
                session["user_id"]=user.id
                return redirect('/')
            else:
                flash( "Entered password doesn't match ","dengerous")
        except Exception as e:
            flash( f"an error occurred {str (e)}")
    return render_template("login.html")

@app.route('/dashboard', methods=['GET', 'POST'])    
def dashboard():
    if 'user_id' in session:
        
        user = User.query.get(session['user_id'])
        
        
        if user:
            return render_template("dashboard.html", user=user)
        else:
            
            session.pop('user_id', None) 
            flash("User not found. Please log in again.", "error")
            return redirect(url_for('login'))
            
    else: 
        
        flash("You need to be logged in to access the dashboard.", "warning")
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id',None)
        flash("successfully logout")
   else: 
       flash("user not logged in")
   return redirect('/login')
if __name__ == "__main__":
    app.run(debug=True)