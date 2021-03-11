from flask import Flask,render_template,url_for,redirect,request,session

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

app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///travel.db")

db = SQLAlchemy(app)



class MyForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userid = IntegerField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    email = StringField('Email Address', [validators.Length(min=6, max=35)])

    number = IntegerField('Number', validators=[DataRequired()])




class MyForm_blog(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    userid = IntegerField('userid', validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired()])

    image= FileField(validators=[FileRequired()])

    description= StringField('description', validators=[DataRequired()])



class register(db.Model):

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
	image= db.Column(db.String(30))
	date= db.Column(db.DateTime, nullable=False )
	title=db.Column(db.String(20))
	text=db.Column(db.Text(100),  nullable=False)
	
	def __init__(self,username , image,date,title,text,userid):
		
		self.userid=userid
		self.username = username
		self.image = image
		self.date= date
		self.title = title
		self.text = text
date=date.today()

class booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(30), unique=True, nullable=False)
	source=db.Column(db.String(30),  nullable=False)
	destination=db.Column(db.String(30),  nullable=False)
	s_date=db.Column(db.Integer)

	e_date=db.Column(db.Integer)
	adults=db.Column(db.Integer)
	children=db.Column(db.Integer)

	def __init__(self,id,username , password,source,destination,s_date,e_date,adults,children):
		self.id = id
		self.username = username
		self.password = password
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


@app.route('/blog')
def blog():



	return render_template('blog.html')

@app.route('/addblog/<user>',methods=["POST", "GET"])
def addblog(user):

	form = MyForm_blog()
	

	if request.method == "POST":

	

		addblogs = blogs (userid=form.userid.data,username=form.username.data,image=form.image.data,date=date,title=form.title.data,text=form.description.data)
		
		print(request.form)


		db.session.add(addblogs)
		db.session.commit()

		userid1=request.form["userid"]

		return redirect(url_for("blogs1",result=userid1))
	

	result1=register.query.filter_by(userid=user).first()

	return render_template("addblog.html",result=result1,form=form)


@app.route('/login/<int:user>/update',methods = ['GET','POST'])
def update(user):

	details = blogs.query.filter_by(userid=user).first()

	if request.method == 'POST':
		if details:
			db.session.delete(details)
			db.session.commit()
 
			userid=request.form["userid1"]
			name=request.form["name"]
			title=request.form["title"]
			image=request.form["img"]
			text=request.form["text"]
			
			details= blogs(username=name,userid=userid,title=title,image=image,text=text,date=date)
			db.session.add(details)
			db.session.commit()
			
			return redirect(url_for("blogs1"))

		return f"user with id = {user} Does not exist"
 
	return render_template('updateblogs.html', result = details)


@app.route('/contact')
def contact():
	return render_template('contact.html')


@app.route('/page')
def page():
	return render_template('page.html')



@app.route('/login',methods=["POST", "GET"])
def login():

	if request.method == "POST":
		user=request.form["Uname"]
		
		session['user1']=user

		user1=request.form["Password"]
		
		login=register.query.filter_by(userid=user,password=user1).first()
		if login is not None:
			return redirect(url_for("addblog",user=user))
		
		#return redirect(url_for("user", user=user))
		
	return render_template('login.html')


#@app.route("/user")*
#def user():
#	if "user" in session:
#		user=session["user"]

#		return f"<h1>{user}</h1>"

#	else:
#		return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.clear()
	#session.pop("user",None)
	return redirect(url_for("login"))

	

@app.route('/signup',methods=["POST","GET"])
def signup():
	
	form = MyForm()
	
	if request.method == "POST":
		if form.validate_on_submit(): 
			
			email=form.email.data
			print(email)
			#msg = Message("successfully registered",

				#sender="gamil@gmail.com",

				#recipients=[email])
			#msg.body = "Hello "

			#mail.send(msg)
			
			signup=register(userid=form.userid.data,username=form.username.data,password=form.password.data,email=form.email.data,number=form.number.data)
			

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


@app.route("/deleteblog/<userid>")
def deleteblog(userid):
	
	details= blogs.query.filter_by(userid=userid).first()
	if employee:
		db.session.delete(details)
		db.session.commit()
		return redirect(url_for("blogs1"))

	return redirect(url_for("home"))




@app.route('/booking',methods=["POST","GET"])
def booking():
	if request.method == "POST":

		name=request.form["username"]

		password=request.form["Password"]
		source=request.form["source"]
		destination=request.form["dest"]
		s_date=request.form["s_date"]
		e_date=request.form["e_date"]
		adults=request.form["adults"]
		children=request.form["children"]
		user1 = booking(username=username,password=password,source=source,destination=destination,s_date=s_date,e_date=e_date,adults=adults,children=children,id=id)
		db.session.add(user)
		db.session.commit()
		return render_template('booking.html')



@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

if __name__ == "__main__":

	db.create_all()
	app.run(debug= True)