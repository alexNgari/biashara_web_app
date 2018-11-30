from flask import Flask, render_template, request, url_for, redirect, flash, g, session
from app import app, login, db
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from app.models import User, Business


@app.route('/')
def home():
    print(current_user)
    return render_template('app.html')


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

            user = User.query.filter_by(username=username).first()
            if user is None:
                user = User(first_name=first_name, middle_name=middle_name, last_name=last_name, username=username, email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Sign-up Successful. Click login above to log in')
                return render_template('signup.html')
            else:
                flash('Username has already been taken')
                return render_template('signup.html')

    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(user)
        if user is None or not user.check_password(password):
            return render_template('app.html', wrongPass="Wrong username or password")
        else:
            login_user(user)
            return redirect(url_for('landing', username=username))


@app.route('/register_business/<username>', methods = ['GET', 'POST'])
@login_required
def register_business(username):
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        description = request.form['description']
        location = request.form['location']
        created_by = username

        business = Business(name=name, category=category, desctiption=description, location=location, user_id=current_user.id)
        db.session.add(business)
        db.session.commit()
        flash("The business has been successfully registered")
        return render_template('registerBusiness.html', username=username)
    session.pop('_flashes', None)
    return render_template('registerBusiness.html', username=username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/landing/<string:username>')
@login_required
def landing(username):
    rows = Business.query.filter_by(user_id=current_user.id).all()
    names=[]
    for row in rows:
        names.append(row.name)
    if len(rows) == 0:
        flash('No results found')
    return render_template('landing.html', username=username, names=names)


@app.route('/search_business', methods=['GET'])
@login_required
def search_business():
    if request.method == 'GET':
        keyword_type=request.args.get('keyword_type', None)
        keyword=request.args.get('keyword', None)

        rows = Business.query.filter_by(keyword_type=keyword).all()
        if len(rows) == 0:
            flash('No results found')
            return render_template('landing.html')
        
        else:
            names = []
            for row in rows:
                names.append(row.name)
            return render_template('landing.html', names=rows)

@app.route('/business/<string:business_name>', methods=['GET'])
def business(business_name):
    if request.method == 'GET':
        business = Business.query.filter_by(name=business_name).first()
        return render_template('business.html', business=business)


@app.route('/delete', methods=['POST'])
@login_required
def delete_business():
    business_name = request.form['business_name']
    business = Business.query.filter_by(name=business_name).first()
    db.session.delete(business)
    db.session.commit()
    flash('Successfully deleted business')
    return render_template('business.html', business=None)