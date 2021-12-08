from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import re
import mysql.connector
import time
from datetime import datetime
from models.User import *
# from flask_apscheduler import APScheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
# import os

# aps = APScheduler()
# class Config(object):
#     JOBS = [
#         {
#             'id': 'job1',
#             'func': 'scheduler:task',
#             'args': (1, 2),
#             'trigger': 'interval',
#             'seconds': 3
#         }
#     ]
#     SCHEDULER_API_ENABLED = True
#
#
# def task(a, b):
#     print(str(datetime.datetime.now()) + ' execute task ' + '{}+{}={}'.format(a, b, a + b))
#
#
user1 = User("user1", "User1")
user2 = User("user2", "User2")
user3 = User("user3", "User3")

all_users = {}
all_users["user1"] = user1
all_users["user2"] = user2
all_users["user3"] = user3

#Initialize the app from Flask
app = Flask(__name__)
# app.config.from_object(Config())
# scheduler = APScheduler()
# scheduler.init_app(app)
# scheduler.start()


#Configure MySQL
conn = mysql.connector.connect(host='localhost',
					port='8889',
					user='root',
					password='root',
					database='Auction')



login = LoginManager(app)
login.login_view = 'login' # force user to login
login.login_message = "Please login first"

@login.unauthorized_handler
def unauthorized_callback():
       return redirect(url_for('login'))

@login.user_loader
def load_user(username):
    if username in all_users:
        return all_users[username]
    return None


@app.route('/')
def hello():
 return render_template('login.html')

#Define route for login
@app.route('/login')
def login():
 return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
 return render_template('register.html')

@app.route('/post')
def post():
 return render_template('post.html')

@app.route('/profile')
def profile():
 return render_template('profile.html')

# @app.route('/logout')
# def logout():
# 	logout_user(current_user)
# 	return redirect('/login.html')


#----------------------register------------------------------------------

@app.route('/cus_register', methods=['GET', 'POST'])
def cus_register():
	email = request.form['email']
	name = request.form['username']
	password = request.form['password']

	cursor = conn.cursor()
	query = "SELECT * FROM Customer WHERE customerEmail = \'{}\'"
	cursor.execute(query.format(email, name))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This email already exists"
		return render_template('register.html', error = error)
	else:
		cursor = conn.cursor()
		query = "SELECT * FROM Customer WHERE customerName = \'{}\'"
		cursor.execute(query.format(email, name))
		data = cursor.fetchone()
		cursor.close()
		if(data):
			#If the previous query returns data, then user exists
			error = "This username already exists"
			return render_template('register.html', error = error)

	ins = "INSERT INTO Customer(customerEmail, customerName, customerPassword) VALUES(\'{}\', \'{}\', \'{}\')"
	cursor = conn.cursor()
	cursor.execute(ins.format(email, name, password))
	conn.commit()
	cursor.close()
	flash("You are registered")
	return render_template('login.html', error= "Welcome! Please login~")


def mainSquareSupport():
	cursor = conn.cursor()
	file = open("./Queries/mainSquare.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format())
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	print(data1)
	return data1


@app.route('/MainSquare', methods = ["GET", "POST"])
# @login_required
def MainSquare():
	data1 = mainSquareSupport()
	error = None
	return render_template('mainSquare.html', posts=data1, error = error)

#------------------------------------login----------------------------------------

@app.route('/cus_login', methods=['POST', 'GET'])
def cus_login():
	if current_user.is_authenticated:
		data1 = mainSquareSupport()
		error = None
		return render_template('mainSquare.html', posts=data1, error = error)
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Customer WHERE customerName = \'{}\' and customerPassword = \'{}\'"
	cursor.execute(query.format(username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		user = User(username)
		login_user(user)
		data1 = mainSquareSupport()
		return render_template('mainSquare.html', posts=data1, error = error)

	else:
		#returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)
	# error = 'Invalid username or password'
	# return render_template('mainSquare.html', error=error)

@app.route('/Admin_login', methods=['POST'])
def Admin_login():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Admin WHERE adminName = \'{}\' and adminPassword = \'{}\'"
	cursor.execute(query.format(username, password, booking_agent_id))
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		login_user(username)
		print(username)
		return render_template('mainSquare.html', type = "admin", name = username)
	else:
		#returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)







# #--------------------------customer-------------------------------------------

@app.route('/cus_search', methods = ["GET", "POST"])
# @login_required
def cus_search():
	keyword = request.form["keyword"]
	cursor = conn.cursor()
	file = open("./Queries/cusSearch.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(keyword))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('mainSquare.html', posts=data1, type=keyword)



@app.route('/post_item', methods = ["GET", "POST"])
# @login_required
def post_item():
	# f = request.files['itemPicture']
	# f.save()
	#f.save(secure_filename(f.filename))
	owner = "user2"
	itemName = request.form["itemName"]
	price = request.form["itemPrice"]
	itemDescription = request.form["itemDescription"]
	auctionTime = "2020-01-01"
	print(price)
	print("!!!!!!!!!!!!!!!!")
	cursor = conn.cursor()
	file = open("./Queries/postItem.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(owner, itemName, itemDescription, price, auctionTime))
	conn.commit()
	cursor.close()
	error = "Item posted!"
	data1 = mainSquareSupport()
	return render_template('mainSquare.html', posts=data1, error = error)

def productInfo(productID):
	cursor = conn.cursor()
	file = open("./Queries/productInfo.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	data1 = cursor.fetchall()
	cursor.close()
	return data1


@app.route('/product/<int:productID>', methods = ["GET", "POST"])
# @login_required
def Product(productID):
	# productID = request.form["productID"]
	# scheduler.add_job(refresh, 'interval', seconds = 3)
	data1 = productInfo(productID)
	error = None
	return render_template('product.html', posts=data1, error = error)

#----------------------Bid------------------------------------------


@app.route('/Bid', methods = ["GET", "POST"])
# @login_required
def bid():
	productID = request.form["productID"]
	new_price = request.form["new_price"]
	# username = current_user.id
	username="user1"
	cursor = conn.cursor()
	file = open("./Queries/bid.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(new_price, username, productID))
	conn.commit()
	cursor.close()

	cursor = conn.cursor()
	file = open("./Queries/currentPrice.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	data1 = cursor.fetchall()
	cursor.close()
	# print(data1)
	# print("!!!!!!!!!!!!!!!!!")
	error = "Bidding successfully!"
	return render_template('product.html', posts=data1, error = error)


#----------------------Bid------------------------------------------




@app.route('/refreshPrice', methods = ["GET", "POST"])
# @login_required
def refresh():
	productID = request.form["productID"]
	cursor = conn.cursor()
	file = open("./Queries/currentPrice.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(new_price, username, productID))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	# print('Tick! The time is: %s' % datetime.now())
	return render_template('product.html', posts=data1, error = error)



@app.route('/myProduct', methods = ["GET"])
# @login_required
def myProduct():
	# username = current_user.id
	username="user1"
	cursor = conn.cursor()
	file = open("./Queries/myProduct.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('profile.html', posts=data1, error = error, type = "product")



@app.route('/myTransaction', methods = ["GET"])
# @login_required
def myTransaction():
	# username = current_user.id
	username="user1"
	cursor = conn.cursor()
	file = open("./Queries/myTransaction.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('profile.html', posts=data1, error = error, type = "transaction")


@app.route('/myProfile', methods = ["GET"])
# @login_required
def myProfile():
	# username = current_user.id
	username="user1"
	cursor = conn.cursor()
	file = open("./Queries/myProfile.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('profile.html', posts=data1, error = error, type = "profile")

@app.route('/recharge', methods = ["GET", "POST"])
# @login_required
def recharge():
	# username = current_user.id
	username="user1"
	amount = request.form["amount"]

	cursor = conn.cursor()
	file = open("./Queries/recharge.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(amount, username))
	conn.commit()
	cursor.close()

	cursor = conn.cursor()
	file = open("./Queries/myProfile.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	error = "Successfully recharged"
	return render_template('profile.html', posts=data1, error = error, type = "profile")



# @app.route('/verify', methods = ["GET"])
# @login_required
# def verify():
# 	########if verified
# 	new_status = request.form["new_status"]
# 	productID = request.form["productID"]


# 	cursor = conn.cursor()
# 	file = open("./Queries/checkProductStatus.sql","r")
# 	query = file.read()
# 	file.close()
# 	cursor.execute(query.format(productID))
# 	currentStatus = cursor.fetchall()
# 	#print(currentStatus)
# 	cursor.close()
# 	if currentStatus != "to_be_verified":
# 		error = "this product has already been verified"
# 		MainSquare()
# 	else:
# 		cursor = conn.cursor()
# 		file = open("./Queries/verify.sql","r")
# 		query = file.read()
# 		file.close()
# 		cursor.execute(query.format(new_status, productID))
# 		data1 = cursor.fetchall()
# 		conn.commit()

# 		file = open("./Queries/startPrice.sql","r")
# 		query = file.read()
# 		file.close()
# 		cursor.execute(query.format(productID))
# 		startPrice= cursor.fetchall()

# 		file = open("./Queries/startBidding.sql","r")
# 		query = file.read()
# 		file.close()
# 		cursor.execute(query.format(productID, startPrice))
# 		data1 = cursor.fetchall()
# 		cursor.close()

# 		return render_template('profile.html', posts=data1, error = error)


# @app.route('/endBidding', methods = ["GET"])
# @login_required
# def endBidding():
# 	########if verified
# 	productID = request.form["productID"]
# 	cursor = conn.cursor()
# 	file = open("./Queries/endBidding.sql","r")
# 	query = file.read()
# 	file.close()
# 	cursor.execute(query.format(productID))
# 	data1 = cursor.fetchall()
# 	conn.commit()
# 	cursor.close()
# 	MainSquare()

# def tick():
   # print('Tick! The time is: %s' % datetime.now())


# cannot be for your own product
#-------------------------------------------------------------------------
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	# scheduler = BlockingScheduler()
	# # scheduler.add_job(refresh, 'interval', seconds = 3)
	# print('Press Ctrl+{0} to exit'.format('Break'
	#    if os.name == 'nt'
	#    else 'C'))
	# try:
	# 	scheduler.start()
	# except (KeyboardInterrupt, SystemExit):
	# 	pass

	app.run('127.0.0.1', 5000, debug = True)
