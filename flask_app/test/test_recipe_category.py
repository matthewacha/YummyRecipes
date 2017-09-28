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

    def test_delete(self):
        """RecipeCategory can be deleted"""
        self.assertIsInstance(self.category, RecipeCategory)
        self.category.save(self.db)
        self.assertEqual(self.category, self.db.recipe_categories[self.category.key])
        self.assertEqual(self.category, self.db.recipe_categories.get(self.category.key))
        self.category.delete(self.db)
        self.assertRaises(KeyError, utilities.return_value_from_dict,
                          self.db.recipe_categories, self.category.key)
        self.assertNotIn(self.category.key, self.db.recipe_category_keys)
        self.assertNotIn(self.category.key, self.user.recipe_categories)
        self.assertNotIn(self.category.name, self.db.recipe_category_name_key_map.keys())
        # database parameter should be of type Database
        self.assertRaises(TypeError, self.category.delete, 
                          'string instead of Database object')
        # calling delete more than once on same Database objec raises KeyError
        self.assertRaises(KeyError, self.category.delete, self.db)

    def test_set_name(self):
        """ The name can be set with a new non-empty string value"""
        # try to set a new name
        new_name = 'foo'
        self.category.set_name(new_name)
        # assert that the new name is set
        self.assertEqual(new_name, self.category.name)
        # try setting with a non string name
        self.assertRaises(TypeError, self.category.set_name, 2)
        # try setting with an empty string
        self.assertRaises(ValueError, self.category.set_name, '')
        # try setting with a space string 
        self.assertRaises(ValueError, self.category.set_name, '  ')
    
    def test_set_description(self):
        """ The description can be set with a new non-empty string value"""
        # try to set a new description
        new_description = 'bar'
        self.category.set_description(new_description)
        # assert that the new description is set
        self.assertEqual(new_description, self.category.description)
        # try setting with a non string description
        self.assertRaises(TypeError, self.category.set_description, 2)


if __name__ == '__main__':
    unittest.main()

