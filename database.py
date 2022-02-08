import sqlite3


def initialise_database():
    initialise_accounts()
    initialise_qanda_boards()
    initialise_questions()


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


def initialise_questions():
    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("""DROP TABLE IF EXISTS questions""")
    conn.commit()
    c.execute("""CREATE TABLE questions (
    question_id integer,
    qanda_board_id integer,
    question text,
    asker text,
    date text,
    answer text,
    answerer text,
    answer_date text,
    likes text,
    comments text
    )""")
    conn.commit()
    c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (1, 1, "How do I use HTML?", "Student1",
                                                                              "13/11/2021",
                                                                              "This is the answer on how to use HTML.",
                                                                              "Tutor70", "02/02/2022",
                                                                              str(["Student1", "Student2", "Student3"]),
                                                                              str([])))
    conn.commit()
    c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (2, 1,
                                                                              "Has the assignment been released yet?",
                                                                              "Student2", "15/11/2021", "", "", "",
                                                                              str(["Student2", "Student3"]), str([])))
    conn.commit()
    conn.close()
