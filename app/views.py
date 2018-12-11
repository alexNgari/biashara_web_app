from flask import Flask, render_template, request, url_for, redirect, flash, g, session
from app import app, login, db
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from app.models import User, Business, Review


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
    my_rows = Business.query.filter_by(user_id=current_user.id).all()
    my_names=[]
    for row in my_rows:
        my_names.append(row.name)
    rows = Business.query.all()
    names = []
    for row in rows:
        names.append(row.name)
    return render_template('landing.html', username=username, my_names=my_names, names=names)


@app.route('/search_business', methods=['GET'])
@login_required
def search_business():
    if request.method == 'GET':
        keyword_type=request.args.get('keyword_type', None)
        keyword=request.args.get('keyword', None)

        if keyword_type == 'business_name':
            rows = Business.query.filter_by(name=keyword).all()
        elif keyword_type == 'location':
            rows = Business.query.filter_by(location=keyword).all()
        else:
            rows = Business.query.filter_by(category=keyword).all()
            
        if len(rows) == 0:
            flash('No results found')
            return render_template('landing.html')
        
        else:
            names = []
            for row in rows:
                names.append(row.name)
            return render_template('landing.html', names=names)



@app.route('/business/<string:business_name>', methods=['GET'])
def business(business_name):
    if request.method == 'GET':
        business = Business.query.filter_by(name=business_name).first()
        if business.user_id == current_user.id:
            return redirect(url_for('my_business', business_name=business_name))
        else:
            return redirect(url_for('other_business', business_name=business_name))


@app.route('/mbusiness/<string:business_name>', methods=['GET'])
def my_business(business_name):
    if request.method == 'GET':
        my_rows = Business.query.filter_by(user_id=current_user.id).all()
        my_names=[]
        for row in my_rows:
            my_names.append(row.name)
        business = Business.query.filter_by(name=business_name).first()
        reviews = Review.query.filter_by(business_id=business.id).all()
        query = User.query
        return render_template('mbusiness.html', business=business, my_names=my_names, reviews=reviews, query=query)


@app.route('/obusiness/<string:business_name>', methods=['GET'])
def other_business(business_name):
    if request.method == 'GET':
        my_rows = Business.query.filter_by(user_id=current_user.id).all()
        my_names=[]
        for row in my_rows:
            my_names.append(row.name)
        business = Business.query.filter_by(name=business_name).first()
        reviews = Review.query.filter_by(business_id=business.id).all()
        query = User.query
        return render_template('obusiness.html', business=business, my_names=my_names, reviews=reviews, query=query)


@app.route('/delete', methods=['POST'])
@login_required
def delete_business():
    session.pop('_flashes', None)
    business_name = request.form['business_name']
    business = Business.query.filter_by(name=business_name).first()
    if business:
        if business.user_id == current_user.id:
            db.session.delete(business)
            db.session.commit()
            flash('Successfully deleted business')
        else:
            flash('Get your own business!')
    else:
        flash('Names do not match!')
    return render_template('mbusiness.html', business=None)


@app.route('/update_business/<string:business_name>', methods = ['GET', 'POST'])
@login_required
def update_business(business_name):
    if request.method == 'POST':
        business = Business.query.filter_by(name=business_name).first()
        business.name = request.form['name']
        business.category = request.form['category']
        business.desctiption = request.form['description']
        business.location = request.form['location']
        db.session.commit()
        flash('Successfully updated details')
        return render_template('update_business.html', business=business)
    else:
        session.pop('_flashes', None)
        business = Business.query.filter_by(name=business_name).first()
        return render_template('update_business.html', business=business)
def review_business(business_name):
    if request.method == 'POST':
        business = Business.query.filter_by(name=business_name).first()
        post = request.form['post']

        review = Review(user_id=current_user.id, business_id=business.id, post=post)
        db.session.add(review)
        db.session.commit()
        flash('Review Posted')
        return render_template('review.html', business=business)
    else:
        session.pop('_flashes', None)
        business = Business.query.filter_by(name=business_name).first()
        return render_template('review.html', business=business)


@app.route('/review/<string:business_name>', methods=['GET', 'POST'])
@login_required
def review_business(business_name):
    if request.method == 'POST':
        business = Business.query.filter_by(name=business_name).first()
        post = request.form['post']

        review = Review(user_id=current_user.id, business_id=business.id, post=post)
        db.session.add(review)
        db.session.commit()
        flash('Review Posted')
        return render_template('review.html', business=business)
    else:
        session.pop('_flashes', None)
        business = Business.query.filter_by(name=business_name).first()
        return render_template('review.html', business=business)
