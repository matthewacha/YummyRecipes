"""
This is the entry point for the app
"""

import os
from flask import request, redirect, url_for,\
    render_template, flash
from app import create_app

config_name = os.getenv('APP_SETTINGS') or 'development'
app = create_app(config_name)


# routes
@app.route('/')
def index():
    """
    A sample route to show that flask is working
    """
    return "Hello YummyRecipes!"


if __name__ == '__main__':
    app.run()