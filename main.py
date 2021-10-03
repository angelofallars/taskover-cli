"""To-do list with Python and SQL"""
import sqlite3
from os import path, system
from os import name as os_name
from sys import argv

DATABASE = "./list.db"
TITLE = "========TASKOVER BETA============"
SEPARATOR = "================================="


def clear():
    """Clear the screen."""
    system("cls" if os_name == "nt" else "clear")


def id_from_input(task_ids):
    """Get an ID of a task from user input"""

    while True:
        index = input("$ ")

        # Return none if no input
        if index == "":
            return None

        try:
            id = task_ids[int(index) - 1]
        except (IndexError, ValueError):
            print("That task doesn't exist.")
            continue

        # Reject negative numbers because they
        # work in lists and we accept only positive input
        if int(index) <= -1:
            print("That task doesn't exist.")
            continue

        return id


def print_list(cursor, numbering=False):
    """Print the current todo list.

    Returns the IDs of the tasks ordered in a list.

    Args:
        cursor - the SQL cursor
        numbering - add numbering to the displayed list"""

    task_ids = []

    # Select the list of tasks
    cursor.execute("SELECT id, title, finished FROM tasklist")

    # Fetch the results
    rows = cursor.fetchall()

    # Display numbers if needed to print numbers of list
    number = 1

    for row in rows:
        task_ids.append(row[0])

        if numbering:
            print("{}. ".format(number), end="")
            number += 1

        if row[2]:
            print("[x] ", end="")
        else:
            print("[ ] ", end="")

        # Print the title
        print("{}".format(row[1]))

    return task_ids


def main():
    """The main function"""

    # Help message
    if argv[1] == "--help":
        print("""Taskover - A todo-list by Angelo-F
usage: python [options]

--help
   Display this help message.

Program keywords:
- i - Insert a new task
- u - Update the description of a task
- m - Mark a task as done (or unmark a completed task)
- d - Delete a task
- q - Quit the program

Please report bugs to https://github.com/angelofallars/taskover""")
        return 0


    print("Taskover - A todo-list by Angelo-F")

    # Check if a list.db file exists
    if not path.isfile(DATABASE):
        # Create a database because it doesn't exist
        open(DATABASE, "w", encoding="utf-8").close()
        print("Created new SQL database.")

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        # Make a SQL table in the database
        cur.execute("""CREATE TABLE tasklist
                       (id INTEGER PRIMARY KEY, title TEXT,
                        finished INTEGER DEFAULT 0)
                       """)

        # Save and close the database
        con.commit()
        con.close()

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    while True:
        clear()

        print(TITLE)
        task_ids = print_list(cur)
        print(SEPARATOR)
        option = input("(i) Insert (u) Update (m) Mark as done (d) Delete (q) Quit\n$ ")\
        .lower()

        # Add
        if option == 'i':
            title = input("Title of task: $ ")

            cur.execute("""INSERT INTO tasklist(title)
                           VALUES(?)""", (title,))

        # Delete
        elif option == 'd':
            clear()
            print(TITLE)
            task_ids = print_list(cur, numbering=True)
            print(SEPARATOR)

            print("Which task to delete?")
            id_to_delete = id_from_input(task_ids)

            cur.execute("""DELETE FROM tasklist WHERE id = ?""",
                        (id_to_delete, ))

        # Mark as done
        elif option == 'm':
            clear()
            print(TITLE)
            task_ids = print_list(cur, numbering=True)
            print(SEPARATOR)

            print("Which task to mark as done/undone?")
            id_to_mark = id_from_input(task_ids)

            cur.execute("""UPDATE tasklist
                           SET finished = NOT finished
                           WHERE id = ?""", (id_to_mark, ))

        # Update
        elif option == 'u':
            clear()
            print(TITLE)
            task_ids = print_list(cur, numbering=True)
            print(SEPARATOR)

            print("Which task description to update?")
            id_to_update = id_from_input(task_ids)

            new_description = input("New description:\n$ ")

            cur.execute("""UPDATE tasklist
                           SET title = ?
                           WHERE id = ?""", (new_description, id_to_update,))

        # Exit
        elif option == 'q':
            print("Thanks for running my program!")
            break
  
        # Continue the program as usual if no/wrong input
        else:
            pass

    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
