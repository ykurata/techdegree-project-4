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

        if choice in menu:
            clear_screen()
            menu[choice]()


def add_entry():
    """Add an entry."""
    name = input("Enter your name: ")
    title = input("Enter the task name: ")
    time = input("Enter the number of time you spent(minutes): ")
    print("Enter any additional notes. Press ctrl+d when finished.")
    note = sys.stdin.read().strip()

    if input("Save entry? Enter y or n: ").lower() != "n":
        Entry.create(name=name, title=title, time=time, note=note)
        print("The entry saved successfully.")


def search_entries():
    """Search previous entries."""
    search_options()
    search_choice = input("""
Enter the number associated with the search you want: """)
    clear_screen()
    try:
        search_choice = int(search_choice)
    except ValueError:
        print("{} is not a valid number.".format(search_choice) + "\n")
        search_entries()
    else:
        if search_choice == 1:
            find_name()
        elif search_choice == 2:
            clear_screen()
            print("e) Exact date search")
            print("r) Date range search")
            choice = input("\nEnter 'e' or 'r': ").lower().strip()
            if choice == "e":
                find_date()
            elif choice == "r":
                find_by_range()
        elif search_choice == 3:
            find_time()
        elif search_choice == 4:
            find_task_note()


def search_options():
    print("Please choose one of the following search options.")
    print("""
    1) Find by employee's name
    2) Find by date
    3) Find by time spent
    4) Find by task name or notes
    """)


def view_entries():
    """view previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear_screen()
        show_entry(entry)
        next_action(entry)


def show_names():
    """show enployee's name"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    clear_screen()
    print("-----Employee's name-----")
    for entry in entries:
        print("\n" + entry.name + "\n")


def find_name():
    """
    allow user to input employee's name,
    and show the employee's entry.
    """
    show_names()
    name_choice = input("\nPlease enter the name you want to search. ")
    entries = Entry.select().where(Entry.name.contains(name_choice))
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def find_date():
    """allow user to input the date and show the entry matched with the date"""
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


def find_by_range():
    """
    allow user to input date range,
    and show the entry matched with the date range.
    """
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


def find_time():
    """
    allow user to input the time,
    and show the entry matched with the time.
    """
    time_spent = input("\nEnter the time you spent(minutes): ")
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


def find_task_note():
    """
    allow user to input the taks name or note,
    and show the entry matched with the task name or note.
    """
    search = input("Enter task name or notes: ")
    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(
            (Entry.title.contains(search)) | (Entry.note.contains(search)))
    for entry in entries:
        show_entry(entry)
        next_action(entry)


def show_entry(entry):
    """show entry with timestamp."""
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
    """ask user to input next action."""
    print("""
n) next entry
d) delete entry
q) return to main menu""")
    action = input("\nPlease select your next action: " + "\n").lower().strip()
    if action == 'd':
        delete_entry(entry)
        print("Entry deleted.")
    elif action == "q":
        menu_loop()
        sys.exit()


def delete_entry(entry):
    """Delete an entry."""
    delete = input("Do you want to delete this entry? Enter y or n: ").lower()
    if delete == "y":
        entry.delete_instance()


menu = OrderedDict([
    ('a', add_entry),
    ('s', search_entries),
    ('v', view_entries),
])


if __name__ == '__main__':
    initialize()
    menu_loop()
