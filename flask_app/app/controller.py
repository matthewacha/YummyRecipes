"""
This module holds functionality that connects the models to the views
"""
from flask import session
from app.models import db

def process_form_data(dict_form_data):
    """ 
    After casting form data to dict, the values 
    become lists. Transform the lists to non-iterables
    """
    new_dict = {}
    try:
        for key in dict_form_data.keys():
            new_dict[key] = dict_form_data[key][0]
    except AttributeError:
        raise AttributeError('The input should be a dictionary')
    return new_dict


def get_logged_in_user_key():
    """
    This checks the session and gets the logged in user's key
    """
    if 'user_key' in session.keys():
        return session['user_key']
    else:
        return None  


def remove_user_from_session():
    """
    Removes the session variable user_key
    from the session to logout the user
    """
    if 'user_key' in session.keys():
        session.pop('user_key')
        session.modified = True
    else:
        raise KeyError('User does not exist in the session')


def add_user_to_session(user_key):
    """
    Adds the session variable user_key for 
    logged in user
    """
    user = db.get_user(user_key)
    if user is None:
        raise KeyError('User does not exist')

    session['user_key'] = user_key
    session.modified = True
    