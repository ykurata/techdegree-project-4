import datetime
import unittest
import mock
from mock import patch
from peewee import *

import work_log_db
from work_log_db import Entry


class WorkLogTest(unittest.TestCase):
    def setUp(self):
        self.name = "Yasuko"
        self.title = "project4"
        self.time = 60
        self.note = "Test Notes"


    def test_add_new_entry(self):
        Entry.create(name=self.name,
                    title=self.title,
                    time=self.time,
                    note=self.note)
        entry = Entry.select().order_by(Entry.id.desc())
        Entry.delete_by_id(entry)


    @patch("builtins.input", side_effect=["q"])
    def test_menu_loop(self, mock_input):
        work_log_db.menu_loop()


    @patch("builtins.input", return_value=["yasuko", "project4", 60, "test notes"])
    def test_add_entry(self, mock_input):
        work_log_db.add_entry()


    @patch("builtins.input", return_value="s")
    def test_menu_input(self, mock_input):
        work_log_db.search_entries()


    @patch("builtins.input", return_value="v")
    def test_view_entries(self, mock_input):
        work_log_db.view_entries()


    @patch("builtins.input", return_value="a")
    def test_bad_search_entries(self, mock_input):
        with self.assertRaises(ValueError):
            int("a")


    def test_show_names(self):
        work_log_db.show_names()


    def test_next_action(self):
        work_log_db.next_action(entry)


    @patch("builtins.input", return_value="q")
    def test_next_action_input(self, mock_input):
        work_log_db.menu_loop()


    @patch("builtins.input", return_value="y")
    def test_delete_entry(self, mock_input):
        work_log_db.delete_entry(entry)


class FindNameTest(unittest.TestCase):
    def find_name(self):
        show_name()
        name_choice = input("Please enter the name you want to search. ")
        entries = Entry.select().where(Entry.name.contains(name_choice))
        for entry in entries:
            work_log_db.show_entry(entry)
            next_action(entry)

    @patch("builtins.input", return_value="Yasuko")
    def test_find_name(self, mock_input):
        work_log_db.find_name()


class FindDateTest(unittest.TestCase):
    def find_date(self):
        date = input("\nEnter the date YYYY-MM-DD format. ")
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print("{} doesn't seem to be a valid date".format(date))
            find_date()
        else:
            date = date.strftime('%Y-%m-%d')
            entries = Entry.select().order_by(Entry.timestamp.desc())
            entries = entries.where(Entry.timestamp.contains(date))
            for entry in entries:
                show_entry(entry)
                next_action(entry)

    @patch("builtins.input", return_value = "2018-04-07")
    def test_find_date(self, mock_input):
        work_log_db.find_date()


class FindByRangeTest(unittest.TestCase):
    def find_by_range(self):
        first_date = input("\nEnter the first date in YYYY-MM-DD format. ")
        second_date = input("Enter the second date in YYYY-MM-DD format. ")
        try:
            first_date = datetime.strptime(first_date, '%Y-%m-%d')
            second_date = datetime.strptime(second_date, '%Y-%m-%d')
        except ValueError:
            print("{} doesn't seem to be a valid date".format(first_date))
            print("{} doesn't seem to be a valid date".format(second_date))
            find_by_range()
        else:
            first_date = first_date.strftime('%Y-%m-%d')
            second_date = second_date.strftime('%Y-%m-%d')
            entries = Entry.select().order_by(Entry.timestamp.desc())
            entries = entries.where(first_date <= Entry.timestamp <= second_date)
            for entry in entries:
                show_entry(entry)
                next_action(entry)

    @patch("builtins.input", side_effect=["2018-04-06", "2018-04-07"])
    def test_find_by_range(self, mock_input):
        work_log_db.find_by_range()


class FindTimeTest(unittest.TestCase):
    def find_time(self):
        time_spent = input("Enter the time you spent(minutes): ")
        try:
            time_spent = int(time_spent)
        except ValueError:
            print("Please enter the number of time you spent.")
        else:
            entries = Entry.select().order_by(Entry.timestamp.desc())
            entries = entries.where(Entry.time==time_spent)
            for entry in entries:
                show_entry(entry)
                next_action(entry)

    @patch("builtins.input", return_value = 60)
    def test_find_time(self, mock_input):
        work_log_db.find_time()


class FindTaskNoteTest(unittest.TestCase):
    def find_task_note(self):
        search = input("Enter task name or notes: ")
        entries = Entry.select().order_by(Entry.timestamp.desc())
        entries = entries.where(
                (Entry.title.contains(search)) | (Entry.note.contains(search)))
        for entry in entries:
            show_entry(entry)
            next_action(entry)

    @patch("builtins.input", side_effect = ["project4", "Test Notes"])
    def test_find_task_note(self, mock_input):
        work_log_db.find_task_note()



if __name__ == '__main__':
    unittest.main()
