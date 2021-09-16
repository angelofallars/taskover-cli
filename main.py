"""To-do list with Python and SQL"""
import sqlite3
from os import path
from os import system
from os import name as os_name

DATABASE = "./list.db"


def clear():
    """Clear the screen.

    Terminal command for clearing screen varies depending
    on the operating system"""
    if os_name == "nt":
        system("cls")
    else:
        system("clear")


def printlist(cursor):
    """Print the current todo list.

    Returns the IDs of the tasks ordered in a list."""
    task_ids = []

    # Select the list of tasks
    cursor.execute("SELECT id, title, description, finished FROM tasklist")

    # Fetch the results
    rows = cursor.fetchall()

    for row in rows:
        task_ids.append(row[0])

        if row[3]:
            print("[x] ", end="")
        else:
            print("[ ] ", end="")

        print("{}\n    {}".format(row[1], row[2]))

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
        cur.execute("""INSERT INTO tasklist(title, description)
                       VALUES('Clean the room',
                              'You need to clean your room now!')""")
        # Second task
        cur.execute("""INSERT INTO tasklist(title, description, finished)
                       VALUES('Do the biology homework', NULL, 1)""")
        # Third task
        cur.execute("""INSERT INTO tasklist(title, description)
                       VALUES('Make a sandwich', NULL)""")

        # Save and close the database
        con.commit()
        con.close()

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    while True:
        clear()
        print("===== TODO LIST BY ANGELO-F =====")

        task_ids = printlist(cur)

        option = input("[1] Add [2] Delete [3] Exit\n$ ")

        if option == '1':
            title = input("Title of task: ")
            description = input("Description of task (Can be blank): ")

            cur.execute("""INSERT INTO tasklist(title, description)
                           VALUES(?, ?)""", (title, description))

        elif option == '2':
            print("Which task to delete?")
            deleted_index = int(input("$ ")) - 1
            id_to_delete = task_ids[deleted_index]
            print(id_to_delete)

            cur.execute("""DELETE FROM tasklist WHERE id = ?""",
                        (id_to_delete, ))

        elif option == '3':
            print("Thanks for running my program!")
            break

        else:
            print("Unrecognized input. Try again.")

    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
