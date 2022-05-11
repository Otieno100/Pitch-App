from crypt import methods
import email
# from turtle import title
# from turtle import title
import bcrypt
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from wtforms import StringField,SubmitField,PasswordField,FileField,TextAreaField,EmailField
from wtforms.validators import DataRequired
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_manager, login_required,login_user,logout_user,LoginManager,current_user
from flask_mail import Message, Mail
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'
app.config['SECRET_KEY']='my secrecte key'
bcrypt = Bcrypt(app)


db = SQLAlchemy(app)
migrate = Migrate(app,db)


class pitch(db.Model) :
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(50),nullable = False)
    comments = db.Column(db.String(400),nullable = False)

class comments(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(25),nullable =False) 
    Addpitch = db.Column(db.String(50),nullable =False)
 
#     replies_id = db.Column(db.Integer,db.Foreignkey('replies.id'))




class RegisterFrm(FlaskForm):
    name=StringField("username",validators=[DataRequired()])
    email=EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    cnfpass=PasswordField("Confirm Password",validators=[DataRequired()])
    submt=SubmitField('Register')





@app.route('/register',methods=['POST','GET'])
def register():
    frm=RegisterFrm()
    if frm.validate_on_submit():
        if frm.password.data==frm.cnfpass.data:
            hash_pwd=bcrypt.generate_password_hash(frm.password.data)
            newuser=User(username=frm.name.data,email=frm.email.data,password=hash_pwd)
            db.session.add(newuser)
            db.session.commit()
            msg=Message(subject=" POSTER APP REGISTRATION",recipients=[frm.email.data],body=frm.name.data+" Thank you for registering")
            mail.send(msg)
        #     return redirect(url_for('login'))
        # else:
        #     flash(" Passwords do not match")

      

    return render_template('register.html',form=frm)






# class Replies(db.Model):
#     id = db.Column(db.Integer,primary_key = True)
#     replies =db.Column(db.Integer,nullable = False)
#     type = db.Column(db.Interger,nullable = False)
#     comments = db.relationship('comments,',backref = 'replies') 


class User(db.Model) :
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30),nullable = False) 
    email = db.Column(db.String(20),nullable = False)
    password = db.Column(db.String(200), nullable = False)


class UpdateForm(FlaskForm) :   
    name = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    cnfpass=PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField('login')




class UserForm (FlaskForm) :
    title = StringField(' pitch title',validators = [DataRequired()])
    Addpitch = StringField('Enter your first pitch',validators = [DataRequired()])
   
    submit = SubmitField('submit')


@app.route('/login', methods = ['POST','GET'])
def login():
    updateUser =UpdateForm()
  
    if updateUser.validate_on_submit():
        if updateUser.cnfpass.data==updateUser.password.data:
           hash_pwd = bcrypt.generate_password_hash(updateUser.password.data)
        user = User(name = updateUser.data, email = updateUser.data, password = hash_pwd)
        session['name'] = updateUser.name.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('display'))

    return render_template('login.html', form = updateUser)




#user form 
@app.route('/user')
def user():
    pitch = comments.query.all()
    return render_template('user.html',data = pitch)




@app.route('/display')
def display():
    # querry selector
    qr_all =comments.query.all()
#  return redirect(url_for('login'))

     
    return render_template('display.html', data = qr_all)


@app.route('/', methods = ['POST','GET'])
def index():

    dataForm =UserForm()


    if dataForm.validate_on_submit():
        addpit = comments(Addpitch = dataForm.Addpitch.data, title = dataForm.title.data)
        db.session.add(addpit)
        # db.session.add(title)
        db.session.commit()




        return redirect(url_for('login'))


         #user section
    # if request.method == 'POST':

    #     # adding data to my tables
    #     form = request.form
    #     addpit =comments(yourname =form['name'],pitch = form['pitchsection'])
    #     db.session.add(addpit)
    #     db.session.commit()

    # return render_template('user.html')
        # return redirect(url_for('user'))



    return render_template('update.html',form = dataForm,)    



if __name__== '__main__':
    app.run(debug = True)

    
