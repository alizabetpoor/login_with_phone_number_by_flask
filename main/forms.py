from flask.app import Flask
from main.models import User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import EqualTo,Email,DataRequired, ValidationError
class register_form(FlaskForm):
    username=StringField("username",validators=[DataRequired()],render_kw={"id":"floatingusername","placeholder":"alizabetpoor"})
    email=StringField("email",validators=[DataRequired(),Email()],render_kw={"id":"floatingemail","placeholder":"email@gmail.com"})
    phonenumber=StringField("phonenumber",validators=[DataRequired()],render_kw={"id":"floatingphonenumber","placeholder":"09111194521"})
    password=PasswordField("password",validators=[DataRequired()],render_kw={"id":"floatingpassword","placeholder":"******"})
    confrim_password=PasswordField("password",validators=[DataRequired(),EqualTo("password","password doesn't match")],render_kw={"id":"floatingconfrimpassword","placeholder":"******"})
    submit=SubmitField("submit")
    def validate_phonenumber(self,phonenumber):
        if len(phonenumber.data)!=11 or phonenumber.data[0]!="0":
            raise ValidationError("phone number is wrong")
        if User.query.filter_by(phonenumber=phonenumber.data).first():
            raise ValidationError("this phone number is exist in database")
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("this username is exist in database")
    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("this email is exist in database")
class login_form(FlaskForm):
    phonenumber=StringField("phonenumber",validators=[DataRequired()],render_kw={"id":"floatingphonenumber","placeholder":"09111194521"})
    password=PasswordField("password",validators=[DataRequired()],render_kw={"id":"floatingpassword","placeholder":"******"})
    submit=SubmitField("submit")
    def validate_phonenumber(self,phonenumber):
        if len(phonenumber.data)!=11 or phonenumber.data[0]!="0":
            raise ValidationError("phone number is wrong")
class verify_form(FlaskForm):
    code=StringField("code",validators=[DataRequired()],render_kw={"id":"floatingcode","placeholder":"******"})
    submit=SubmitField("submit")