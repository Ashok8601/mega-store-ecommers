from flask import Flask, render_template, request, redirect, flash, session, url_for, send_from_directory

from models import db, User, UserProfile,SellerRegistration
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "ashokkumar"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cart.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = 'user_upload'

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


db.init_app(app)


with app.app_context():
    db.create_all()


# ======================= ROUTES ===========================
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')

        if not password or not mobile:
            flash("Mobile and password required.", "warning")
            return render_template("login.html"), 400

        try:
            user = User.query.filter_by(mobile=mobile).first()
            if not user:
                flash("User not registered with this mobile number.", "warning")
                return render_template("login.html")

            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                return redirect('/')
            else:
                flash("Entered password doesn't match.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}")

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
        session.pop('user_id', None)
        flash("Successfully logged out.", "success")
    else:
        flash("User not logged in.", "warning")
    return redirect('/login')


@app.route('/user_upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash("User not logged in.")
        return redirect('/login')

    user_id = session.get('user_id')
    user = User.query.get(user_id)
    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        file = request.files.get("user_photo")
        filepath = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
        else:
            
            if profile:
                filepath = profile.photo


    
        username = request.form.get("username")
        alternate_mo = request.form.get("alternate_mo")
        
        try:
            pincode = int(request.form.get("pincode"))
        except (ValueError, TypeError):
            pincode = None 
            
        state = request.form.get("state")
        district = request.form.get("district")
        city = request.form.get("city")
        flat_no = request.form.get("flat_no")
        address_remark = request.form.get("address_remark")

        
        if profile:
            profile.username = username
            profile.alternate_mo = alternate_mo
            profile.pincode = pincode
            profile.state = state
            profile.district = district
            profile.city = city
            profile.flat_no = flat_no
            profile.address_remark = address_remark
            if filepath:
                profile.photo = filepath
            flash("Profile updated successfully!", "success")
        else:
            profile = UserProfile(
                user_id=user_id,
                username=username,
                alternate_mo=alternate_mo,
                pincode=pincode,
                state=state,
                district=district,
                city=city,
                flat_no=flat_no,
                address_remark=address_remark,
                photo=filepath
            )
            db.session.add(profile)
            flash("Profile created successfully!", "success")

        try:
            db.session.commit()
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving the profile: {str(e)}", "error")
            
            return render_template("profile.html", profile=profile, user=user)


    return render_template("profile.html", profile=profile, user=user)


@app.route('/seller_registration', methods=['GET', 'POST'])
def seller_registration():
    if request.method == 'POST':
        seller_name = request.form.get('name')
        mobile_no = request.form.get('mobile_no')
        password=request.form.get('password')
        email = request.form.get('email')
        shop_name = request.form.get('shop_name')
        pincode = request.form.get('pincode')
        shop_type = request.form.get('shop_type')
        shop_address = request.form.get('shop_address')
        remark = request.form.get('remark')
        if not all([seller_name, mobile_no, password ,email, shop_name, pincode, shop_type, shop_address]):
            flash("All Field required")
            return redirect("/seller_ragistration")
        hash_pass=generate_password_hash(password)
        existing_seller=SellerRegistration.query.filter((SellerRegistration.mobile_no==mobile_no) |(SellerRegistration.email==email)).first()
        if existing_seller:
            flash("A Seller registered with this email and mobile ")
            return redirect('/login')
        seller=SellerRegistration(seller_name=seller_name,
            mobile_no=mobile_no,
            email=email,
            password=hash_pass,
            shop_name=shop_name,
            pincode=pincode,
            shop_type=shop_type,
            shop_address=shop_address,
            remark=remark,
            status='Pending Review') 
        try:
              db.session.add(seller)
              db.session.commit()
              flash("Seller Ragistration successful")
              return redirect('/login')
        except Exception as e:
              db.session.rollback()
              flash(f"An Error occurred during seller ragistration{str(e)}")
              return redirect('/seller_registration')

    return render_template("seller_registration.html")


if __name__ == "__main__":
    app.run(debug=True)