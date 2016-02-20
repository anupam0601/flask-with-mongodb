# import the Flask class from the flask module
from flask import Flask, render_template, redirect, \
    url_for, request, session, flash, g
from functools import wraps
import datetime
import sqlite3
import time
from flask import Flask  
from pymongo import MongoClient


# create the application object
app = Flask(__name__)

# Providing the details for mongoclient and database
client = MongoClient('localhost',27017)
db = client.anupam

# config
app.secret_key = 'my precious'
#app.database = 'sample.db'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

'''
# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    # g is a flaskobject which stores temporary object requests. It will destroy once the transaction is done, Below is the connection state
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    #return render_template('index.html', posts=posts)  # render a template

time.sleep(2)
'''
#mongodb function to fetch data
@app.route('/')
@login_required
def todo():
   _items = db.movie.find()
   items = [item for item in _items]  
   return render_template('index.html', items=items)
   


@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] != 'admin') \
                or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


# for highcharts
@app.route('/graph')
@login_required
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 800):
    anupam = 'hi there'
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'CPU', "data": [6.3,8.8,6.9,6,7,8,8,9,45,34,23,23]}, {"name": 'MEM', "data": [7.8,10.5,9.36,7,8,8,9,34,23,23,12,3]}]
    title = {"text": 'My Title'}
    xAxis = {"categories":['2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27','2015-07-14 01:27:27']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, anupam=anupam)
    #return render_template('graph.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)



# For Logout
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

# connect to database
#def connect_db():
 #   return sqlite3.connect(app.database)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True,host = '0.0.0.0')