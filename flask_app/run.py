"""
This is the entry point for the app
"""

import os
from flask import request, redirect, url_for,\
    render_template, flash
from app import create_app
from app.models import db
from app import controller

config_name = os.getenv('APP_SETTINGS') or 'development'
app = create_app(config_name)
    

# routes
@app.route('/')
def index():
    """
    The homepage comprising signup and signin options
    """
    active = 'home'
    return render_template('index.html', active=active)


@app.route('/signup', methods=['POST'])
def signup():
    """
    The signup route handles POST data sent from 
    the signup form on the home/index page
    """
    error = None
    form_data = None
    try:
        form_data = controller.process_form_data(dict(request.form))
    except AttributeError:
        error = 'invalid request'
    if form_data:
        # get the data and attempt to create a new user
        try:
            user = db.create_user(form_data)            
        except ValueError:
            error = 'Invalid form input'
        else:
            # if new user is created, log them in
            try:
                controller.add_user_to_session(user.key)
            except KeyError:
                error = 'Error while logging in'
            else:
                # redirect the user to dashboard
                flash('User sign up successful')
                return redirect(url_for('categories_list',
                                user_key=user.key))
    if error:
        flash(error)
    return redirect(url_for('index'))



@app.route('/signout')
def signout():
    """
    The signout route logs out the user
    """
    error = None
    # remove user_key from session
    try:
        controller.remove_user_from_session()
    except KeyError:
        error = 'You are not logged in'
    if error:
        flash(error)
    return redirect(url_for('index'))


@app.route('/signin', methods=['POST'])
def signin():
    """
    Logs in the user
    """
    error = None
    form_data = None
    # get request.form data
    try:
        form_data = controller.process_form_data(dict(request.form))
    except AttributeError:
        error = "Invalid form input"
    
    if form_data:
        try:
            user = db.get_user_by_email(form_data['email'])
            if user is None:
                raise KeyError('User non-existent')
        except KeyError:
            error = "User does not exist"
        else:
            # if user exists, check against the saved password
            if user.password == form_data['password']:
                # if it is the same, save username to session
                controller.add_user_to_session(user.key)
                flash('Login successful')
                return redirect(url_for('categories_list',
                                user_key=user.key))
            else:
                error = "Invalid password or username"
    if error:
        flash(error)
    return redirect(url_for('index'))


@app.route('/user/<int:user_key>/categories', methods=['GET', 'POST'])
def categories_list(user_key):
    """
    The page showing all availaible categories of recipes
    GET: Show all user's categories
    POST: Create a new category
    """
    active = 'categories_list'
    error = None
    editable = False
    category_list = None
    user = None
    # try to get the user
    try:
        user = db.get_user(int(user_key))
    except (KeyError, TypeError):
        error = "User does not exist"
    # try to get the logged in user
    logged_in_user = controller.get_logged_in_user_key()
    if logged_in_user == user and logged_in_user is not None:
        # a reigstered user should be able to edit/create categories
        editable = True
    # get the user's categories and save them to category_list
    return render_template('categories_list.html', active=active)


@app.route('/categories/<int:id>')
def categories_detail(id):
    """
    The page showing all availaible recipes in a given category
    """
    return render_template('categories_detail.html')


@app.route('/categories/<int:id>/recipes/<int:recipe_id>')
def recipe_detail(id, recipe_id):
    """
    The page showing the details of a single recipe 
    including all steps
    """
    return render_template('recipe_detail.html')
    

if __name__ == '__main__':
    app.run()