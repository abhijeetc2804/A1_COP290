
from datetime import date 
from datetime import datetime, timedelta
import pandas 
import yfinance as yf
import sys 
from datetime import date
import time
import memory_profiler 
from memory_profiler import profile 
import pyarrow 
import pyarrow.parquet
import matplotlib.pyplot as graph
import os 
import csv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import plotly.express as pex
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots
'''
app = Flask(name)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key


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




if name == 'main':
    app.run(debug=True)
    
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
    return render_template('apply_filter.html')
@app.route('/write_from_csv', methods=['POST'])
def write_from_csv():
    parameter =request.form['parameter']
    date_str = request.form['start_date']
    start_date=date_str
    selected_companies = request.form.getlist('sym')
    date_str = request.form['to_date']
    to_date=date_str
    print(start_date,to_date)
    # Create a subplot
    fig = make_subplots(rows=1, cols=1)

    for i in range(len(selected_companies)):
        company = selected_companies[i]
        executable(start_date, to_date, selected_companies[i]+".NS")
        csv_file_path = company + '.NS.csv'
        df = pandas.read_csv(csv_file_path)

    # Print the column names
        print(f"Column names for {company}: {df.columns}")

    # Convert the 'DATE' column to datetime
        df['Date'] = pandas.to_datetime(df['Date'])
        df = df.sort_values(by='Date')

        x_column = 'Date'
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

def executable(start_date,to_date, sym):
    try:
        # Download stock data
        df = yf.download(sym, start=start_date, end=to_date)

        # Resetting index to include 'Date' as a regular column
        df.reset_index(inplace=True)

        # Save data to CSV
        file_path_csv = sym + '.csv'
        df.to_csv(file_path_csv, index=False)

        print(f"Data downloaded and saved for {sym}")
    except Exception as e:
        print(f"Error downloading data for {sym}: {e}")


lt=["1day","1week","1month","1year","10years","alltime"]
@app.route('/see_timely',methods=['POST'])
def see_timely():
    selected_companies = request.form.getlist('stockname')
    duration =request.form['duration']
    day_today=date.today()
    to_date =day_today
    
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
    start_date=days_ago
    fig = make_subplots(rows=1, cols=1)
    print(start_date,to_date, selected_companies)
    for i in range(len(selected_companies)):
        company = selected_companies[i]
        executable(start_date,to_date, selected_companies[i]+".NS")
        csv_file_path = company + '.NS.csv'
        df = pandas.read_csv(csv_file_path)
        df['Date'] = pandas.to_datetime(df['Date'])
        df = df.sort_values(by='Date')
        x_column = 'Date'
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
company_list = [
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT",
    "AXISBANK",
    "BAJAJ-AUTO",
    "BAJFINANCE",
    "BAJAJFINSV",
    "BPCL",
    "BHARTIARTL",
    "BRITANNIA",
    "CIPLA",
    "COALINDIA",
    "DIVISLAB",
    "DRREDDY",
    "EICHERMOT",
    "GRASIM",
    "HCLTECH",
    "HDFCBANK",
    "HDFCLIFE",
    "HEROMOTOCO",
    "HINDALCO",
    "HINDUNILVR",
    "ICICIBANK",
    "ITC",
    "INDUSINDBK",
    "INFY",
    "JSWSTEEL",
    "KOTAKBANK",
    "LTIM",
    "LT",
    "MARUTI",
    "NTPC",
    "NESTLEIND",
    "ONGC",
    "POWERGRID",
    "RELIANCE",
    "SBILIFE",
    "SBIN",
    "SUNPHARMA",
    "TCS",
    "TATACONSUM",
    "TATAMOTORS",
    "TATASTEEL",
    "TECHM",
    "TITAN",
    "UPL",
    "ULTRACEMCO",
    "WIPRO"
]
def calculate_mean_stock_price(sym, start_date, end_date):
    # Download stock data
    df = yf.download(sym+'.NS', start=start_date, end=end_date)

    # Calculate mean closing price
    mean_price = df['Close'].mean()

    return mean_price
def calculate_pe_ratio(symbol):
    try:
        # Download fundamental data
        data = yf.Ticker(symbol).info

        # Extract P/E ratio
        pe_ratio = data.get('trailingPE', None)

        return pe_ratio
    except Exception as e:
        print(f"Error calculating P/E ratio for {symbol}: {e}")
        return None   

def calculate_pe_ratio(symbol):
        # Fetch stock information
        stock = yf.Ticker(symbol)

        # Get historical data for the last trading day
        history = stock.history(period="1d")

        # Extract the latest closing price
        latest_close = history['Close'].iloc[-1]

        # Extract the earnings per share (EPS)
        eps = stock.info.get('trailingPE', None)

        # Check if EPS is available
        if eps is not None:
            # Calculate the P/E ratio
            pe_ratio = latest_close / eps
            return pe_ratio
        else:
            return None


@app.route('/apply_filter_to_table',methods=['POST'])
def apply_filter_to_table():
    filtered_companies=[i for i in company_list]
    parameter = request.form.getlist('parameter[]')
    start_date = request.form['start_date']
    to_date = request.form['to_date']
    average_min_value=0
    average_max_value=0
    volume_min_value=0
    volume_max_value=0
    pe_ratio_min_value=0
    pe_ratio_max_value=0
    if 'close' in parameter:
    # Retrieve min and max values for Close Price
    	average_min_value = int(request.form.get('average_min_value'))
    	average_max_value = int(request.form.get('average_max_value'))
   # print(average_min_value,average_max_value)
    # Retrieve min and max values for Volume
    if 'volume' in parameter:
    	volume_min_value = int(request.form.get('volume_min_value'))
    	volume_max_value = int(request.form.get('volume_max_value'))
    
    if 'pe_ratio' in parameter:
    	pe_ratio_min_value = float(request.form.get('pe_ratio_min_value'))
    	pe_ratio_max_value = float(request.form.get('pe_ratio_max_value'))
    final_companies=[]
  #  print(parameter,"hi")
    if 'close' in parameter:
        for company in filtered_companies:
            x=calculate_mean_stock_price(company, start_date, to_date)
            
            if x>=average_min_value and x<=average_max_value:
                final_companies.append(company)
        filtered_companies=[i for i in final_companies]
        final_companies=[]
  #  print(filtered_companies," hi")
    if 'volume' in parameter:
        for company in filtered_companies:
            df = yf.download(company+'.NS', start=start_date, end=to_date)
            if df['Volume'].max() >= volume_min_value and df['Volume'].max()<=volume_max_value:
                    final_companies.append(company)
        filtered_companies=[i for i in final_companies]
        final_companies=[]   
    if 'pe_ratio' in parameter:
        for company in filtered_companies:
            x=calculate_pe_ratio(company+'.NS')
            print(company,x)
            if x is not None and float(x)>=pe_ratio_min_value and float(x)<=pe_ratio_max_value:
                final_companies.append(company)
        filtered_companies=[i for i in final_companies]
    print(filtered_companies)
    
    return render_template('filtered_company_data.html',companies=filtered_companies)
    
    
    
@app.route('/company/<company_symbol>')
def company_details(company_symbol):
        company = yf.Ticker(company_symbol+'.NS')
        history = company.history(period="1d")  # Fetch daily historical data
        details = {
            'Name': company.info.get('longName', ''),
            'Symbol': company_symbol,
            'Description': company.info.get('longBusinessSummary', 'No description available.'),
            'Industry': company.info.get('industry', 'N/A'),
            'Sector': company.info.get('sector', 'N/A'),
            'Open': history['Open'].iloc[0],
            'Close': history['Close'].iloc[0],
            'High': history['High'].iloc[0],
            'Low': history['Low'].iloc[0],
            'Average': history['Close'].mean(),
            'Volume': history['Volume'].iloc[0],
        }
        return render_template('company_data.html', details=details)
 
if __name__ == '__main__':
    app.run(debug=True)

