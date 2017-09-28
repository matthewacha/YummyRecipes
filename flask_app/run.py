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
    recipe_categories = []
    user_details = {}
    user = None
    # try to get the user
    try:
        user = db.get_user(int(user_key))
        if user:
            user_details = dict(first_name=user.first_name, email=user.email,
            last_name=user.last_name, key=user.key)
            recipe_categories = user.get_all_recipe_categories(db)
            # try to get the logged in user
            logged_in_user_key = controller.get_logged_in_user_key()
            if logged_in_user_key == user.key:
                # a registered user should be able to edit/create categories
                editable = True
    except (KeyError, TypeError):
        error = "User does not exist"

    if request.method == 'POST' and not error:
        # Get the form data
        try:
            form_data = controller.process_form_data(dict(request.form))
        except AttributeError:
            error = "Invalid form input"
        else:
            # Try to create a new recipe category and add it to recipe category list
            new_category = user.create_recipe_category(db, form_data)
            if new_category:
                recipe_categories.append(new_category)

    return render_template('categories_list.html', active=active, error=error,
                            user_details=user_details, editable=editable,
                            recipe_categories=recipe_categories)

# Not yet implemented

@app.route('/user/<int:user_key>/categories/<int:category_key>')
def categories_detail(user_key, category_key):
    """
    The page showing all availaible recipes in a given category (GET)
    Also handles PUT and DELETE of a recipe category
    Allows creation of new recipes under this category(POST)
    """
    error = None
    editable = False
    recipe_category_details = {}
    recipe_category = None
    recipes = []
    user = None
    try:
        recipe_category = db.get_recipe_category(category_key)
        if recipe_category and user_key == recipe_category.user:
            if user_key == controller.get_logged_in_user_key():
                editable = True
        else:
            raise ValueError('Wrong params in url')
    except (ValueError, KeyError, AttributeError):
        error = "Recipe Category does not exist"  

    if request.method == 'GET':
        method = request.args.get('_method') or None
        if editable and method == 'delete' and recipe_category:
            # attempt to delete the recipe_category
            recipe_category.delete(db)
            flash('Delete successful')
            return redirect(url_for('categories_list', user_key=user_key))
        
        if editable and method == 'put' and recipe_category:
            # get args data
            success = None
            description = request.args.get('description') or None
            name = request.args.get('name') or None
            if name:
                # update the name
                recipe_category.set_name(str(name), db)
                success = "Update successful"
            if description:
                # update the description
                recipe_category.set_description(str(description), db)
                success = "Update successful"
            flash(success)
            return redirect(url_for('categories_list', user_key=user_key))            
        
        if not error:
            recipe_category_details = dict(name=recipe_category.name,
                            description=recipe_category.description, 
                            key=recipe_category.key)
            recipes = list(recipe_category.get_all_recipes(db))
        return render_template('categories_detail.html', 
                recipe_category_details=recipe_category_details, user_key=user_key,
                 editable=editable, error=error, recipes=recipes, category_key=category_key)

    if request.method == 'POST' and not error:
        # get form data
        try:
            form_data = controller.process_form_data(dict(request.form))
        except AttributeError:
            error = "Invalid form input"
            flash(error)
    
        if form_data:
            try:
                recipe_category.create_recipe(**form_data, database=db)
            except ValueError:
                error = "Invalid form input for recipe"
                flash(error)
            else:
                flash('Recipe has been added successfully')

            return redirect(url_for('categories_detail', user_key=user_key,
                                category_key=category_key))
  
    return render_template('categories_detail.html')


@app.route('/categories/<int:id>/recipes/<int:recipe_id>')
def recipe_detail(id, recipe_id):
    """
    The page showing the details of a single recipe 
    including all steps (GET)
    It also handles PUT and DELETE of the recipe
    It also handles POST for creation of new RecipeSteps
    """
    return render_template('recipe_detail.html')
    

if __name__ == '__main__':
    app.run()