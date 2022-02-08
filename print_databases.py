import sqlite3

conn = sqlite3.connect("accounts.db")
c = conn.cursor()
c.execute("SELECT * FROM accounts")
for x in c.fetchall():
    print(x)
conn.commit()
conn.close()

print("=====")

conn = sqlite3.connect("qanda_boards.db")
c = conn.cursor()
c.execute("SELECT * FROM qanda_boards")
for x in c.fetchall():
    print(x)
conn.commit()
conn.close()


print("=====")

conn = sqlite3.connect("questions.db")
c = conn.cursor()
c.execute("SELECT * FROM questions")
for x in c.fetchall():
    print(x)
conn.commit()
conn.close()
