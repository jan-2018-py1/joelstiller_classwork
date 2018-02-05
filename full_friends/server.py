from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'full_friends')
import re
app.secret_key = 'ThisIsSecret' # you need to set a secret key for security purposes
@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', friends = friends) # pass data to our template
@app.route('/friends', methods=['POST'])
def create():
    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
    if not EMAIL_REGEX.match(email):
        flash('Email is not valid!')  
        return redirect('/')
    elif len(fname) < 3 or len(lname) < 3:
        flash('First name and last name must be at least 3 characters')
        return redirect('/')
    else:
        query = "INSERT into friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, now(), now())"
        data = {
            'first_name': fname,
            'last_name': lname,
            'email': email
        }
        mysql.query_db(query, data)
        return redirect('/')
@app.route('/friends/<id_in>/edit')
def edit_page(id_in):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {"id":id_in}
    friend = mysql.query_db(query, data)
    return render_template('edit.html', one_friend=friend[0])
@app.route('/friends/<id_toupdate>', methods=["POST"])
def submit_update(id_toupdate):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :ident"
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'ident':id_toupdate
    }
    mysql.query_db(query,data)
    return redirect('/')
@app.route('/friends/<to_delete>/delete')
def delete(to_delete):
    query = "DELETE from friends WHERE id = :id"
    data = {'id': to_delete}
    mysql.query_db(query,data)
    return redirect('/')
app.run(debug=True)