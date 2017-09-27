"""
This includes the tests for the User Object
"""

import unittest
from app.models import Database, User, Recipe, RecipeCategory, \
RecipeStep

class DatabaseTest(unittest.TestCase):
    """
    Tests for the Database class
    """

    def setUp(self):
        """Declares variables to be used in most tests"""
        self.db = Database()
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }

    def test_get_next_key(self):
        """The next key for each model object type can be got"""
        self.assertEqual(self.db.get_next_key(User), 1)
        self.assertEqual(self.db.get_next_key(Recipe), 1)
        self.assertEqual(self.db.get_next_key(RecipeCategory), 1)
        self.assertEqual(self.db.get_next_key(RecipeStep), 1)
        self.db.user_keys += [1,2,3]
        self.assertEqual(self.db.get_next_key(User), 4)
        self.db.recipe_keys += [1,2,3,7]
        self.assertEqual(self.db.get_next_key(Recipe), 8)
        self.db.recipe_category_keys += [1,2,3, 4]
        self.assertEqual(self.db.get_next_key(RecipeCategory), 5)
        self.db.recipe_step_keys += [1,2,3,9]
        self.assertEqual(self.db.get_next_key(RecipeStep), 10)
        self.assertRaises(TypeError, self.db.get_next_key, 2)

    def test_create_user(self):
        """A user can be created in 'Database'"""
        user = self.db.create_user(self.user_data)
        self.assertIsInstance(user, User)
        self.assertIn(user.key, self.db.user_keys)
        self.assertEqual(user, self.db.users[user.key])
        self.assertIn(user.email, self.db.user_email_key_map.keys())
        self.assertEqual(user.key, self.db.user_email_key_map[user.email])

    def test_get_user(self):
        """A user can be got by user_key"""
        user = User(**self.user_data, key=1)
        user.save(self.db)
        user_from_db = self.db.get_user(user.key)
        self.assertEqual(user, user_from_db)
        non_existent_key = 3
        self.assertIsNone(self.db.get_user(non_existent_key))
        self.assertRaises(TypeError, self.db.get_user, 'user_key should be int')

    def test_get_user_by_email(self):
        """A user can be got by email"""
        user = self.db.create_user(self.user_data)
        self.assertIsInstance(user, User)
        user_instance = self.db.get_user_by_email(user.email)
        self.assertEqual(user, user_instance)
        self.assertRaises(TypeError, self.db.get_user_by_email, 2)
        



    # key should not be negative or zero
    # key should not exist already


if __name__ == '__main__':
    unittest.main()
    