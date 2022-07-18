""" read from a SQLite database and return data to templates """

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jklm'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type

class Selections(db.Model):
    __tablename__ = 'selections'
    id = db.Column(db.Integer, primary_key=True)
    supplement = db.Column(db.String(100), nullable=False)
    amount_in_mcg = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    infant_age = db.Column(db.Integer)
    age = db.Column(db.Integer, nullable=False)
    maternity = db.Column(db.String(3), nullable=False)

db.create_all()


#routes

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form.get('user name')
        password = request.form.get('password')
        gender = request.form.get('gender')
        infant_age = request.form.get('infant age')
        age = request.form.get('age')
        maternity = request.form.get('maternity')

        user=User.query.filter_by(user_name=user_name).first()
        if user:
            flash('User name already exists.', category='error')
        elif user_name == "":
            flash('User name must be at least one character.', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', category='error')
        elif age.isdigit() is False:
            flash('Please enter only integers.', category='error')
        else:
            new_user = User(user_name=user_name, password=password, gender=gender, infant_age=infant_age, age=age, maternity=maternity)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            
    return render_template("sign_up.html")

@app.route('/', methods=['GET', 'POST'])
def add_selection():
    if request.method == 'POST':
        id = request.form.get('id')
        supplement = request.form.get('supplement')
        amount_in_mcg = request.form.get('amount in mcg')

        if amount_in_mcg.isdigit() is False:
            flash('Please enter only integers.', category='error')
        else:
            selection = Selections(id=id, supplement=supplement, amount_in_mcg=amount_in_mcg)
            db.session.add(selection)
            db.session.commit()
    return render_template('home.html')


@app.route('/results')
def table_selections():
    selections = Selections.query.all()
    return render_template('results.html', selections=selections)

   
if __name__ == '__main__':
    app.run(debug=True)
