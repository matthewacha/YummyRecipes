"""Module holds tests for the RecipeCategory class"""


import unittest
from app.models import Database, User, RecipeCategory, Recipe
from app import utilities


class RecipeCategoryTest(unittest.TestCase):
    """All tests for the RecipeCategory class"""
    
    def setUp(self):
        """Initiates variables to be used in most tests"""
        self.db = Database()
        self.user_data = {
            'key': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }
        self.user = User(**self.user_data)
        self.db = Database()
        self.user.save(self.db)
        self.category_data = {
            'key': 1,
            'name': 'cakes',
            'description': 'all recipes cake!',
            'user': self.user.key,
        }
        self.category = RecipeCategory(**self.category_data)

    def test_name_is_mandatory(self):
        """
        In the constructor, the name parameter should be 
        a string which is not empty
        """
        self.assertRaises(TypeError, RecipeCategory, key=1,
                          description='', user=self.user.key)
        invalid_data = utilities.replace_value_in_dict(self.category_data, 'name', 7)
        self.assertRaises(TypeError, RecipeCategory, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.category_data, 'name', '')
        self.assertRaises(ValueError, RecipeCategory, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.category_data, 'name', ' ')
        self.assertRaises(ValueError, RecipeCategory, **invalid_data)

    def test_save_method(self):
        """
        The save() method should be able to update the parent user's 
        list of recipe categories as well as that of the database
        """
        self.assertIsInstance(self.category, RecipeCategory)
        self.category.save(self.db)
        length_of_db_category_keys = len(self.db.recipe_category_keys)
        length_of_user_categories = len(self.user.recipe_categories)
        self.assertIn(self.category.key, self.db.recipe_category_keys)
        self.assertEqual(self.category, self.db.recipe_categories[self.category.key])
        self.assertIn(self.category.key, self.user.recipe_categories)
        self.assertIn(self.category.name, self.db.recipe_category_name_key_map.keys())
        self.assertEqual(self.category.key,
                         self.db.recipe_category_name_key_map[self.category.name])
        # the user should exist in database
        invalid_data = utilities.replace_value_in_dict(self.category_data, 'user', 78)
        new_category = RecipeCategory(**invalid_data)
        self.assertRaises(KeyError, new_category.save, self.db)
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.category.save, 
                          'string instead of Database object')
        # calling save more than once does not increase size of self.db.recipe_category_keys
        self.category.save(self.db)
        self.assertEqual(len(self.db.recipe_category_keys), length_of_db_category_keys)
        # calling save more than once does not increase size of self.user.recipe_categories
        self.assertEqual(len(self.user.recipe_categories), length_of_user_categories)


