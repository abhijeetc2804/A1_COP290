from datetime import date 
from datetime import datetime, timedelta
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
import plotly.express as pex
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key

'''
# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.static_folder = 'static'

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
    date_str=request.form['start_date']
    start_year,start_month,start_date=map(int,date_str.split('-'))
    #sym=request.form['sym']
    selected_companies=request.form.getlist('sym')
    date_str=request.form['to_date']
    to_year,to_month,to_date=map(int,date_str.split('-'))
  #  print(start_date,start_month,start_year)
  #  print(to_date,to_month,to_year)
    print(selected_companies)
   # executable(start_date,start_month,start_year,to_date,to_month,to_year,selected_companies[0])
    # with open('stock_file.csv', newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     data = list(reader)
    #fig = make_subplots(rows=1, cols=1)
    for i in range(len(selected_companies)):
    	company=selected_companies[1-i]
    	executable(start_date,start_month,start_year,to_date,to_month,to_year,selected_companies[1-i])
    	csv_file_path = company+'.csv' 
    	df = pandas.read_csv(csv_file_path)
    	df['DATE'] = pandas.to_datetime(df['DATE'])
    	df = df.sort_values(by='DATE')
 #   print(df['DATE'])
    	x_column = 'DATE'
    	y_column = 'VALUE'
    	#fig = pex.line(df, x=x_column, y=y_column, title='CSV Data Plot')
    	trace = go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=company)
    	fig.add_trace(trace)
#    plot_html = pyo.offline.plot(fig, output_type='div', include_plotlyjs=False, show_link=False)
    
    fig.update_layout(title='Stock Data',
                      xaxis_title='Date',
                      yaxis_title='Value',
                      showlegend=True)
    
    
    html_file_path = 'templates/output_plot.html' 
    fig.write_html(html_file_path)
  


    return render_template('output_plot.html')
	
	
	
def executable(start_date,start_month,start_year,to_date,to_month,to_year,sym):
    start_date=int(start_date)
    start_month=int(start_month)
    start_year=int(start_year)
    to_year=int(to_year)
    to_month=int(to_month)
    to_date=int(to_date)	
    df = stock_df(symbol=sym, from_date=date(start_year,start_month,start_date),
        to_date=date(to_year,to_month,to_date), series="EQ")
    file_path_csv = sym+'.csv'
    df.to_csv(file_path_csv, index=False)
    print("hi")




if __name__ == '__main__':
    app.run(debug=True)
    
'''

'''
import pandas
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
'''

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.static_folder = 'static'

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
@app.route('/option_page')
def option_page():
    return render_template('option_page.html')
@app.route('/analyze_stocks')
def analyze_stocks():
    return render_template('analyze_stocks.html')
@app.route('/see_timely_stock')
def see_timely_stock():
    return render_template('see_timely_stock.html')
@app.route('/apply_filter')
def apply_filter():
    return render_templates('apply_filter.html')
@app.route('/write_from_csv', methods=['POST'])
def write_from_csv():
    parameter =request.form['parameter']
    date_str = request.form['start_date']
    start_year, start_month, start_date = map(int, date_str.split('-'))
    selected_companies = request.form.getlist('sym')
    date_str = request.form['to_date']
    to_year, to_month, to_date = map(int, date_str.split('-'))

    # Create a subplot
    fig = make_subplots(rows=1, cols=1)

    for i in range(len(selected_companies)):
        company = selected_companies[i]
        executable(start_date, start_month, start_year, to_date, to_month, to_year, selected_companies[i])
        csv_file_path = company + '.csv'
        df = pandas.read_csv(csv_file_path)
        df['DATE'] = pandas.to_datetime(df['DATE'])
        df = df.sort_values(by='DATE')

        x_column = 'DATE'
        y_column = parameter

        trace = go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=company)
        fig.add_trace(trace)

    fig.update_layout(title='Stock Data',
                      xaxis_title='Date',
                      yaxis_title=parameter,
                      showlegend=True)

    html_file_path = 'templates/output_plot.html'
    fig.write_html(html_file_path)

    return render_template('output_plot.html')

def executable(start_date, start_month, start_year, to_date, to_month, to_year, sym):
    start_date = int(start_date)
    start_month = int(start_month)
    start_year = int(start_year)
    to_year = int(to_year)
    to_month = int(to_month)
    to_date = int(to_date)    
    df = stock_df(symbol=sym, from_date=date(start_year,start_month,start_date),
        to_date=date(to_year,to_month,to_date), series="EQ")
    file_path_csv = sym+'.csv'
    df.to_csv(file_path_csv, index=False)



lt=["1day","1week","1month","1year","10years","alltime"]
@app.route('/see_timely',methods=['POST'])
def see_timely():
    selected_companies = request.form.getlist('stockname')
    duration =request.form['duration']
    day_today=date.today()
    to_date =day_today.day 
    to_month=day_today.month 
    to_year =day_today.year 
    parameter =request.form['parameter']
    days_ago=day_today
    if duration ==lt[0]:
    	days_ago = day_today - timedelta(days=1)
    elif duration==lt[1]:
    	days_ago = day_today - timedelta(days=7)
    elif duration ==lt[2]:
    	days_ago = day_today - timedelta(days=30)
    elif duration ==lt[3]:
    	days_ago = day_today - timedelta(days=365)
    elif duration ==lt[4]:
    	days_ago = day_today - timedelta(days=3650)
    else:
    	days_ago = day_today - timedelta(days=3650)
    start_date=days_ago.day
    start_month=days_ago.month
    start_year =days_ago.year 
    fig = make_subplots(rows=1, cols=1)
    print(start_date, start_month, start_year, to_date, to_month, to_year, selected_companies)
    for i in range(len(selected_companies)):
    	company = selected_companies[i]
    	executable(start_date, start_month, start_year, to_date, to_month, to_year, selected_companies[i])
    	csv_file_path = company + '.csv'
    	df = pandas.read_csv(csv_file_path)
    	df['DATE'] = pandas.to_datetime(df['DATE'])
    	df = df.sort_values(by='DATE')
    	x_column = 'DATE'
    	y_column = parameter
    	trace = go.Scatter(x=df[x_column], y=df[y_column], mode='lines', name=company)
    	fig.add_trace(trace)

    fig.update_layout(title='Stock Data',
                      xaxis_title='Date',
                      yaxis_title=parameter,
                      showlegend=True)

    html_file_path = 'templates/output_plot.html'
    fig.write_html(html_file_path)

    return render_template('output_plot.html')





if __name__ == '__main__':
    app.run(debug=True)





