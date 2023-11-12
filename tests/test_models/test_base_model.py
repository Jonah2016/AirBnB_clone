#!/usr/bin/python3
"""Defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        b_mod1 = BaseModel()
        b_mod2 = BaseModel()
        self.assertNotEqual(b_mod1.id, b_mod2.id)

    def test_two_models_diff_created_at(self):
        b_mod1 = BaseModel()
        sleep(0.05)
        b_mod2 = BaseModel()
        self.assertLess(b_mod1.created_at, b_mod2.created_at)

    def test_two_models_diff_updated_at(self):
        b_mod1 = BaseModel()
        sleep(0.05)
        b_mod2 = BaseModel()
        self.assertLess(b_mod1.updated_at, b_mod2.updated_at)

    def test_str_rep(self):
        d_time = datetime.today()
        d_time_rep = repr(d_time)
        b_mod = BaseModel()
        b_mod.id = "123456"
        b_mod.created_at = b_mod.updated_at = d_time
        b_mod_str = b_mod.__str__()
        self.assertIn("[BaseModel] (123456)", b_mod_str)
        self.assertIn("'id': '123456'", b_mod_str)
        self.assertIn("'created_at': " + d_time_rep, b_mod_str)
        self.assertIn("'updated_at': " + d_time_rep, b_mod_str)

    def test_unused_args(self):
        b_mod = BaseModel(None)
        self.assertNotIn(None, b_mod.__dict__.values())

    def test_init_with_kwargs(self):
        d_time = datetime.today()
        d_time_iso = d_time.isoformat()
        b_mod = BaseModel(id="345", created_at=d_time_iso, updated_at=d_time_iso)
        self.assertEqual(b_mod.id, "345")
        self.assertEqual(b_mod.created_at, d_time)
        self.assertEqual(b_mod.updated_at, d_time)

    def test_init_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_init_with_args_and_kwargs(self):
        d_time = datetime.today()
        d_time_iso = d_time.isoformat()
        b_mod = BaseModel("12", id="345", created_at=d_time_iso, updated_at=d_time_iso)
        self.assertEqual(b_mod.id, "345")
        self.assertEqual(b_mod.created_at, d_time)
        self.assertEqual(b_mod.updated_at, d_time)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
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
        b_mod = BaseModel()
        sleep(0.05)
        fst_updated_at = b_mod.updated_at
        b_mod.save()
        self.assertLess(fst_updated_at, b_mod.updated_at)

    def test_two_saves(self):
        b_mod = BaseModel()
        sleep(0.05)
        fst_updated_at = b_mod.updated_at
        b_mod.save()
        sec_updated_at = b_mod.updated_at
        self.assertLess(fst_updated_at, sec_updated_at)
        sleep(0.05)
        b_mod.save()
        self.assertLess(sec_updated_at, b_mod.updated_at)

    def test_save_with_arg(self):
        b_mod = BaseModel()
        with self.assertRaises(TypeError):
            b_mod.save(None)

    def test_save_updates_file(self):
        b_mod = BaseModel()
        b_mod.save()
        b_mod_id = "BaseModel." + b_mod.id
        with open("file.json", "r") as f:
            self.assertIn(b_mod_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        b_mod = BaseModel()
        self.assertTrue(dict, type(b_mod.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        b_mod = BaseModel()
        self.assertIn("id", b_mod.to_dict())
        self.assertIn("created_at", b_mod.to_dict())
        self.assertIn("updated_at", b_mod.to_dict())
        self.assertIn("__class__", b_mod.to_dict())

    def test_to_dict_contains_added_attr(self):
        b_mod = BaseModel()
        b_mod.name = "Holberton"
        b_mod.my_number = 98
        self.assertIn("name", b_mod.to_dict())
        self.assertIn("my_number", b_mod.to_dict())

    def test_to_dict_datetime_attr_are_strs(self):
        b_mod = BaseModel()
        bm_dict = b_mod.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_to_dict_output(self):
        d_time = datetime.today()
        b_mod = BaseModel()
        b_mod.id = "123456"
        b_mod.created_at = b_mod.updated_at = d_time
        ts_dict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': d_time.isoformat(),
            'updated_at': d_time.isoformat()
        }
        self.assertDictEqual(b_mod.to_dict(), ts_dict)

    def test_contrast_to_dict_dunder_dict(self):
        b_mod = BaseModel()
        self.assertNotEqual(b_mod.to_dict(), b_mod.__dict__)

    def test_to_dict_with_arg(self):
        b_mod = BaseModel()
        with self.assertRaises(TypeError):
            b_mod.to_dict(None)


if __name__ == "__main__":
    unittest.main()
