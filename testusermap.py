import unittest
from usermap import UserMap, PasswordError, UserRecord

class TestUserRecord(unittest.TestCase):
    def setUp(self):
        self.user1 = UserRecord(username = 'melanie', password = 'password123')

    def testinit(self):
        self.assertEqual(self.user1.username, 'melanie')
        self.assertNotEqual(self.user1.password_hash, 'password123')

class TestUserMap(unittest.TestCase):
    def test_len(self):
        um = UserMap()
        self.assertEqual(um.__len__(), 0)
        um.add_user('melanie', 'password123')
        self.assertEqual(um.__len__(), 1)

    def test_getitem(self):
        um = UserMap()
        um.add_user('melanie', 'password')
        self.assertEqual(repr(um.__getitem__('melanie')), 'UserRecord: melanie')

    def test_contains(self):
        um = UserMap()
        um.add_user('melanie', 'password123')
        self.assertTrue(um.__contains__('melanie'))

    def test_add_user(self):
        um = UserMap()
        um.add_user('melanie', 'password123')
        self.assertTrue(um.__contains__('melanie'))
        um.add_user('kiki', 'password456')
        self.assertTrue(um.__contains__('kiki'))
        um.add_user('laura', 'password789')
        self.assertTrue(um.__contains__('laura'))

    def test_update_password(self):
        um = UserMap()
        um.add_user('melanie', 'password123')
        um.update_password('melanie', 'password123', 'password000')
        self.assertEqual(um['melanie'].password_hash, hash(um['melanie'].salt + 'password000'))

    def test_update_password_incorrect_password(self):
        um = UserMap()
        um.add_user('kiki', 'password111')
        with self.assertRaises(PasswordError):
            um.update_password('kiki', 'password000', 'password123')

    def test_update_password_incorrect_username(self):
        um = UserMap()
        um.add_user('kiki', 'password111')
        with self.assertRaises(KeyError):
            um.update_password('melanie', 'password111', 'password123')

    def test_double(self):
        um = UserMap()
        um._double()
        self.assertEqual(um._num_buckets, 16)


class TestPasswordError(unittest.TestCase):
    def test_error(self):pass



unittest.main()