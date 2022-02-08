def initialise_database(c, conn):
    c.execute("""DROP TABLE accounts""")
    conn.commit()
    c.execute("""CREATE TABLE accounts (
    username text,
    password text,
    is_admin integer
    )""")
    conn.commit()
    c.execute("INSERT INTO accounts VALUES ('Tutor1', 'password', 1)")
    conn.commit()
    c.execute("INSERT INTO accounts VALUES ('ypark1', 'pass', 1)")
    conn.commit()
    c.execute("INSERT INTO accounts VALUES ('Student123', '123', 0)")
    conn.commit()
    c.execute("INSERT INTO accounts VALUES ('stu1', 'stu1', 0)")
    conn.commit()
    conn.close()

# c.execute("SELECT * FROM accounts")
# Fetch first row from query.
# print(c.fetchall())
