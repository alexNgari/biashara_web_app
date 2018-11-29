from flask import Flask, render_template, request, url_for, redirect, flash
from app.database import Database
from app import app


@app.route('/')
def home():
    return render_template('app.html')


@app.route('/hello')    # routing addresses
def hello():
    return 'Hello Code Camp'


# @app.route('/home')
# def home():
#     db = Database()
#     username, password = db.test()

#     title = 'Mokoso'
#     application = {'heading':'Andela Code Camp Flask Session', 'body': 'Lorem Ipsum blah blah blah'}
#     return render_template('app.html', title = title, application = application, username = username, password = password)


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
            if len(db.check_username(username)) == 0:
                db.sign_up(first_name, middle_name, last_name, email, username, password)
                flash('Sign-up Successful. Click login above to log in')
                return render_template('signup.html')
            else:
                flash('Username has already been taken')
                return render_template('signup.html')

    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/log_in', methods = ['POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = Database()
        if db.log_in(username, password):
            return redirect(url_for('landing', username=username))
        else:
            return render_template('app.html', wrongPass="Wrong username or password")


@app.route('/register_business/<username>', methods = ['GET', 'POST'])
def register_business(username):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        location = request.form['location']
        created_by = username

        db = Database()
        db.register_business(name, description, location, created_by)
        return redirect(url_for('landing', username=username))

    return render_template('registerBusiness.html', username=username)


@app.route('/landing/<string:username>')
def landing(username):
    return render_template('landing.html', username=username)
