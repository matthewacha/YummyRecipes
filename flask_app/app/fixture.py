"""
This module holds the db definition. The db is a store
of all the model objects of the current app
"""
from random import randint

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
        self._user_keys = set()
        self._recipe_keys = set()
        self._recipe_category_keys = set()
        self._recipe_steps_keys = set()

    def get_next_key(self, type_of_object):
        """Gets the next key basing on the type of object"""
        # check if type_of_object is User, RecipeCategory
        # Recipe or RecipeStep
        # get the appopraite set of keys and 
        # return the last one incremented by 1
        pass

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
        pass

    def get_user(self, user_key):
        """
        returns the User object corresponding to user_key or
        None if user does not exist
        """
        pass

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

    

# write the crud functions for all
