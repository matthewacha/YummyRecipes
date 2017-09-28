"""Module containing all the tests for Recipe class"""


import unittest
from app.models import Database, User, RecipeCategory, Recipe
from app import utilities


class RecipeTest(unittest.TestCase):
    """All tests for the Recipe class"""
    
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
        self.category.save(self.db)
        self.recipe_data = {
            'key': 1,
            'name': 'Banana cake',
            'description': 'yummy!',
            'category': self.category.key
        }
        self.recipe = Recipe(**self.recipe_data)

    def test_name_is_mandatory(self):
        """
        In the constructor, the name parameter should be 
        a string which is not empty
        """
        self.assertRaises(TypeError, Recipe, key=1,
                          description='', category=self.category.key)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', 7)
        self.assertRaises(TypeError, Recipe, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', '')
        self.assertRaises(ValueError, Recipe, **invalid_data)
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'name', ' ')
        self.assertRaises(ValueError, Recipe, **invalid_data)

    def test_save_method(self):
        """
        The save() method should be able to update the parent category's 
        list of recipes as well as that of the database
        """
        self.assertIsInstance(self.recipe, Recipe)
        self.recipe.save(self.db)
        length_of_db_recipe_keys = len(self.db.recipe_keys)
        length_of_category_recipes = len(self.category.recipes)
        self.assertIn(self.recipe.key, self.db.recipe_keys)
        self.assertEqual(self.recipe, self.db.recipes[self.recipe.key])
        self.assertIn(self.recipe.key, self.category.recipes)
        self.assertIn(self.recipe.name, self.db.recipe_name_key_map.keys())
        self.assertEqual(self.recipe.key,
                         self.db.recipe_name_key_map[self.recipe.name])
        # the category should exist in database
        invalid_data = utilities.replace_value_in_dict(self.recipe_data, 'category', 78)
        new_recipe = Recipe(**invalid_data)
        self.assertRaises(KeyError, new_recipe.save, self.db)
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.recipe.save, 
                          'string instead of Database object')
        # calling save more than once does not increase size of self.db.recipe_keys
        self.recipe.save(self.db)
        self.assertEqual(len(self.db.recipe_keys), length_of_db_recipe_keys)
        # calling save more than once does not increase size of self.category.recipes
        self.assertEqual(len(self.category.recipes), length_of_category_recipes)


if __name__ == '__main__':
    unittest.main()