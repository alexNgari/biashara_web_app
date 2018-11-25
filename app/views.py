from flask import Flask, render_template, request
from app import database
from app import app


@app.route('/hello')    # routing addresses
def hello():
    return 'Hello Code Camp'


@app.route('/home')
def home():
    db = Database()
    username, password = db.test()

    title = 'Mokoso'
    application = {'heading':'Andela Code Camp Flask Session', 'body': 'Lorem Ipsum blah blah blah'}
    return render_template('app.html', title = title, application = application, username = username, password = password)


@app.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        if request.form['password'] == request.form['password2']:
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            db = Database()
            db.sign_up(first_name, middle_name, last_name, email, username, password)
            
            return login()

    return render_template('signup.html')


@app.route('/log_in', methods = ['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = Database()
        if db.log_in(username, password):
            return render_template('landing.html')

    return render_template('login.html')


@app.route('/landing')
def landing():
    return render_template('landing.html')
