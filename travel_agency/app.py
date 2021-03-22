from flask import Flask,render_template,url_for,redirect,request,session,flash

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import insert
import pdb
from datetime import  date

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired
from wtforms import StringField
from wtforms import IntegerField
from flask_mail import Mail,Message

from flask_login import LoginManager, UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, login_required

import flask_login

from flask_login import login_required, current_user


app = Flask(__name__)




#app.config['MAIL_SERVER']='smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'None'
#app.config['MAIL_PASSWORD'] = 'None'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True



#mail = Mail(app)

app.secret_key="lkjh0987"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///traveldb.db")

db = SQLAlchemy(app)


login_manager= LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return register.query.get(int(user_id))


class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userid = IntegerField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    email = StringField('Email Address', [validators.Length(min=6, max=35)])

    number = IntegerField('Number', validators=[DataRequired()])


class Myform_login(FlaskForm):

	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me',validators=[DataRequired()])
	email = StringField('Email Address', [validators.Length(min=6, max=35)])

class MyForm_blog(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userid = IntegerField('userid', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])
    blog_id = IntegerField('blogid', validators=[DataRequired()])
    image= FileField(validators=[FileRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])

    description= StringField('description', validators=[DataRequired()])



class register(UserMixin,db.Model):

	id = db.Column(db.Integer,unique=True,primary_key=True)

	userid = db.Column(db.Integer,  nullable=False)
	username=db.Column(db.String(30),  nullable=False)
	password = db.Column(db.String(30),  nullable=False)
	email=db.Column(db.String(30),  nullable=False)
	number=db.Column(db.Integer)
	

	def __init__(self,username , password,email,number,userid):
		self.userid = userid
		self.username = username
		self.password = password
		self.email = email
		self.number = number


class blogs(db.Model):

	id= db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String(20),db.ForeignKey('register'))
	username= db.Column(db.String(30),  nullable=False)
	blog_id=db.Column(db.Integer)
	image= db.Column(db.String(30))
	date= db.Column(db.DateTime, nullable=False )
	title=db.Column(db.String(20))
	text=db.Column(db.Text(100),  nullable=False)
	email=db.Column(db.String(20))
	def __init__(self,username , image,date,title,text,userid,blog_id,email):
		
		self.userid=userid
		self.username = username
		self.image = image
		self.date= date
		self.title = title
		self.text = text
		self.email = email
		self.blog_id= blog_id
date=date.today()

class booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	username = db.Column(db.String(20), nullable=False)

	email= db.Column(db.String(30), unique=True, nullable=False)
	source=db.Column(db.String(30),  nullable=False)
	destination=db.Column(db.String(30),  nullable=False)
	s_date=db.Column(db.Integer)

	e_date=db.Column(db.Integer)
	adults=db.Column(db.Integer)
	children=db.Column(db.Integer)

	def __init__(self,username , email,source,destination,s_date,e_date,adults,children):
		
		self.username = username
		self.email = email
		self.source = source
		self.destination = destination
		self.s_date= s_date
		self.e_date = e_date
		self.adults= adults
		self.children=children










@app.route('/')
def home():
	return render_template('home.html')
   

@app.route('/about')
def about():
	return render_template('about.html')




@app.route('/addblog',methods=["POST", "GET"])
def addblog():
	if current_user.is_authenticated:
		form = MyForm_blog()
		user=flask_login.current_user
		print(user)
		
		if request.method == "POST":

		

			addblogs = blogs (userid=form.userid.data,username=form.username.data,image=form.image.data,date=date,title=form.title.data,text=form.description.data,email=form.email.data,blog_id=form.blog_id.data)
			
			print(request.form)


			db.session.add(addblogs)
			db.session.commit()

			userid1=request.form["userid"]

			return redirect(url_for("blogs1",result=userid1))
		

		result1=register.query.filter_by(email=current_user.email).first()

		return render_template("addblog.html",result=result1,form=form)
	return redirect(url_for("login"))

@app.route('/blog')
def blog():

	result1=register.query.filter_by(email=email).first()


	return render_template('blog.html')



@app.route('/update',methods = ['GET','POST'])
def update():
	if current_user.is_authenticated:
		
		details = blogs.query.filter_by(email=current_user.email).first()

		return render_template("updateblogs.html",result=details)

	return redirect(url_for("login"))



@app.route('/updated',methods = ['GET','POST'])
def updated():
	if current_user.is_authenticated:
		if request.method == 'POST':
			details = blogs.query.filter_by(email=current_user.email).first()
			if details:
				db.session.delete(details)
				db.session.commit()
	 
				userid=request.form["userid1"]
				name=request.form["name"]
				title=request.form["title"]
				image=request.form["img"]
				text=request.form["text"]
				email=request.form["email"]
				blog_id=request.form["blog_id"]

				details= blogs(username=name,userid=userid,title=title,image=image,text=text,date=date,blog_id=blog_id,email=email)
				db.session.add(details)
				db.session.commit()
				
				return redirect(url_for("blogs1"))

			return f"user with id = {user} Does not exist"

		details = blogs.query.filter_by(email=current_user.email).first()
		return render_template('updateblogs.html', result = details)
	return redirect(url_for("login"))




@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/page')
def page():
	return render_template('page.html')



@app.route('/login',methods=["POST", "GET"])
def login():
	form = Myform_login()
	if request.method == "POST":
		if form.validate_on_submit(): 
			user=form.email.data
			session["user"]=user

			user1=form.password.data
			
			user=register.query.filter_by(email=user).first()
		
			
			#return redirect(url_for("addblog",user=user))
			if not user or not check_password_hash(user.password,user1):
			#if login is not None:
				flash("check login credential")
				return(redirect(url_for("login",form=form)))


			login_user(user)
			flash("you have been logged in")
			return redirect(url_for("home"))
			#return redirect(url_for("user", user=user))
		
	return render_template('login.html',form=form)


#@app.route("/user")*
#def user():
#	if "user" in session:
#		user=session["user"]

#		return f"<h1>{user}</h1>"

#	else:
#		return redirect(url_for("login"))


	

@app.route('/signup',methods=["POST","GET"])
def signup():
	
	form = MyForm()
	
	if request.method == "POST":
		if form.validate_on_submit(): 
			email=form.email.data
			signup=register.query.filter_by(email=email).first()
			if signup:  # if a user is found, we want to redirect back to signup page so user can try again
				flash('Email address already exists')
				return redirect(url_for('signup'))
			#msg = Message("successfully registered",

				

				#sender="email@gmail.com",

				#recipients=[email])
			#msg.body = "Hello "

			#mail.send(msg)
			
			signup=register(userid=form.userid.data,username=form.username.data,password=generate_password_hash(form.password.data,method='sha256'),email=form.email.data,number=form.number.data)
			

			db.session.add(signup)
			db.session.commit()

		
		return redirect(url_for('login'))
	
	return render_template('signup.html',form=form)



@app.route('/users')

def users():
	details= register.query.all()

	
	return render_template("users.html",user=details)





@app.route('/blogs1')

def blogs1():
	result= blogs.query.all()

	
	return render_template("blogs1.html",user=result)

@app.route('/detail_page/<id>')
def detail_page(id):

	details= register.query.filter_by(id=id).first()

	
	return render_template("detail_page.html",result=details)




@app.route("/delete/<id>")
def delete(id):
	
	details= register.query.filter_by(id=id).first()

	db.session.delete(details)
	db.session.commit()
	return redirect(url_for("users"))



@app.route("/deleteblog")
def deleteblog():
	if current_user.is_authenticated:
		
		
		result=blogs.query.all()

		if result:

			return render_template("deleteblog.html",user=result)

		return f"user  Does not created any blog"

	return redirect(url_for("login"))		

@app.route("/delete_blog")
def delete_blog():

	details = blogs.query.filter_by(email=current_user.email).first()
	if details:

		db.session.delete(details)
		db.session.commit()
		return redirect(url_for("blogs1"))
	return redirect(url_for("deleteblog"))

@app.route('/booking',methods=["POST","GET"])
def booking():
	user=flask_login.current_user
	if not session.get("user") is None:
		if request.method == "POST":
			details = blogs.query.filter_by(email=current_user.email).first()
			if details:
				email=request.form["email"]
				username=request.form["name"]

				
				source=request.form["source"]
				destination=request.form["dest"]
				s_date=request.form["s_date"]
				e_date=request.form["e_date"]
				adults=request.form["adults"]
				children=request.form["children"]

				user1 = booking(username = username,email=email,source=source,destination=destination,s_date=s_date,e_date=e_date,adults=adults,children=children)
				db.session.add(user1)
				db.session.commit()

				return redirect(url_for("home"))

		details = register.query.filter_by(email=current_user.email).first()
		return render_template('booking.html',user=details)

	return redirect(url_for("login"))

@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

if __name__ == "__main__":
	create_app()
	db.create_all()
	app.run(debug= True)
