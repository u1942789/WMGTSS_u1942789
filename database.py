import sqlite3


def initialise_database():
    initialise_accounts()
    initialise_qanda_boards()


def initialise_accounts():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS accounts""")
    conn.commit()
    c.execute("""CREATE TABLE accounts (
    username text,
    password text,
    is_admin integer
    )""")
    conn.commit()
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", ('Tutor1', 'password', 1))
    conn.commit()
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", ('ypark1', 'pass', 1))
    conn.commit()
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", ('Student123', '123', 0))
    conn.commit()
    c.execute("INSERT INTO accounts VALUES (?, ?, ?)", ('stu1', 'stu1', 0))
    conn.commit()
    conn.close()


def initialise_qanda_boards():
    conn = sqlite3.connect("qanda_boards.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS qanda_boards""")
    conn.commit()
    c.execute("""CREATE TABLE qanda_boards (
    qanda_board_id integer,
    topic text,
    creator text
    )""")
    conn.commit()
    c.execute("INSERT INTO qanda_boards VALUES (?, ?, ?)", (1, "Computer Science", 'ypark1'))
    conn.commit()
    c.execute("INSERT INTO qanda_boards VALUES (?, ?, ?)", (2, 'Mathematics', 'tutor1'))
    conn.commit()
    conn.close()

# c.execute("SELECT * FROM accounts")
# Fetch first row from query.
# print(c.fetchall())
