from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'email_db')
import re
app.secret_key = 'ThisIsSecret' # you need to set a secret key for security purposes
@app.route('/')
def index():
    return render_template('index.html') # pass data to our template
@app.route('/validate', methods=['POST'])
def validate():
    email = request.form['email']
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
    if not EMAIL_REGEX.match(email):
        flash('Email is not valid!')  
        return redirect('/')
    else:
        query = "INSERT into emails (email, created_at, updated_at) VALUES (:email, now(), now())"
        data = {'email': email}
        mysql.query_db(query, data)
        session['entered'] = email
        return redirect('/success')
@app.route('/success')
def success():
    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', emails=emails, entered = session['entered'])
@app.route('/delete/<to_delete>')
def delete(to_delete):
    query = "DELETE from emails WHERE id = :id"
    data = {'id': to_delete}
    mysql.query_db(query,data)
    return redirect('/success')
app.run(debug=True)