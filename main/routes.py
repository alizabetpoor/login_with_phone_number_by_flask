from flask import render_template,redirect,url_for,flash,abort
import requests
from main.models import User
from main.forms import register_form,login_form,verify_form
from main import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
from random import randint
@app.route("/")
def index():
    return render_template("index.html",title="home")
@app.route("/register",methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form=register_form()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,phonenumber=form.phonenumber.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash("your account has been created",category="success")
        return redirect(url_for("login"))
    return render_template("register.html",title="register",form=form)
def send_code(code,phonenumber):
    '''send verify code to user'''
    #username of your sms panel
    username="username"
    #password of your sms panel
    password="password"
    #phone number of your sms panel
    sms_panel_phonenumber="number"
    requests.get(f"https://raygansms.com/SendMessageWithUrl.ashx?Username={username}&Password={password}&PhoneNumber={sms_panel_phonenumber}&MessageBody={code}&RecNumber={phonenumber}&Smsclass=1")
@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    form=login_form()
    if form.validate_on_submit():
        
        
        phonenumber=form.phonenumber.data
        user=User.query.filter_by(phonenumber=phonenumber).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            code=randint(1000,9999)
            user.code=code
            db.session.commit()
            token=user.get_login_token()
            send_code(code,user.phonenumber)
            flash("the code has been sent to your phone",category="success")
            return redirect(url_for("verify",token=token))
        else:
            flash("this number doesn't exist or the password is wrong",category="error")
            return redirect(url_for("login"))
    return render_template("login.html",title="login",form=form)
@app.route("/verify/<token>",methods=["POST","GET"])
def verify(token):
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    user=User.check_token(token)
    if user:
        form=verify_form()
        if form.validate_on_submit():
            if form.code.data==user.code:
                login_user(user)
                flash("you logged in seccessfully",category="success")
                return redirect(url_for("profile"))
            else:
                flash("your code is wrong",category="error")
                return redirect(url_for("verify",token=token))
    else:
        abort(403)
    return render_template("verify.html",title="verify",form=form)
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html",title="profile")
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))