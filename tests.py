import datetime
import unittest

import work_log_db
from work_log_db import Entry


class WorkLogTests(unittest.TestCase):
    def test_create_new_entry(self):
        from work_log_db import create_new_entry
        test_entry = create_new_entry("test name", "test title", 1, "test notes")
        self.assertEqual(test_entry.name, "test name")
        test_entry.delete_instance()


    def test_valid_menu_input(self):
        from work_log_db import valid_menu_input
        self.assertTrue(valid_menu_input("a"))
        self.assertTrue(valid_menu_input("s"))
        self.assertTrue(valid_menu_input("v"))
        self.assertFalse(valid_menu_input("w"))
        self.assertFalse(valid_menu_input(""))


    def test_valid_search_input(self):
        from work_log_db import valid_search_input
        self.assertTrue(valid_search_input("a"))
        self.assertTrue(valid_search_input("b"))
        self.assertTrue(valid_search_input("c"))
        self.assertTrue(valid_search_input("d"))
        self.assertTrue(valid_search_input("e"))
        self.assertFalse(valid_search_input("f"))
        self.assertFalse(valid_search_input(""))


    def test_valid_name_input(self):
        from work_log_db import valid_name_input
        self.assertTrue(valid_name_input("Test name"))
        self.assertFalse(valid_name_input(""))


    def test_valid_title_input(self):
        from work_log_db import valid_title_input
        self.assertTrue(valid_title_input("Test title"))
        self.assertFalse(valid_title_input(""))


    def test_valid_time_input(self):
        from work_log_db import valid_time_input
        self.assertTrue(valid_time_input("5"))
        self.assertFalse(valid_time_input("a"))


    def test_valid_note_input(self):
        from work_log_db import valid_note_input
        self.assertTrue(valid_note_input("test note"))
        self.assertEqual(valid_note_input(""), None)


    def test_valid_date_input(self):
        from work_log_db import valid_date_input
        self.assertTrue(valid_date_input("2018-04-11"))
        self.assertFalse(valid_date_input("123"))


    def test_valid_date_range_input(self):
        from work_log_db import valid_date_range_input
        self.assertTrue(valid_date_range_input("2018-04-11", "2018-04-20"))
        self.assertFalse(valid_date_range_input("123", "abc"))


    def test_valid_find_task_note(self):
        from work_log_db import valid_find_task_note
        self.assertTrue(valid_find_task_note("test note"))
        self.assertFalse(valid_find_task_note(""))


    def test_show_entry(self):
        from work_log_db import create_new_entry
        test_entry = create_new_entry("test name", "test title", 1, "test notes")
        from work_log_db import show_entry
        show_entry(test_entry)
        test_entry.delete_instance()


    def test_valid_next_action_input(self):
        from work_log_db import valid_next_action_input
        self.assertTrue(valid_next_action_input("d"))
        self.assertFalse(valid_next_action_input("1"))


    def test_show_name(self):
        work_log_db.show_names()


if __name__ == '__main__':
    unittest.main()
