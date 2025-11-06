# models.py
from flask_sqlalchemy import SQLAlchemy

# db object ko initialize kiye bina yahan define karte hain.
# Isko main app file mein initialize kiya jayega.
db = SQLAlchemy()

# ======================= MODELS ===========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(200), nullable=True, unique=True)
    mobile = db.Column(db.String(16), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    profile = db.relationship('UserProfile', backref='user', uselist=False)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(200))
    alternate_mo = db.Column(db.String(16))
    pincode = db.Column(db.Integer)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    flat_no = db.Column(db.String(100))
    address_remark = db.Column(db.String(1000))
    photo = db.Column(db.String(300))
    
class SellerRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_name = db.Column(db.String(100), nullable=False)
    mobile_no = db.Column(db.String(16), nullable=False, unique=True)
    password=db.Column(db.String(200))
    email = db.Column(db.String(200), nullable=False, unique=True)
    shop_name = db.Column(db.String(200), nullable=False)
    shop_type = db.Column(db.String(100))
    pincode = db.Column(db.String(10), nullable=False)
    shop_address = db.Column(db.String(500), nullable=False)
    registration_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Pending Review')
    remark = db.Column(db.String(1000))