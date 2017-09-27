"""
This is the entry point for the app
"""

import os
from flask import request, redirect, url_for,\
    render_template, flash
from app import create_app
from app.models import db

config_name = os.getenv('APP_SETTINGS') or 'development'
app = create_app(config_name)


# routes
@app.route('/')
def index():
    """
    The homepage comprising signup and signin options
    """
    active = 'home'
    user = ''
    while user != 'STOP':
        user = input('Feed in a number\n').upper()
        db['users'].append(user)

    users = db['users']
    return render_template('index.html', active=active, users=users)


@app.route('/categories')
def categories_list():
    """
    The page showing all availaible categories of recipes
    """
    active = 'categories_list'
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