"""
This module holds the pretend-models for the application
"""
from app.fixture import Database

# A global db
db = Database()

class User:
    """
    Any user who interfaces with the app falls in this category
    """
    def __init__(self, key, first_name, last_name, email, password):
        self.key = key
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        # a list of recipe_category keys
        self.recipe_categories = set()
    
    def login(self, request):
        """Logs in the user"""
        pass

    def logout(self, request):
        """Logs out the user"""
        pass

    def save(self):
        """Saves user to the database appropriately"""
        # add self's key to db's set of user keys
        # Add self to db.users dict with key as self.key
        pass


class RecipeCategory:
    """
    All categories of recipes belong to this class.
    Each RecipeCategory is created and can be deleted by
    one user
    """
    def __init__(self, key, name, description, user):
        self.key = key
        self.name = name
        self.description = description
        # the creator's key. It does not change
        self.user = user
        # the list of child recipe keys
        self.recipes = set()

    def delete(self):
        """Deletes this category of recipes and all recipes in it"""
        # deletes all child recipes based on list of child recipes
        # get the creator
        # delete self's key from creator's set of categories
        # delete self's key from db's set of recipe category keys
        # then deletes itself (CASCADE) using db.delete_object()
        pass

    def edit_description(self, description):
        """Edit the description of this recipe category"""
        pass

    def edit_name(self, name):
        """Edit the description of this recipe category"""
        pass

    def save(self):
        """Saves recipe category in db and in user"""
        # add self's key to set of recipe categories of user
        # add self's key to set of db's recipe_category_keys
        # Add self to db.recipe_categories dict with key as self.key
        pass
    



class Recipe:
    """
    Each recipe are owned by a user and has a category
    """
    def __init__(self, key, name, description, category, user):
        self.key = key
        self.name = name
        self.description = description
        # the key of the parent category
        self.category = category
        # list of keys of child steps
        self.recipe_steps = set()

    def change_category(self, new_category):
        """Changes the category of the recipe"""
        # add self's key to new_category's recipe list
        # remove self's key from old category's recipe list
        pass

    def delete(self):
        """Deleted the recipe"""
        # deletes all child steps based on the self.recipe_steps list
        # deletes self's key from category's set of recipes
        # deletes self's key from db's set of recipe keys
        # then deletes itself using db.delete_object()
        pass

    def edit_name(self):
        """Changes the name of the recipe"""
        pass

    def edit_description(self):
        """changes the description of the recipe"""
        pass

    def save(self):
        """
        Saves the recipe to the db and to the category's set of recipes
        """
        # add self's key to the set of category's set of recipe keys
        # add self's key to the set of recipe keys in the db
        # Add self to db.recipes dict with key as self.key
        pass


class RecipeStep:
    """Every recipe contains individual steps"""
    def __init__(self, key, recipe, text_content):
        self.key = key
        self.recipe = recipe
        self.text_content = text_content

    def delete(self):
        """Deletes this RecipeStep"""
        # remove self's key from set of keys of recipe steps in parent
        # recipe
        # remove self's key from the set of recipe_step_keys in db
        # delete itself using db.delete_object()
        pass

    def edit_text_content(self):
        """Edit the text_content"""
        pass

    def save(self):
        """
        Save this object's key in parent recipe's set of recipe steps
        and in db
        """
        # Add self.key in self.recipe.recipe_steps set
        # Add self.key in db.recipe_step_keys set
        # Add self to db.recipe_steps dict with key as self.key
        pass

