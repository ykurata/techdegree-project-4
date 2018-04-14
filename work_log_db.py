from collections import OrderedDict
from datetime import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('work_log.db')


class Entry(Model):
    name = CharField(max_length=100)
    title = CharField(max_length=100)
    time = IntegerField(default=0)
    note = TextField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and tables if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        clear_screen()
        print("Welcome to Work Log!\n")
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("Please select your next action. ").lower().strip()
        if choice == "q":
            break
        if valid_menu_input(choice):
            clear_screen()
            menu[choice]()


def valid_menu_input(choice):
    """Check if the choice is in the menu."""
    if choice in menu.keys():
        return True
    else:
        print("Please enter again!")
        return False


def add_entry():
    """Create a new entry."""
    while True:
        name = input("Enter your name: ").strip()
        if valid_name_input(name):
            break
    while True:
        title = input("Enter the task name: ").strip()
        if valid_title_input(title):
            break
    while True:
        time = input("Enter the number of time you spent(minutes): ").strip()
        if valid_time_input(time):
            break
    print("Enter any additional notes. Press ctrl+d when finished.")
    note = sys.stdin.read().strip()
    valid_note_input(note)
    create_new_entry(name, title, time, note)


def create_new_entry(name, title, time, note):
    """Create a new entry"""
    print("The entry saved successfully.")
    return Entry.create(name=name, title=title, time=time, note=note)


def valid_name_input(name):
    """Check if the employee name is valid."""
    if len(name) != 0:
        clear_screen()
        return True
    else:
        clear_screen()
        print("Please enter a name again!")
        return False


def valid_title_input(title):
    """Check if the title is valid."""
    if len(title) != 0:
        clear_screen()
        return True
    else:
        clear_screen()
        print("Please enter a title again!")
        return False


def valid_time_input(time):
    """Check if the time is valid."""
    if time.isdigit():
        time = int(time)
        clear_screen()
        return True
    else:
        clear_screen()
        print("Please enter time spent again!")
        return False


def valid_note_input(note):
    """Checks if task note is valid."""
    if len(note) != 0:
        clear_screen()
        return True
    elif len(note) == 0:
        return None


def search_entries():
    """Search previous entries."""
    choice = None

    while choice != "q":
        clear_screen()
        print("Enter 'q' to return menu\n")
        for key, value in search_option.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("""
Pease select your search option: """)
        if choice == "q":
            menu_loop()
        if valid_search_input(choice):
            clear_screen()
            search_option[choice]()


def valid_search_input(choice):
    """Check if the choice is in the search options."""
    if choice in search_option.keys():
        return True
    else:
        print("{} is not a valid number".format(choice))
        return False


def view_entries():
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear_screen()
        show_entry(entry)
        next_action(entry)


def show_names():
    """Show enployee's name."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    clear_screen()
    print("-----Employee's name-----")
    for entry in entries:
        print("\n" + entry.name + "\n")


def find_name():
    """Find by employee's name"""
    show_names()
    while True:
        name = input("\nPlease enter the name you want to search. ")
        if valid_name_input(name):
            break
    entries = Entry.select().where(Entry.name.contains(name))
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def find_exact_date():
    """Find by exact date."""
    while True:
        date = input("\nEnter the date YYYY-MM-DD format. ")
        if valid_date_input(date):
            break
    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(Entry.timestamp.contains(date))
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def valid_date_input(date):
    """Check if the date is valid."""
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        clear_screen()
        print("{} doesn't seem to be a valid date".format(date))
        return False


def find_by_range():
    """Find by date range."""
    while True:
        first_date = input("\nEnter the first date in YYYY-MM-DD format. ")
        second_date = input("Enter the second date in YYYY-MM-DD format. ")
        if valid_date_range_input(first_date, second_date):
            break
    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(first_date <= Entry.timestamp <= second_date)
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def valid_date_range_input(first_date, second_date):
    """Check if the date range is valid."""
    try:
        first_date = datetime.strptime(first_date, '%Y-%m-%d')
        second_date = datetime.strptime(second_date, '%Y-%m-%d')
        return first_date, second_date
    except ValueError:
        clear_screen()
        print("{} doesn't seem to be a valid date".format(first_date))
        print("{} doesn't seem to be a valid date".format(second_date))
        return False


def find_time():
    """Find by time spent."""
    while True:
        time_spent = input("\nEnter the time you spent(minutes): ")
        if valid_time_input(time_spent):
            break
    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(Entry.time==time_spent)
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def find_task_note():
    """Find by task name or note."""
    while True:
        search = input("Enter task name or notes: ")
        if valid_find_task_note(search):
            break
    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(
            (Entry.title.contains(search)) | (Entry.note.contains(search)))
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def valid_find_task_note(search):
    """Check if the search input of task name or note is valid."""
    if len(search) != 0:
        return True
    elif len(search) == 0:
        clear_screen()
        print("Please enter task name or note")
        return False


def show_entry(entry):
    """Show entry with timestamp."""
    clear_screen()
    timestamp = entry.timestamp.strftime('%Y-%m-%d, %I:%M%p')
    print(timestamp)
    print('='*len(timestamp))
    print("""
Employee's name: {}
Task name: {}
Time spent: {}
Note:
{}""".format(entry.name, entry.title, entry.time, entry.note))
    print('\n\n' + '='*len(timestamp))


def next_action(entry):
    """Ask user to input next action."""
    print("""
n) next entry
d) delete entry
q) return to main menu""")
    while True:
        action = input("\nPlease select your next action: " + "\n").lower().strip()
        if valid_next_action_input(action):
            break
    if action == 'd':
        return delete_entry(entry)
    elif action == "q":
        menu_loop()
        sys.exit()


def valid_next_action_input(action):
    """Check if the action is in search options"""
    next_action = ["n", "d", "q"]
    if action in next_action:
        return True
    else:
        print("{} is not a valid choice".format(action))
        return False


def delete_entry(entry):
    """Delete an entry."""
    if input("""
Do you want to delete this entry? Enter y or n: """).lower() == "y":
        entry.delete_instance()


menu = OrderedDict([
    ('a', add_entry),
    ('s', search_entries),
    ('v', view_entries),
])


search_option = OrderedDict([
    ('a', find_name),
    ('b', find_exact_date),
    ('c', find_by_range),
    ('d', find_time),
    ('e', find_task_note),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
