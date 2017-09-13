from flask import Flask, request, redirect, render_template, session, flash
import re
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'emailDB')
app.secret_key = "ThisIsSecret!"
# an example of running a query

print("***************** Emails *******************")
print mysql.query_db("SELECT * FROM emails")
# print("****************** USERS ******************")
# print mysql.query_db("SELECT * FROM users")

@app.route('/')
def index():

    query = "SELECT * FROM emails"
    emails = mysql.query_db(query)
    return render_template('index.html', all_emails=emails)



@app.route('/success', methods=['POST'])
def success():
    # if len(request.form['email']) < 1:
    #     flash("Email cannot be blank!")
    # elif not EMAIL_REGEX.match(request.form['email']):
    #     flash("Invalid Email Address!")
    # else:
    #select email from emails where email = 'fake1@fake.com'
    query = "SELECT * from emails where email = :email"
    query2 = "SELECT * from emails"
    # query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    # We'll then create a dictionary of data from the POST data received.
    email =  request.form['email']
    data = {
             'email': request.form['email']
           }
    value = mysql.query_db(query, data)
    if len(value)==0:
        valid = False
        return redirect('/')
    else: valid = True
    value = mysql.query_db(query2, data)

    return render_template('index.html', valid=valid, all_emails=value, email = email)
#
#
# @app.route('/fake')
# def success():
#     query = "SELECT * FROM emails"
#     emails = mysql.query_db(query)
#     return render_template('index.html', all_emails=emails)



# Say we wanted to update a specific record, we could create another page and add a form that would submit to the following route:
# @app.route('/update_age', methods=['POST'])
# def update():
#     query = "UPDATE emails SET age = :age WHERE id = :id"
#     data = {
#              'age': request.form['age2'],
#              'id': request.form['user_id2']
#            }
#     mysql.query_db(query, data)
#     return redirect('/')
#
# @app.route('/delete_users', methods=['POST'])
# def delete():
#     query = "DELETE FROM email WHERE id = :id"
#     data = {'id': request.form['user_id']}
#     mysql.query_db(query, data)
#     return redirect('/')
#



app.run(debug=True)
