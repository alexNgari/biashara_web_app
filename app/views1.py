# from flask import Flask, render_template, request, url_for, redirect, flash, g, session
# from app.database import Database, User
# from app import app
# from flask_login import LoginManager, login_required, logout_user, login_user, current_user


# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     db = Database()
#     if len(db.check_username(user_id)) == 1:
#         return User(user_id)
#     else:
#         return None

# @app.route('/')
# def home():
#     return render_template('app.html')


# # @app.route('/home')
# # def home():
# #     db = Database()
# #     username, password = db.test()

# #     title = 'Mokoso'
# #     application = {'heading':'Andela Code Camp Flask Session', 'body': 'Lorem Ipsum blah blah blah'}
# #     return render_template('app.html', title = title, application = application, username = username, password = password)


# @app.route('/sign_up', methods = ['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         if request.form['password'] == request.form['password2']:
#             first_name = request.form['first_name']
#             middle_name = request.form['middle_name']
#             last_name = request.form['last_name']
#             email = request.form['email']
#             username = request.form['username']
#             password = request.form['password']

#             db = Database()
#             if len(db.check_username(username)) == 0:
#                 db.sign_up(first_name, middle_name, last_name, email, username, password)
#                 flash('Sign-up Successful. Click login above to log in')
#                 return render_template('signup.html')
#             else:
#                 flash('Username has already been taken')
#                 return render_template('signup.html')

#     if request.method == 'GET':
#         return render_template('signup.html')


# @app.route('/log_in', methods = ['POST'])
# def log_in():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = Database()
#         user = User(username)
#         if db.log_in(username, password):
#             login_user(user)
#             return redirect(url_for('landing', username=username))
#         else:
#             return render_template('app.html', wrongPass="Wrong username or password")


# @app.route('/register_business/<username>', methods = ['GET', 'POST'])
# @login_required
# def register_business(username):
#     if request.method == 'POST':
#         name = request.form['name']
#         category = request.form['category']
#         description = request.form['description']
#         location = request.form['location']
#         created_by = username

#         db = Database()
#         db.register_business(name, category, description, location, created_by)
#         flash("The business has been successfully registered")
#         return render_template('registerBusiness.html', username=username)

#     session.pop('_flashes', None)
#     return render_template('registerBusiness.html', username=username)

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @app.route('/landing/<string:username>')
# @login_required
# def landing(username):
#     db = Database()
#     rows = db.all_business_names()
#     my_rows = db.my_businesses(username)
#     names=[]
#     my_names=[]
#     for row in rows:
#         names.append(row['business_name'])
#     for row in my_rows:
#         my_names.append(row['business_name'])
#     if len(rows) == 0:
#         flash('No results found')
#     return render_template('landing.html', username=username, names=names, businesses=my_names)


# @app.route('/search_business', methods=['GET'])
# @login_required
# def search_business():
#     if request.method == 'GET':
#         keyword_type=request.args.get('keyword_type', None)
#         keyword=request.args.get('keyword', None)
#         username=current_user.get_id()

#         db = Database()
#         rows = db.search_business_names(keyword_type, keyword)
#         my_rows = db.my_businesses(username)
#         my_names=[]
#         for row in my_rows:
#             my_names.append(row['business_name'])
#         if len(rows) == 0:
#             flash('No results found')
#             return render_template('landing.html')
        
#         else:
#             return render_template('landing.html', names=rows, businesses=my_names)


# @app.route('/business/<string:business_name>', methods=['GET'])
# def business(business_name):
#     if request.method == 'GET':
#         db = Database()
#         rows = db.search_business('business_name', business_name)
#         business = rows.pop(0)
#         if business['created_by'] == current_user.get_id():
#             return redirect(url_for('my_business', business_name=business_name))
#         else:
#             return redirect(url_for('other_business', business_name=business_name))


# @app.route('/mbusiness/<string:business_name>', methods=['GET'])
# def my_business(business_name):
#     if request.method == 'GET':
#         db = Database()
#         rows = db.search_business('business_name', business_name)
#         business = rows.pop(0)
#         return render_template('mbusiness.html', business=business)


# @app.route('/obusiness/<string:business_name>', methods=['GET'])
# def other_business(business_name):
#     if request.method == 'GET':
#         db = Database
#         rows = db.search_business('business_name', business_name)
#         business = rows.pop(0)
#         return render_template('obusiness.html', business=business)


# @app.route('/delete', methods=['POST'])
# @login_required
# def delete_business():
#     session.pop('_flashes', None)
#     business_name = request.form['business_name']
#     db=Database()
#     row = db.search_business('business_name', business_name)
#     if len(row) == 1:    
#         db.delete_business(business_name)
#         flash('Successfully deleted business')
#     else:
#         flash('Names do not match!')
#     return render_template('business.html', business=None)


# @app.route('/update_business/<string:business_name>', methods = ['GET', 'POST'])
# @login_required
# def update_business(business_name):
#     if request.method == 'POST':
#         name = request.form['name']
#         category = request.form['category']
#         description = request.form['description']
#         location = request.form['location']

#         db = Database()
#         rows = db.search_business('business_name', name)
#         if len(rows) == 1 and rows[0]['created_by'] == current_user.get_id():
#             db.update_business(business_name, name, category, description, location)
#             flash('Details successfully updated')
#             return render_template('update_business.html')
#     else:
#         session.pop('_flashes', None)
#         business_name = request.args.get('business_name', None)
#         db = Database()
#         business = db.search_business('business_name', business_name)
#         return render_template('update_business.html', business_name="business_name", business=business)


        