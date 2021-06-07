import sqlite3

conn = sqlite3.connect('pong.db')
c = conn.cursor()


#       c.execute("""CREATE TABLE pong  (
#       first_name TEXT,
#       last_name TEXT,
#       email TEXT
#       )""")

#       adding score column to the database
#       c.execute("ALTER TABLE pong ADD COLUMN score ")

#c.execute("SELECT * FROM pong WHERE first_name = (?) AND last_name =(?) AND email = (?)",(name,last_name,email))
    #items = c.fetchall()

def show_all():
    # show everything in the date base
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()
    c.execute("SELECT * FROM pong ")
    items = c.fetchall()
    for item in items:
        print(item)

    conn.commit()
    conn.close()


def add_record(name, last_name, email, wins=0):
    # add to the date base
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()
    c.execute("INSERT INTO pong VALUES (?,?,?,?)", (name, last_name, email,wins))
    conn.commit()
    conn.close()


def delete_record(id):
    # deletes from the date base using id
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()
    c.execute("DELETE FROM pong WHERE rowid = (?)", id)
    conn.commit()
    conn.close()


def add_win(name, last_name, email):
    # add win to the player
    conn = sqlite3.connect('pong.db')
    c = conn.cursor()
    c.execute("UPDATE pong SET score = score +1 WHERE first_name = (?) AND last_name =(?) AND email =(?)",
              (name, last_name, email))
    conn.commit()
    conn.close()




conn.commit()
conn.close()
