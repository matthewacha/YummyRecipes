"""
This module holds the pretend-models for the application
"""
from random import randint
from app.utilities import check_type

def binary_search(character, list_of_characters, position=0):
    """
    Searches for character using binary search
    returns None if character is not found
    otherwise returns character's position in sorted list
    """
    length_of_list = len(list_of_characters)
    if length_of_list <= 1:
        if length_of_list == 0:
            return None
        if character != list_of_characters[0]:
            return None
        return position

    random_int = randint(0, length_of_list - 1)
    if character < list_of_characters[random_int]:
        new_list = list_of_characters[:(random_int)]
        position += 0
    else:
        new_list = list_of_characters[random_int:]
        position += random_int
    # return this so that it recursively comes back to the surface
    return binary_search(character, new_list, position)


class Database:
    """This is the daabase for the application"""
    def __init__(self):
        self.users = {}
        self.recipes = {}
        self.recipe_categories = {}
        self.recipe_steps = {}
        self.user_keys = []
        self.recipe_keys = []
        self.recipe_category_keys = []
        self.recipe_step_keys = []

    def get_next_key(self, type_of_object):
        """Gets the next key basing on the type of object"""
        # type_of_object should be of type type
        if check_type(type_of_object, type):
            if type_of_object == User:
                return self.__get_max_value(self.user_keys) + 1

            if type_of_object == Recipe:
                return self.__get_max_value(self.recipe_keys) + 1

            if type_of_object == RecipeCategory:
                return self.__get_max_value(self.recipe_category_keys) + 1

            if type_of_object == RecipeStep:
                return self.__get_max_value(self.recipe_step_keys) + 1

    def __get_max_value(self, unsorted_list):
        """Returns the maximum value of a list or 0 if list is empty"""
        if check_type(unsorted_list, list):
            length = len(unsorted_list)
            if length == 0:
                return 0

            unsorted_list.sort()
            return unsorted_list[length - 1]


    def delete_object(self, object_to_delete):
        """
        Depending on the object type, delete object from
        the dict where its type is
        """
        # store the type of object in a variable
        # check that variable against all the possible
        # Object types and locate the dict
        # then call del(approriate_dict[object_to_delete.key])
        pass
    
    def create_user(self, user_data):
        """Creates a new user and adds the user to self.users"""
        # get the last user key and add 1 (use self.get_next_key(User))
        # create a new user with that key
        # add them to the dict of users in self.users and
        # update the set of user keys (call the new user's save method)
        user_key = self.get_next_key(User)
        try:
            user = User(**user_data, key=user_key)
            user.save(self)
        except:
            raise ValueError('invalid user data')
        return user

    def get_user(self, user_key):
        """
        returns the User object corresponding to user_key or
        None if user does not exist
        """
        try:
            user = self.users[user_key]
        except KeyError:
            return None
        return user

    def create_recipe_category(self, recipe_category_data):
        """
        Creates a new recipe category and
        adds it to self.recipe_categories
        """
        # get the last recipe category key and add 1 
        # (use self.get_next_key(RecipeCategory))
        # create a new recipe category with that key
        # add them to the dict of recipe categories 
        # in self.recipe_categories and
        # update the set of recipe category keys 
        # (call the new recipe category's save method)
        pass

    def get_recipe_category(self, recipe_category_key):
        """
        Returns the RecipeCategory object if it exists
        or None if it doesn't
        """
        pass

    def create_recipe(self, recipe_data):
        """
        Creates a new recipe and
        adds it to self.recipes
        """
        # get the last recipe key and add 1 to it
        # (use self.get_next_key(Recipe))
        # create a new recipe with that key
        # add it to the dict of recipes in self.recipes
        # update the set of recipe keys (call the new recipe's save method)
        pass

    def get_recipe(self, recipe_key):
        """
        Returns the Recipe object if it exists
        or None if it doesn't
        """
        pass

    def create_recipe_step(self, recipe_data):
        """
        Creates a new recipe step and
        adds it to self.recipe_steps
        """
        # get the last recipe step key and add 1 to it
        # (use self.get_next_key(RecipeStep))
        # create a new recipe step with that key
        # call the recipe's save method
        pass

    def get_recipe_step(self, recipe_key):
        """
        Returns the RecipeStep object if it exists
        or None if it doesn't
        """
        pass


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
        self.recipe_categories = []
    
    def login(self, request):
        """Logs in the user"""
        pass

    def logout(self, request):
        """Logs out the user"""
        pass

    def save(self, database):
        """Saves user to the database appropriately"""
        # add self's key to db's set of user keys
        # Add self to db.users dict with key as self.key
        if check_type(database, Database):
            database.user_keys.append(self.key)
            database.users[self.key] = self
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

    def delete(self, database):
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

    def save(self, database):
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

    def change_category(self, new_category, database):
        """Changes the category of the recipe"""
        # add self's key to new_category's recipe list
        # remove self's key from old category's recipe list
        pass

    def delete(self, database):
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

    def save(self, database):
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

    def delete(self, database):
        """Deletes this RecipeStep"""
        # remove self's key from set of keys of recipe steps in parent
        # recipe
        # remove self's key from the set of recipe_step_keys in db
        # delete itself using db.delete_object()
        pass

    def edit_text_content(self):
        """Edit the text_content"""
        pass

    def save(self, database):
        """
        Save this object's key in parent recipe's set of recipe steps
        and in db
        """
        # Add self.key in self.recipe.recipe_steps set
        # Add self.key in db.recipe_step_keys set
        # Add self to db.recipe_steps dict with key as self.key
        pass


# A global db
db = Database()
