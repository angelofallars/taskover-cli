"""To-do list with Python and SQL"""
import sqlite3
from os import path, system
from os import name as os_name

DATABASE = "./list.db"


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
    cursor.execute("SELECT id, title, description, finished FROM tasklist")

    # Fetch the results
    rows = cursor.fetchall()

    # Display numbers if needed to print numbers of list
    number = 1

    for row in rows:
        task_ids.append(row[0])

        if numbering:
            print("{}. ".format(number), end="")
            number += 1

        if row[3]:
            print("[x] ", end="")
        else:
            print("[ ] ", end="")

        # Print the title
        print("{}".format(row[1]))

        # Print the description (Don't print blank descriptions)
        if row[2] != "":
            print("      {}".format(row[2]))

    return task_ids


def main():
    """The main function"""
    print("TODO LIST by Angelo")

    # Check if a list.db file exists
    if not path.isfile(DATABASE):
        # Create a database because it doesn't exist
        open(DATABASE, "w", encoding="utf-8").close()
        print("Created new SQL database.")

        con = sqlite3.connect(DATABASE)
        cur = con.cursor()

        # Make a SQL table in the database
        cur.execute("""CREATE TABLE tasklist
                       (id INTEGER PRIMARY KEY, title TEXT, description TEXT,
                        finished INTEGER DEFAULT 0)
                       """)

        # First task
        # cur.execute("""INSERT INTO tasklist(title, description)
        #               VALUES('Clean the room',
        #                      'You need to clean your room now!')""")

        # Save and close the database
        con.commit()
        con.close()

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    while True:
        clear()

        print("========TASKOVER BETA============")
        task_ids = print_list(cur)
        print("=================================")
        option = input("(1) Add (2) Delete (3) Mark as done (4) Exit\n$ ")

        # Add
        if option == '1':
            title = input("Title of task: $ ")
            description = input("Description of task (Optional): $ ")

            cur.execute("""INSERT INTO tasklist(title, description)
                           VALUES(?, ?)""", (title, description))

        # Delete
        elif option == '2':
            clear()
            print("========TASKOVER BETA============")
            task_ids = print_list(cur, numbering=True)
            print("=================================")

            print("Which task to delete?")
            id_to_delete = id_from_input(task_ids)

            cur.execute("""DELETE FROM tasklist WHERE id = ?""",
                        (id_to_delete, ))

        # Mark as done
        elif option == '3':
            clear()
            print("========TASKOVER BETA============")
            task_ids = print_list(cur, numbering=True)
            print("=================================")

            print("Which task to mark as done/undone?")
            id_to_mark = id_from_input(task_ids)

            cur.execute("""UPDATE tasklist
                           SET finished = NOT finished
                           WHERE id = ?""", (id_to_mark, ))

        # Exit
        elif option == '4':
            print("Thanks for running my program!")
            break

        else:
            print("Unrecognized input. Try again.")
            input()

    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
