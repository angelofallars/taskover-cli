"""To-do list with Python and SQL"""
import sqlite3
from os import path, system
from os import name as os_name
from sys import argv

DATABASE = "./list.db"
TITLE = "Taskover (Beta)"


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
            print("Out of range.")
            continue

        # Reject negative numbers because they
        # work in lists and we accept only positive input
        if int(index) <= -1:
            print("Out of range.")
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

    print(TITLE)

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

    # Print footer
    if len(rows) > 1:
        task_count = "{} tasks".format(len(rows))
    elif len(rows) == 1:
        task_count = "1 task"
    else:
        task_count = "no tasks"

    print("--- {} ---".format(task_count))

    return task_ids


def main():
    """The main function"""

    # Help message
    if len(argv) > 1 and argv[1] == "--help":
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

        task_ids = print_list(cur)

        option = input("(i) Insert (u) Update (m) Mark as done (d) Delete (q) Quit\n$ ")\
        .lower()

        # Add
        if option == 'i':
            title = input("Title of task: $ ")

            cur.execute("""INSERT INTO tasklist(title)
                           VALUES(?)""", (title,))

        # Delete
        elif option == 'd':

            if len(task_ids) > 0:
                clear()

                task_ids = print_list(cur, numbering=True)

                print("Which task to delete?")
                id_to_delete = id_from_input(task_ids)

                cur.execute("""DELETE FROM tasklist WHERE id = ?""",
                            (id_to_delete, ))
            else:
                print("No tasks to delete")
                input()

        # Mark as done
        elif option == 'm':

            if len(task_ids) > 0:
                clear()

                task_ids = print_list(cur, numbering=True)

                print("Which task to mark as done/undone?")
                id_to_mark = id_from_input(task_ids)

                cur.execute("""UPDATE tasklist
                               SET finished = NOT finished
                               WHERE id = ?""", (id_to_mark, ))
            else:
                print("No tasks to mark as done")
                input()

        # Update
        elif option == 'u':
            clear()

            task_ids = print_list(cur, numbering=True)

            print("Which task description to update?")
            id_to_update = id_from_input(task_ids)

            # Continue to main menu if no input
            if not id_from_input:
                continue

            new_description = input("New description:\n$ ")

            # Continue to main menu if no input
            if not new_description:
                continue

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
