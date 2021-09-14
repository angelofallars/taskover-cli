"""To-do list with Python and SQL"""
import sqlite3
from os import path

DATABASE = "./list.db"


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
                        done INTEGER)
                       """)

        # First task
        cur.execute("""INSERT INTO tasklist VALUES(1,'Clean the room', 'You need to clean your room now!')""")
        # Second task
        cur.execute("""INSERT INTO tasklist VALUES(2,'Do the biology homework','')""")
        # Third task
        cur.execute("""INSERT INTO tasklist VALUES(3,'Make a sandwich','')""")

        # Save and close the database
        con.commit()
        con.close()

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()

    # Select the list of tasks
    cur.execute("SELECT id, title, description FROM tasklist")
    rows = cur.fetchall()

    # Print them out
    for row in rows:
        print("TASK {}: {}".format(row[0], row[1]))
        if row[2] != '':
            print("    {}".format(row[2]))

    con.commit()
    con.close()
    return 0


if __name__ == "__main__":
    main()
