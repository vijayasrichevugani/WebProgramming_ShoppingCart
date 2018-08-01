import os
import sqlite3
from flask import *
from flask_sqlalchemy import *
from datetime import datetime


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__='users'
	userId = db.Column(db.Integer,primary_key=True)
	password = db.Column(db.String(255))
	email = db.Column(db.String(255))
	name = db.Column(db.String(255))
	address = db.Column(db.String(255))
	state = db.Column(db.String(255))
	phone = db.Column(db.String(255))

db.create_all()


@app.route("/register",methods = ['GET','POST'])
def register():
	if request.method =='POST':
		password = request.form['password']
		email = request.form['email']
		name = request.form['name']
		address = request.form['address']
		state = request.form['state']
		phone = request.form['phone']
		try:
			user = Users(password=password,email=email,name=name,address=address,state=state,phone=phone)
			db.session.add(user)
			db.session.commit()
			msg="registered successfully"
		except:
			db.session.rollback()
			msg="error occured"
	db.session.close()
	return render_template("login.html",error=msg)

@app.route("/loginForm")
def loginForm():
        return render_template('login.html', error='')


@app.route('/')
def layout():	
	return render_template("layout.html")

@app.route('/show_books')
def books ():	
	return render_template("show_books.html")

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return render_template('show_books.html')
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

def is_valid(email,password):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False

@app.route("/logout")
def logout():
        return render_template('login.html', error='')

@app.route("/cart/<tsum>/<int:sss>")
def addcart(tsum,sss):
	global x,p
	x=tsum
	p=sss
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	else:
		stmt = "SELECT name FROM users WHERE email = '" + session['email'] + "'"
		name=db.engine.execute(stmt).fetchone()[0]
		stmt = "SELECT address FROM users WHERE email = '" + session['email'] + "'"
		address=db.engine.execute(stmt).fetchone()[0]
		stmt = "SELECT state FROM users WHERE email = '" + session['email'] + "'"
		state=db.engine.execute(stmt).fetchone()[0]
		stmt = "SELECT phone FROM users WHERE email = '" + session['email'] + "'"
		phone=db.engine.execute(stmt).fetchone()[0]
	return render_template('viewcart.html',name=name,address=address,state=state,phone=phone,tsum=tsum,sss=sss)
x=0
p=0
@app.route("/payment")
def payment():
	stmt = "SELECT userId FROM users WHERE email = '" + session['email'] + "'"
	userId = db.engine.execute(stmt).fetchone()[0]
	stmt = "SELECT name FROM users WHERE email = '" + session['email'] + "'"
	name=db.engine.execute(stmt).fetchone()[0]
	stmt = "SELECT address FROM users WHERE email = '" + session['email'] + "'"
	address=db.engine.execute(stmt).fetchone()[0]
	stmt = "SELECT state FROM users WHERE email = '" + session['email'] + "'"
	state=db.engine.execute(stmt).fetchone()[0]
	stmt = "SELECT phone FROM users WHERE email = '" + session['email'] + "'"
	phone=db.engine.execute(stmt).fetchone()[0]
	return render_template('payment.html', userId=userId,name=name,address=address,state=state,phone=phone,p=p,x=x)


if __name__ =='__main__':
	
	app.run(port=5001)