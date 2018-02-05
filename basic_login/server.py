from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
# imports the Bcrypt module
from flask_bcrypt import Bcrypt
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app, 'basic_login')
# Basic Login page
@app.route('/')
def index():
 return render_template('index.html')
#This route brings you to the form to create a new user
@app.route('/newuser')
def newuser():
    return render_template('create_user.html')
# This round creates the new user.
@app.route('/create_user', methods=['POST'])
def create_user():
    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    # run validations and if they are successful we can create the password hash with bcrypt
    pw_hash = bcrypt.generate_password_hash(password)
    # now we insert the new user into the database
    insert_query = "INSERT INTO users (first_name, last_name, email, pw_hash, created_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW())"
    query_data = {
        'first_name': fname,
        'last_name': lname, 
        'email': email,
        'pw_hash': pw_hash 
    }
    mysql.query_db(insert_query, query_data)
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = { 'email': email }
    user = []
    user = mysql.query_db(user_query, query_data) # user will be returned in a list
    if not user:
        flash('The email address you entered is not in our records! Here create an account!')
        return redirect('/newuser')
    if bcrypt.check_password_hash(user[0]['pw_hash'], password):
        session['first_name'] = user[0]['first_name']
        session['last_name'] = user[0]['last_name']
        session['email'] = user[0]['email']
        session['birthday'] = user[0]['created_at']
        return render_template('logged_in.html')
    else:
        flash('The password you entered did not match our records!')
        redirect('/')
  # set flash error message and redirect to login page
app.run(debug=True)