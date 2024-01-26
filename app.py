import pandas 
import sys 
from datetime import date
import time
import memory_profiler 
from memory_profiler import profile 
import pyarrow 
import pyarrow.parquet
from jugaad_data.nse import bhavcopy_save, bhavcopy_fo_save
import matplotlib.pyplot as graph
import os 
from jugaad_data.nse import stock_df
import csv
























from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('welcome.html', username=session['username'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))



####################################################################################
#####################################################################################################
####################################################################################












@app.route('/stocks')
def stocks():
    return render_template('stocks.html')




@app.route('/write_from_csv',methods=['POST'])
def write_from_csv():
     start_year = request.form['start_year']
     start_month = request.form['start_month']
     start_date = request.form['start_date']
     to_year = request.form['to_year']
     to_month = request.form['to_month']
     to_date = request.form['to_date']
     sym=request.form['sym']
     
     executable(start_date,start_month,start_year,to_date,to_month,to_year,sym)
     with open('stock_file.csv', newline='', encoding='utf-8') as csvfile:
     	reader = csv.DictReader(csvfile)
     	data = list(reader)

     return render_template('table.html', data=data)
	
	
	
	
def executable(start_date,start_month,start_year,to_date,to_month,to_year,sym):
     start_date=int(start_date)
     start_month=int(start_month)
     start_year=int(start_year)
     to_year=int(to_year)
     to_month=int(to_month)
     to_date=int(to_date)	
     df = stock_df(symbol=sym, from_date=date(start_year,start_month,start_date),
            to_date=date(to_year,to_month,to_date), series="EQ")
     file_path_csv = 'stock_file.csv'
     df.to_csv(file_path_csv, index=False)






















if __name__ == '__main__':
    app.run(debug=True)
