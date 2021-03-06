"""To-do list with Python and SQL"""
import sys
import os
import sqlite3
import kb

DATABASE = "./list.db"
TITLE = "Taskover"


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


def print_list(cursor, vim_cursor=0, vim_cursor_visible=True, numbering=False, extra_text=True):
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

        if vim_cursor_visible:
            print("* " if i == vim_cursor else "  ", end="")

        if numbering:
            print("{}. ".format(number), end="")
            number += 1

        if row[2]:
            print("[x] ", end="")
        else:
            print("[ ] ", end="")

        # Print the title
        if not row[2]:
            print("{}".format(row[1]))
        else:
            # Strike-through completed tasks
            print("\u0336".join("{}".format(row[1])) + "\u0336")

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
            print("""Taskover - A fast and hackable task list with Vim-like
           keybindings. Written in Python and SQL.

usage: taskover [options]

Options:
  help        Display this help message.
  list        Print the tasks ordered numerically and exit.

Program keywords:
  j - move downwards
  k - move upwards
  i - Insert a new task
  u - Update the description of a task
  m - Mark a task as done (or unmark a completed task)
  d - Delete a task
  q - Quit the program

Please report bugs to https://github.com/angelofallars/taskover""")

        # Print list
        elif sys.argv[1] == "list":
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()

            task_ids = print_list(cur,
                                  numbering=True,
                                  vim_cursor_visible=False,
                                  extra_text=False)

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
    footing_message = ""

    while True:
        clear()

        # Correct the position of the vim cursor if it's above the list
        list_length = cur.execute("SELECT COUNT(*) FROM tasklist")\
            .fetchone()[0]
        if vim_cursor >= list_length and list_length > 0:
            vim_cursor = list_length - 1

        task_ids = print_list(cur, vim_cursor)

        if len(task_ids) > 0:
            current_id = str(task_ids[vim_cursor])

        print("(i) Insert (u) Update (m) Mark (d) Delete (q) Quit")
        print(footing_message)

        # Get the current task list in rows
        cur.execute("SELECT id, title, finished FROM tasklist")
        rows = cur.fetchall()

        char = kb.getch().lower()

        # ==========
        # Vim Keybindings
        # ==========
        if char == 'j':
            if vim_cursor < len(task_ids) - 1:
                vim_cursor += 1
        elif char == 'k':
            if vim_cursor > 0:
                vim_cursor -= 1

        # ==========
        # Add
        # ==========
        elif char == 'i':
            footing_message = ""

            title = input("Title of task: $ ")

            # Continue if input title is blank
            if not title:
                continue

            cur.execute("""INSERT INTO tasklist(title)
                           VALUES(?)""", (title,))

        # ==========
        # Delete
        # ==========
        elif char == 'd':
            footing_message = ""

            if len(task_ids) > 0:
                print("Delete task \"{}\"? (D/n)".format(rows[vim_cursor][1]))

                char = kb.getch().lower()
                if char == 'd' or char == '\r':
                    cur.execute("""DELETE FROM tasklist WHERE id = ?""",
                                (current_id, ))

            else:
                footing_message = "No tasks to delete"

        # ==========
        # Mark as done
        # ==========
        elif char == 'm':

            if len(task_ids) > 0:
                cur.execute("""UPDATE tasklist
                               SET finished = NOT finished
                               WHERE id = ?""", (current_id, ))
            else:
                footing_message = "No tasks to mark as done"

        # ==========
        # Update
        # ==========
        elif char == 'u':

            if len(task_ids) > 0:
                new_description = input("New description:\n$ ")

                if not new_description:
                    continue

                cur.execute("""UPDATE tasklist
                               SET title = ?
                               WHERE id = ?""", (new_description,
                                                 current_id))

            else:
                footing_message = "No tasks to update"

        # ==========
        # Exit
        # ==========
        elif char == 'q':
            print("Do you really want to quit? (Y/n)")

            char = kb.getch().lower()
            if char == 'y' or char == '\r' or char == 'q':
                break

    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
