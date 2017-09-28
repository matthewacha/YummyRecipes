"""
This module holds the pretend-models for the application
"""
from random import randint
from app.utilities import check_type, check_email_format

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
        self._user_keys = []
        self.user_email_key_map = {}
        self._recipe_keys = []
        self.recipe_name_key_map = {}
        self._recipe_category_keys = []
        self.recipe_category_name_key_map = {}
        self._recipe_step_keys = []

    @property
    def recipe_category_keys(self):
        self._recipe_category_keys =  list(set(self._recipe_category_keys))
        return self._recipe_category_keys

    @property
    def recipe_keys(self):
        self._recipe_keys =  list(set(self._recipe_keys))
        return self._recipe_keys

    @property
    def recipe_step_keys(self):
        self._recipe_step_keys =  list(set(self._recipe_step_keys))
        return self._recipe_step_keys

    @property
    def user_keys(self):
        self._user_keys =  list(set(self._user_keys))
        return self._user_keys

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
        object_type = type(object_to_delete)
        object_dict = {}
        object_keys_list = []
        object_key_map = {}
        object_mapper = ''
        if object_type == RecipeCategory:
            object_dict = self.recipe_categories
            object_keys_list = self.recipe_category_keys
            object_key_map = self.recipe_category_name_key_map
            object_mapper = object_to_delete.name

        elif object_type == Recipe:
            object_dict = self.recipes
            object_keys_list = self.recipe_keys
            object_key_map = self.recipe_name_key_map
            object_mapper = object_to_delete.name

        elif object_type == RecipeStep:
            object_dict = self.recipe_steps
            object_keys_list = self.recipe_step_keys
            # object_key_map = self.recipe_name_key_map
            # object_mapper = object_to_delete.name            

        else:
            raise TypeError('%s type does not exist in database' % str(object_type)) 

        try:
            del(object_dict[object_to_delete.key])
            object_keys_list.remove(object_to_delete.key)
            if object_mapper:
                del(object_key_map[object_mapper])
        except KeyError:
            raise KeyError('%s does not exist' % str(object_type))        

    
    def create_user(self, user_data):
        """Creates a new user and adds the user to self.users"""
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
        if check_type(user_key, int):
            try:
                user = self.users[user_key]
            except KeyError:
                return None
            return user

    def get_user_by_email(self, email):
        """
        Returns a user object corresponding to the email
        passed in or None is user does not exist
        """
        if check_type(email, str):
            try:
                user_key = self.user_email_key_map[email]
            except KeyError:
                return None
            return self.get_user(user_key)
        
    def get_recipe_category(self, recipe_category_key):
        """
        Returns the RecipeCategory object if it exists
        or None if it doesn't
        """
        if check_type(recipe_category_key, int):
            try:
                recipe_category = self.recipe_categories[recipe_category_key]
            except KeyError:
                return None
            return recipe_category


class User:
    """
    Any user who interfaces with the app falls in this category
    """
    def __init__(self, key, first_name, last_name, email, password):
        if check_type(key, int):
            self.key = key
        if check_type(first_name, str):
            self.first_name = first_name
        if check_type(last_name, str):
            self.last_name = last_name
        if check_type(email, str):
            if check_email_format(email):
                self.email = email
        if check_type(password, str):
            self.password = password
        # a list of recipe_category keys
        self._recipe_categories = []

    @property
    def recipe_categories(self):
        self._recipe_categories = list(set(self._recipe_categories))
        return self._recipe_categories

    def add_recipe_category(self, key):
        """Adds a new recipe category key to self._recipe_categories"""
        self._recipe_categories.append(key)

    def save(self, database):
        """Saves user to the database appropriately"""
        # add self's key to db's set of user keys
        # Add self to db.users dict with key as self.key
        if check_type(database, Database):
            database.user_keys.append(self.key)
            database.users[self.key] = self
            database.user_email_key_map[self.email] = self.key

    def create_recipe_category(self, database, recipe_category_data):
        """
        Creates a new recipe category and
        adds it to database.recipe_categories
        """
        if check_type(database, Database):
            # get the last recipe category key and add 1 
            key = database.get_next_key(RecipeCategory)
            try:
                # save user in database
                self.save(database)
                category = RecipeCategory(**recipe_category_data, key=key, user=self.key)
                category.save(database)
            except TypeError:
                return None
            return category

    def get_all_recipe_categories(self, database):
        """Returns all the user's recipe categories"""
        if check_type(database, Database):
            local_recipe_categories = []
            for category in self.recipe_categories:
                try:
                    recipe_category_object = database.recipe_categories[category]
                except KeyError:
                    self.recipe_categories.remove(category)
                else:
                    local_recipe_categories.append(recipe_category_object)

            return local_recipe_categories


class RecipeCategory:
    """
    All categories of recipes belong to this class.
    Each RecipeCategory is created and can be deleted by
    one user
    """
    def __init__(self, key, name, user, description=''):
        if check_type(key, int):
            self.key = key
        if check_type(name, str):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
        if check_type(description, str):
            self.description = description
        # the creator's key. It does not change
        if check_type(user, int):
            self.user = user
        # the list of child recipe keys
        self._recipes = []

    @property
    def recipes(self):
        self._recipes = list(set(self._recipes))
        return self._recipes

    def delete(self, database):
        """Deletes this category of recipes and all recipes in it"""
        if check_type(database, Database):
            try:
                database.delete_object(self)
                user = database.get_user(self.user)
                if user:
                    user.recipe_categories.remove(self.key)
            except KeyError:
                raise KeyError('The recipe category is non-existent in database')

    def create_recipe(self, database, recipe_data):
        """
        Creates a new recipe and
        adds it to database.recipes
        """
        if check_type(database, Database):
            # get the last recipe key and add 1 
            key = database.get_next_key(Recipe)
            try:
                # save category in database
                self.save(database)
                recipe = Recipe(**recipe_data, key=key, category=self.key)
                recipe.save(database)
            except TypeError:
                return None
            return recipe

    def get_all_recipes(self, database):
        """Returns all recipes under this category"""
        if check_type(database, Database):
            local_recipes = []
            for recipe in self.recipes:
                try:
                    recipe_object = database.recipes[recipe]
                except KeyError:
                    self.recipes.remove(recipe)
                else:
                    local_recipes.append(recipe_object)

            return local_recipes

    def set_description(self, description, database):
        """Edit the description of this recipe category"""
        if check_type(description, str) and check_type(database, Database):
            self.description = description
            self.save(database)

    def set_name(self, name, database):
        """Edit the description of this recipe category"""
        if check_type(name, str) and check_type(database, Database):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
            self.save(database)

    def save(self, database):
        """Saves recipe category in db and in user"""
        # add self's key to set of recipe categories of user
        if check_type(database, Database):
            try:
                user = database.users[self.user]
                user.recipe_categories.append(self.key)
            except KeyError:
                raise KeyError('User should be saved in db first')
            # add self's key to set of db's recipe_category_keys
            database.recipe_category_keys.append(self.key)
            # Add self to db.recipe_categories dict with key as self.key
            database.recipe_categories[self.key] = self
            # Add self's name and key in db's recipe_category_name_key_map
            database.recipe_category_name_key_map[self.name] = self.key


class Recipe:
    """
    Each recipe are owned by a user and has a category
    """
    def __init__(self, key, name, description, category):
        if check_type(key, int):
            self.key = key
        if check_type(name, str):
            if len(name.strip()) == 0:
                raise ValueError('name should be a non-empty string')
            self.name = name
        if check_type(description, str):
            self.description = description
        # the category key. It does not change
        if check_type(category, int):
            self.category = category
        self.recipe_steps = []

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

    def set_name(self):
        """Changes the name of the recipe"""
        pass

    def set_description(self):
        """changes the description of the recipe"""
        pass

    def save(self, database):
        """
        Saves the recipe to the db and to the category's set of recipes
        """
        # add self's key to the set of category's set of recipe keys
        # add self's key to the set of recipe keys in the db
        # Add self to db.recipes dict with key as self.key
        # add self's key to set of recipe categories of user
        if check_type(database, Database):
            try:
                category = database.recipe_categories[self.category]
                category.recipes.append(self.key)
            except KeyError:
                raise KeyError('Category should be saved in db first')
            # add self's key to set of db's recipe_keys
            database.recipe_keys.append(self.key)
            # Add self to db.recipes dict with key as self.key
            database.recipes[self.key] = self
            # Add self's name and key in db's recipe_name_key_map
            database.recipe_name_key_map[self.name] = self.key


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
