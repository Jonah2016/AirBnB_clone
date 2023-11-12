#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def test_two_users_diff_created_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def test_two_users_diff_updated_at(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.updated_at, usr2.updated_at)

    def test_str_rep(self):
        d_time = datetime.today()
        d_time_rep = repr(d_time)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = d_time
        usrstr = usr.__str__()
        self.assertIn("[User] (123456)", usrstr)
        self.assertIn("'id': '123456'", usrstr)
        self.assertIn("'created_at': " + d_time_rep, usrstr)
        self.assertIn("'updated_at': " + d_time_rep, usrstr)

    def test_unused_args(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_init_with_kwargs(self):
        d_time = datetime.today()
        d_time_iso = d_time.isoformat()
        usr = User(id="345", created_at=d_time_iso, updated_at=d_time_iso)
        self.assertEqual(usr.id, "345")
        self.assertEqual(usr.created_at, d_time)
        self.assertEqual(usr.updated_at, d_time)

    def test_init_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        usr = User()
        sleep(0.05)
        fst_updated_at = usr.updated_at
        usr.save()
        self.assertLess(fst_updated_at, usr.updated_at)

    def test_two_saves(self):
        usr = User()
        sleep(0.05)
        fst_updated_at = usr.updated_at
        usr.save()
        sec_updated_at = usr.updated_at
        self.assertLess(fst_updated_at, sec_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(sec_updated_at, usr.updated_at)

    def test_save_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_save_updates_file(self):
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as f:
            self.assertIn(usrid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def test_to_dict_contains_added_attr(self):
        usr = User()
        usr.middle_name = "Holberton"
        usr.my_number = 98
        self.assertEqual("Holberton", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def test_to_dict_datetime_attr_are_strs(self):
        usr = User()
        usr_dict = usr.to_dict()
        self.assertEqual(str, type(usr_dict["id"]))
        self.assertEqual(str, type(usr_dict["created_at"]))
        self.assertEqual(str, type(usr_dict["updated_at"]))

    def test_to_dict_output(self):
        d_time = datetime.today()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = d_time
        ts_dict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': d_time.isoformat(),
            'updated_at': d_time.isoformat(),
        }
        self.assertDictEqual(usr.to_dict(), ts_dict)

    def test_contrast_to_dict_dunder_dict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_to_dict_with_arg(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
