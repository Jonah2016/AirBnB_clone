#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objs(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attr(self):
        stt2 = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(stt2))
        self.assertNotIn("name", stt2.__dict__)

    def test_two_states_unique_ids(self):
        stt1 = State()
        stt2 = State()
        self.assertNotEqual(stt1.id, stt2.id)

    def test_two_states_different_created_at(self):
        stt1 = State()
        sleep(0.05)
        stt2 = State()
        self.assertLess(stt1.created_at, stt2.created_at)

    def test_two_states_different_updated_at(self):
        stt1 = State()
        sleep(0.05)
        stt2 = State()
        self.assertLess(stt1.updated_at, stt2.updated_at)

    def test_str_rep(self):
        d_time = datetime.today()
        d_time_rep = repr(d_time)
        stt2 = State()
        stt2.id = "123456"
        stt2.created_at = stt2.updated_at = d_time
        ststr = stt2.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + d_time_rep, ststr)
        self.assertIn("'updated_at': " + d_time_rep, ststr)

    def test_unused_args(self):
        stt2 = State(None)
        self.assertNotIn(None, stt2.__dict__.values())

    def test_init_with_kwargs(self):
        d_time = datetime.today()
        d_time_iso = d_time.isoformat()
        stt2 = State(id="345", created_at=d_time_iso, updated_at=d_time_iso)
        self.assertEqual(stt2.id, "345")
        self.assertEqual(stt2.created_at, d_time)
        self.assertEqual(stt2.updated_at, d_time)

    def test_init_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        stt2 = State()
        sleep(0.05)
        fst_updated_at = stt2.updated_at
        stt2.save()
        self.assertLess(fst_updated_at, stt2.updated_at)

    def test_two_saves(self):
        stt2 = State()
        sleep(0.05)
        fst_updated_at = stt2.updated_at
        stt2.save()
        sec_updated_at = stt2.updated_at
        self.assertLess(fst_updated_at, sec_updated_at)
        sleep(0.05)
        stt2.save()
        self.assertLess(sec_updated_at, stt2.updated_at)

    def test_save_with_arg(self):
        stt2 = State()
        with self.assertRaises(TypeError):
            stt2.save(None)

    def test_save_updates_file(self):
        stt2 = State()
        stt2.save()
        sttid = "State." + stt2.id
        with open("file.json", "r") as f:
            self.assertIn(sttid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        stt2 = State()
        self.assertIn("id", stt2.to_dict())
        self.assertIn("created_at", stt2.to_dict())
        self.assertIn("updated_at", stt2.to_dict())
        self.assertIn("__class__", stt2.to_dict())

    def test_to_dict_contains_added_attr(self):
        stt2 = State()
        stt2.middle_name = "Holberton"
        stt2.my_number = 98
        self.assertEqual("Holberton", stt2.middle_name)
        self.assertIn("my_number", stt2.to_dict())

    def test_to_dict_datetime_attr_are_strs(self):
        stt2 = State()
        stt_dict = stt2.to_dict()
        self.assertEqual(str, type(stt_dict["id"]))
        self.assertEqual(str, type(stt_dict["created_at"]))
        self.assertEqual(str, type(stt_dict["updated_at"]))

    def test_to_dict_output(self):
        d_time = datetime.today()
        stt2 = State()
        stt2.id = "123456"
        stt2.created_at = stt2.updated_at = d_time
        ts_dict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': d_time.isoformat(),
            'updated_at': d_time.isoformat(),
        }
        self.assertDictEqual(stt2.to_dict(), ts_dict)

    def test_contrast_to_dict_dunder_dict(self):
        stt2 = State()
        self.assertNotEqual(stt2.to_dict(), stt2.__dict__)

    def test_to_dict_with_arg(self):
        stt2 = State()
        with self.assertRaises(TypeError):
            stt2.to_dict(None)


if __name__ == "__main__":
    unittest.main()
