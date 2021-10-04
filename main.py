"""To-do list with Python and SQL"""
import sys, os 
import sqlite3, kb

DATABASE = "./list.db"
TITLE = "Taskover (Beta)"

def clear():
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")


def id_from_input(task_ids):
    """Get an ID of a task from user input"""

    while True:
        index = kb.getch()

        # Return none if no input
        if index == "":
            return None

        try:
            id = task_ids[int(index) - 1]
        except (IndexError, ValueError):
            print("Out of range.")
            continue

        # Reject zero and negative numbers because they
        # work in lists and we accept only positive input
        if int(index) <= 0:
            print("Out of range.")
            continue

        return id


def print_list(cursor, vim_cursor=0, numbering=False, extra_text=True):
    """Print the current todo list.

    Returns the IDs of the tasks ordered in a list.

    Args:
        cursor - the SQL cursor
        vim_cursor - the vim cursor that is manipulated by j, k
        numbering - add numbering to the displayed list
        extra_text - If there should be extra text above and below the tasks"""

    task_ids = []

    # Select the list of tasks
    cursor.execute("SELECT id, title, finished FROM tasklist")

    # Fetch the results
    rows = cursor.fetchall()

    # Display numbers if needed to print numbers of list
    number = 1

    if extra_text:
        print(TITLE)

    # Print the tasks
    for i in range(len(rows)):
        row = rows[i]

        task_ids.append(row[0])

        print("* " if i == vim_cursor else "  ", end="")

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

    if extra_text:
        print("--- {} ---".format(task_count))

    return task_ids


def main():
    """The main function"""

    if len(sys.argv) > 1:

        if sys.argv[1] == "help":
            # Help message
            print("""Taskover - A fast and hackable task list written in Python and SQL.
usage: taskover [options]

help
  Display this help message.

list
  Print the tasks ordered numerically and exit. Useful for scripting.

Program keywords:
- i - Insert a new task
- u - Update the description of a task
- m - Mark a task as done (or unmark a completed task)
- d - Delete a task
- q - Quit the program

Please report bugs to https://github.com/angelofallars/taskover""")
        
        # Print list
        elif sys.argv[1] == "list":
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()

            task_ids = print_list(cur, numbering=True, extra_text=False)

            if not task_ids:
                print("No tasks")

        else:
            print("""usage: taskover [options]
see 'taskover help' for more options""")

        return 0


    print("Taskover - A todo-list by Angelo-F")

    # Check if a list.db file exists
    if not os.path.isfile(DATABASE):
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

    vim_cursor = 0

    while True:
        clear()

        task_ids = print_list(cur, vim_cursor=vim_cursor)

        print("(i) Insert (u) Update (m) Mark as done (d) Delete (q) Quit\n$ ",
                end="")

        # Commit every time so updates are instantly reflected in database
        con.commit()

        char = kb.getch().lower()
        print("")

        if char == 'j':
            if vim_cursor < len(task_ids) - 1:
                vim_cursor += 1

        elif char == 'k':
            if vim_cursor > 0:
                vim_cursor -= 1

        # Add
        elif char == 'i':
            title = input("Title of task: $ ")

            # Continue if input title is blank
            if not title:
                continue

            cur.execute("""INSERT INTO tasklist(title)
                           VALUES(?)""", (title,))

        # Delete
        elif char == 'd':

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
        elif char == 'm':

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
        elif char == 'u':

            if len(task_ids) > 0:
                clear()

                task_ids = print_list(cur, numbering=True)

                print("Which task description to update?")
                id_to_update = id_from_input(task_ids)

                # Continue to main menu if no input
                if not id_from_input:
                    continue

                new_description = input("New description:\n$ ")

                if not new_description:
                    continue

                cur.execute("""UPDATE tasklist
                               SET title = ?
                               WHERE id = ?""", (new_description, id_to_update,))
            else:
                print("No tasks to update")
                input()

        # Exit
        elif char == 'q':
            print("Do you really want to quit? (Y/n)")
            char = kb.getch().lower()

            if char == 'y' or char == '\r':
                break


    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
