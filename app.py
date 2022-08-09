from flask import Flask, render_template, request, flash, redirect, url_for, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
import csv

# Citation:
# Date: 08/08/2022
# Based on: How To Use the sqlite3 Module in Python 3
# Source URL: https://www.digitalocean.com/community/tutorials/how-to-use-the-sqlite3-module-in-python-3

# Citation: Line 27; Line 28
# Date: 08/08/2022
# Based on: Pandas – Remove special characters from column names
# Source URL: https://www.geeksforgeeks.org/pandas-remove-special-characters-from-column-names/

# Citation: Line 47
# Date: 08/08/2022
# Based on: Step 4: Database Connections
# Source URL: https://flask.palletsprojects.com/en/0.12.x/tutorial/dbcon/ 

# Citation:
# Date: 08/08/2022
# Based on: How To Use an SQLite Database in a Flask Application
# Source URL: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application

# Citation: Line 211
# Date: 08/08/2022
# Based on: flask.json jsonify Example Code
# Source URL: https://www.fullstackpython.com/flask-json-jsonify-examples.html

# Citation:
# Date: 08/08/2022
# Based on: Flask flash() method – How to Flash Messages in Flask?
# Source URL: https://www.askpython.com/python-modules/flask/flask-flash-method

# Configuration
app = Flask(__name__)
app.secret_key = 'jklm'

#Removes unwanted characters from csv file and generates a second csv file
def cleandata():
    df = pd.read_csv('C:/Users/user 1/CS361/website/out.csv', keep_default_na=False, header=None, encoding='cp1252')
    
    for col in df.columns:
        df[col] = df[col].apply(str).str.replace(r'\*', "", regex=True)
        df[col] = df[col].apply(str).str.replace('\u2013', "-", regex=True)
        
    df.to_csv('scrapeddata.csv', header=False)

cleandata()

#Connect to sqlite3 database
def connect_to_database():
    sql = sqlite3.connect('C:/Users/user 1/CS361/website/database.db')
    sql.row_factory = sqlite3.Row
    return sql

#Retrieve current contents of database
def get_database():
    if not hasattr(g, 'database_db'):
        g.database_db = connect_to_database()  
    return g.database_db

#Insert data from csv file into database
def import_csv():
    db = get_database()
    file = open('scrapeddata.csv')
    contents = csv.reader(file)
    db.executemany('insert into Temp(row_number, age_range, male, female, pregnancy, lactation) values (?, ?, ?, ?, ?, ?)', contents)
    db.execute('update Data set row_number = (select row_number from Temp where Temp.tempid = Data.dataid)')
    db.execute('update Data set age_range = (select age_range from Temp where Temp.tempid = Data.dataid)')
    db.execute('update Data set male = (select male from Temp where Temp.tempid = Data.dataid)')
    db.execute('update Data set female = (select female from Temp where Temp.tempid = Data.dataid)')
    db.execute('update Data set pregnancy = (select pregnancy from Temp where Temp.tempid = Data.dataid)')
    db.execute('update Data set lactation = (select lactation from Temp where Temp.tempid = Data.dataid)')
    db.commit()
    db.close() 

with app.app_context():
    import_csv()

#Route to Homepage
@app.route('/')
def index():
    return render_template("home.html") 

#Route to Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    db = get_database()
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user_cursor = db.execute('SELECT * from User where user_name = ?', [user_name])
        user = user_cursor.fetchone()

        if user:
            if check_password_hash(user['password'], password):
                return redirect(url_for('add_selection'))
            else:
                flash('Incorrect password. Try again.')
        else:
            flash('User does not exist. Try again.')
    return render_template("login.html") 

#Route to Sign Up Page
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        db = get_database()
        user_name = request.form['user_name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
    
        users = db.execute('SELECT * from User where user_name = ?', [user_name])
        user = users.fetchone()

        if user:
            flash('User name already exists. Please enter a different user name.')
        elif user_name == "":
            flash('User name must be at least one character.')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.')
        else:
            db.execute('INSERT into User (user_name, password) values (?, ?)', [user_name, hashed_password])
            db.commit()
            return redirect(url_for('login'))
    return render_template("sign_up.html")

#Route to Results Page
@app.route('/results')
def results():
    db = get_database()
    selections = db.execute('SELECT * from Selections')
    all_selections = selections.fetchall()
    return render_template('results.html', all_selections=all_selections) 

#Route to Add Supplement Page
@app.route('/add-supplement', methods=['GET', 'POST'])
def add_selection():
    if request.method == 'POST':
        supplement = request.form['supplement']
        amount_per_serving = request.form['amount per serving']
        unit = request.form['unit']
        percent_daily_value = request.form['percent daily value']

        if amount_per_serving is type(str):
            flash('Please enter only integers.')
        elif percent_daily_value.isdigit() is False:
            flash('Please enter only integers.')
        else:
            db = get_database()
            db.execute('INSERT into Selections (supplement, amount_per_serving, unit, percent_daily_value) values (?, ?, ?, ?)', 
            [supplement, amount_per_serving, unit, percent_daily_value])
            db.commit()
            return redirect(url_for('results'))
    return render_template('addsupplement.html')

#Route to Fetch Selection for Update Supplement Page
@app.route('/fetchselection/<int:selectid>')
def fetch_selection(selectid):
    db = get_database()
    selection = db.execute('SELECT * from Selections where selectid = ?', [selectid])
    single_selection = selection.fetchone()
    return render_template('updatesupplement.html', single_selection=single_selection)

#Route to Update Selection on Results Page    
@app.route('/updateselection', methods=['GET', 'POST'])
def update_selection():
    if request.method == 'POST':
        selectid = request.form['selectid']
        supplement = request.form['supplement']
        amount_per_serving = request.form['amount per serving']
        unit = request.form['unit']
        percent_daily_value = request.form['percent daily value'] 

        db = get_database()
        db.execute('UPDATE Selections set supplement = ?, amount_per_serving = ?, unit = ?, percent_daily_value = ? where selectid = ?',
        [supplement, amount_per_serving, unit, percent_daily_value, selectid])
        db.commit()
        return redirect(url_for('results'))
    return render_template('updatesupplement.html')

#Route to Delete Selection from Results Table
@app.route('/deleteselection/<int:selectid>', methods=['GET', 'POST'])
def delete_selection(selectid):
    if request.method == 'GET':
        db = get_database()
        db.execute('DELETE from Selections where selectid = ?', [selectid])
        db.commit()
        return redirect(url_for('results'))
    return render_template('addsupplement.html')

# Route to New Feature Page
@app.route('/newfeature')
def new_feature():
    db = get_database()
    all_data = db.execute('select * from Data')
    datalist = all_data.fetchall()
    return render_template('newfeature.html', datalist=datalist) 

#Route to Fetch Updated Data for New Feature Page if age range is selected
@app.route('/fetchdata', methods=['GET', 'POST'])
def fetchdata():
    db = get_database()
    if request.method == 'POST':
        query = request.form['selected']
        if query == '':
            all_data = db.execute('select * from Data')
            datalist = all_data.fetchall()
        else:
            search_text = request.form['selected']
            all_data = db.execute('SELECT * from Data where age_range = ?', [search_text])
            datalist = all_data.fetchall()
    return jsonify({'response': render_template('response.html', datalist=datalist)})

#Logout 
@app.route('/logout')
def logout():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
