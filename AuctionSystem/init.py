from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask import Flask, send_from_directory, render_template, redirect, url_for, request, json, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import re
import mysql.connector
import time
from datetime import datetime
from models.User import *
import os
# import utils

#Initialize the app from Flask
app = Flask(__name__)


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

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

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

	ins = "INSERT INTO Customer(customerEmail, customerName, customerPassword, balance) VALUES(\'{}\', \'{}\', \'{}\', 0)"
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
	# get_image_paths(data1)

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
	# if current_user.is_authenticated:
	# 	data1 = mainSquareSupport()
	# 	error = None
	# 	return render_template('mainSquare.html', posts=data1, error = error)
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Customer WHERE customerName = \'{}\' and customerPassword = \'{}\'"
	cursor.execute(query.format(username, password))
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		# login_user(user)
		session['username'] = username
		session['role'] = "Customer"

		data1 = mainSquareSupport()
		return render_template('mainSquare.html', posts=data1, error = error)

	else:
		#returns an error message to the html page
		error = 'Invalid username or password'
		return render_template('login.html', error=error)
	# error = 'Invalid username or password'
	# return render_template('mainSquare.html', error=error)

@app.route('/admin_login', methods=['POST'])
def Admin_login():
	username = request.form['username']
	password = request.form['password']
	cursor = conn.cursor()
	query = "SELECT * FROM Admin WHERE adminName = \'{}\' and adminPassword = \'{}\'"
	cursor.execute(query.format(username, password))
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		# login_user(username)
		# print(username)
		session['username'] = username
		session['role'] = "Admin"
		data1 = viewVerifySupport()
		return render_template('adminMain.html', type = "verify", name = username, data = data1)
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
	owner = session["username"]
	itemName = request.form["itemName"]
	price = request.form["itemPrice"]
	itemDescription = request.form["itemDescription"]
	print(price)
	print("!!!!!!!!!!!!!!!!")
	cursor = conn.cursor()
	file = open("./Queries/postItem.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(owner, itemName, itemDescription, price))
	conn.commit()
	cursor.close()

	cursor = conn.cursor()
	file = open("./Queries/productID.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(owner, itemName, itemDescription, price))
	result = cursor.fetchall()

	print(result)
	cursor.close()

	filename = str(result[len(result)-1][0])
	print(filename)
	image = request.files['image']
	image.save(os.path.join("./static/images", filename))


	error = "Item posted!"
	data1 = mainSquareSupport()
	return render_template('mainSquare.html', posts=data1, error = error)

def productInfo(productID):
	cursor = conn.cursor()
	file = open("./Queries/currentPrice.sql","r")
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
	data1 = productInfo(productID)
	error = None
	return render_template('product.html', posts=data1, error = error)

#----------------------Bid------------------------------------------


@app.route('/Bid', methods = ["GET", "POST"])
# @login_required
def bid():
	productID = request.form["productID"]
	new_price = request.form["new_price"]
	username=session["username"]

	cursor = conn.cursor()
	file = open("./Queries/checkProductStatus.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	status = cursor.fetchall()
	cursor.close()
	if status[0][0] != "verified":
		error = "This bidding is closed now!"
	else:
		# username = current_user.id
		cursor = conn.cursor()
		file = open("./Queries/bid.sql","r")
		query = file.read()
		file.close()
		cursor.execute(query.format(new_price, username, productID))
		conn.commit()
		cursor.close()
		error = "Bidding successfully!"


	data1 = productInfo(productID)
	# print(data1)
	# print("!!!!!!!!!!!!!!!!!")
	return render_template('product.html', posts=data1, error = error)


#----------------------Bid------------------------------------------




@app.route('/refreshPrice', methods = ["GET", "POST"])
# @login_required
def refresh():
	# with app.app_context():
	productID = request.form["productID"]
	# print(type(productID))
		# scheduler.resume()
	data1 = productInfo(productID)
	error = None
	# print(data1)
	# print('Tick! The time is: %s' % datetime.now())
	# scheduler.pause()
	return render_template('product.html', posts=data1, error = error)



@app.route('/myProduct', methods = ["GET"])
# @login_required
def myProduct():
	# username = current_user.id
	username=session["username"]
	cursor = conn.cursor()
	file = open("./Queries/myProduct.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('profile.html', posts=data1, error = error, type = "product")

def myTransactionSupport(username):
	cursor = conn.cursor()
	file = open("./Queries/myTransaction.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	data1 = cursor.fetchall()
	cursor.close()
	return data1



@app.route('/myTransaction', methods = ["GET"])
# @login_required
def myTransaction():
	# username = current_user.id
	username=session["username"]
	data1 = myTransactionSupport(username)
	error = None
	return render_template('profile.html', posts=data1, error = error, type = "transaction")


@app.route('/myProfile', methods = ["GET"])
# @login_required
def myProfile():
	# username = current_user.id
	username=session["username"]
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
	username=session["username"]
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

@app.route('/pay', methods = ["GET", "POST"])
# @login_required
def pay():
	transID = request.form["TransactionID"]
	##########
	username=session["username"]
	cursor = conn.cursor()
	file = open("./Queries/checkBalance.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(username))
	balance = cursor.fetchall()
	cursor.close()

	username=session["username"]
	cursor = conn.cursor()
	file = open("./Queries/checkPrice.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(transID))
	price = cursor.fetchall()
	cursor.close()

	if balance[0][0] >= price[0][0]:
		cursor = conn.cursor()
		file = open("./Queries/pay.sql","r")
		query = file.read()
		file.close()
		cursor.execute(query.format(price[0][0], username))
		conn.commit()

		cursor = conn.cursor()
		file = open("./Queries/updateTransactionStatus.sql","r")
		query = file.read()
		file.close()
		new_status = "paid"
		cursor.execute(query.format(new_status, transID))
		conn.commit()

		error = "Paid!"
	else:
		error = "Please recharge!"
	data1 = myTransactionSupport(username)
	return render_template('profile.html', posts=data1, error = error, type = "transaction")



@app.route('/adminProductV/<int:productID>', methods = ["GET", "POST"])
# @login_required
def adminProductV(productID):
	cursor = conn.cursor()
	file = open("./Queries/unverifiedProductInfo.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	data1 = cursor.fetchall()
	cursor.close()
	error = None
	return render_template('adminProduct.html', posts=data1, error = error, type="verify")

@app.route('/adminProductB/<int:productID>', methods = ["GET", "POST"])
# @login_required
def adminProductB(productID):
	data1 = productInfo(productID)
	error = None
	return render_template('adminProduct.html', posts=data1, error = error, type="bidding")


def viewVerifySupport():
	cursor = conn.cursor()
	file = open("./Queries/itemsToBeVerified.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format())
	data1 = cursor.fetchall()
	cursor.close()
	return data1

@app.route('/viewVerify', methods = ["GET", "POST"])
# @login_required
def viewVerify():
	data1 = viewVerifySupport()
	error = None
	return render_template('adminMain.html', posts=data1, error = error, type="verify")


def viewEndBiddingSupport():
	cursor = conn.cursor()
	file = open("./Queries/mainSquare.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format())
	data1 = cursor.fetchall()
	cursor.close()
	return data1

@app.route('/viewEndBidding', methods = ["GET", "POST"])
# @login_required
def viewEndBidding():
	data1 = viewEndBiddingSupport()
	error = None
	return render_template('adminMain.html', posts=data1, error = error, type = "bidding")



@app.route('/verify', methods = ["GET", "POST"])
# @login_required
def verify():
	########if verified
	verify = request.form["new_status"]
	if verify == "true":
		new_status = "verified"
	else:
		new_status = "rejected"
	productID = request.form["productID"]

	cursor = conn.cursor()
	file = open("./Queries/checkProductStatus.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	currentStatus = cursor.fetchall()
	#print(currentStatus)
	cursor.close()
	if currentStatus[0][0] != "to_be_verified":
		error = "This product has already been verified"
		data1 = viewVerifySupport()
		error = "This item has already been verified!"
		return render_template('adminMain.html', posts=data1, error = error, type = "verify")
	else:
		cursor = conn.cursor()
		file = open("./Queries/updateProductStatus.sql","r")
		query = file.read()
		file.close()
		cursor.execute(query.format(new_status, productID))
		conn.commit()

		if new_status == "verified":

			file = open("./Queries/startPrice.sql","r")
			query = file.read()
			file.close()
			cursor.execute(query.format(productID))
			startPrice = cursor.fetchall()

			file = open("./Queries/startBidding.sql","r")
			query = file.read()
			file.close()
			cursor.execute(query.format(productID, startPrice[0][0]))
			conn.commit()
			cursor.close()

		data1 = viewVerifySupport()
		error = "The verify status of the product is " + new_status + "."
		return render_template('adminMain.html', posts=data1, error = error, type = "verify")


def create_new_transaction(productID, buyer, price):
	cursor = conn.cursor()
	file = open("./Queries/newTransaction.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID, buyer, price))
	conn.commit()
	cursor.close()




@app.route('/endBidding', methods = ["GET", "POST"])
# @login_required
def endBidding():
	productID = request.form["productID"]

	cursor = conn.cursor()
	file = open("./Queries/endBidding.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	conn.commit()
	cursor.close()

	cursor = conn.cursor()
	file = open("./Queries/checkBuyer.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(productID))
	buyer_and_price = cursor.fetchall()
	print(buyer_and_price)

	if buyer_and_price[0][0] == "NULL":
		new_status = "not_sold"
	else:
		new_status = "sold"
		create_new_transaction(productID, buyer_and_price[0][0], buyer_and_price[0][1])
		# pay(TransactionID)

	cursor = conn.cursor()
	file = open("./Queries/updateProductStatus.sql","r")
	query = file.read()
	file.close()
	cursor.execute(query.format(new_status, productID))
	conn.commit()
	cursor.close()
	#
	# file = open("./Queries/verify.sql","r")
	# query = file.read()
	# file.close()
	# cursor.execute(query.format(productID, new_status))
	# conn.commit()
	# cursor.close()





	data1 = viewEndBiddingSupport()
	error = "This auction has been ended"
	return render_template('adminMain.html', posts=data1, error = error, type = "bidding")

#-------------------------------------------------------------------------
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	# scheduler = BlockingScheduler()
	# scheduler.add_job(refresh, 'interval', seconds = 3)
	# print('Press Ctrl+{0} to exit'.format('Break'
	#    if os.name == 'nt'
	#    else 'C'))
	app.run('127.0.0.1', 5000, debug = True)
