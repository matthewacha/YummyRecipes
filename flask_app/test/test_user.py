"""Module to test the User Data Model"""

import unittest
from app.models import User, Database


class UserTest(unittest.TestCase):
    """Tests for the User data model"""

    def setUp(self):
        """
        Set up variables that will be used in most tests
        """
        self.user_data = {
            'key': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'password',
            }
        self.user = User(**self.user_data)
        self.db = Database()

    def test_user_can_be_created(self):
        """User can be created"""
        user = User(**self.user_data)
        self.assertIsInstance(user, User)
        self.assertRaises(TypeError, User, key=3)
        del(self.user_data['password'])
        self.assertRaises(TypeError, User, **self.user_data)

    def test_user_can_be_saved(self):
        """User can be saved in Database"""
        self.assertRaises(TypeError, self.user.save,
                          'Database object expected')
        self.user.save(self.db)
        self.assertIn(self.user.key, self.db.user_keys)
        self.assertEqual(self.user, self.db.users[self.user.key])
        self.assertIn(self.user.email, self.db.user_email_key_map.keys())
        # self.assertEqual(self.user.key, self.db.user_email_key_map[self.user.email])




if __name__ == '__main__':
    unittest.main()