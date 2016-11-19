# Gotta have name, surname, mobile, house number/name, street name, town, country, postcode, golf course, golf set, game date, game start time, game end time, booking time, attendance, golf proficiency level, member subscription type.

import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table. You will get an error if you run script twice because the table is already created
def create_table(table_name):
    c.execute('''CREATE TABLE %s
                (date text, trans text, symbol text, qty real, price real)''' % table_name)
    conn.commit() # Save (commit) the changes

def insert_data(table_name, date, trans, symbol, qty, price):
    params = (date, trans, symbol, qty, price)
    c.execute("INSERT INTO %s VALUES (?, ?, ?, ?, ?)" % table_name, params) # Insert a row of data
    conn.commit()

def find_entry(entry):
    c.execute('SELECT * FROM stocks WHERE symbol=?', entry)
    print c.fetchall() # use c.fetchone() to fetch one en

# Below are the working statements to manipulate with data. Just remove the hashtag signs to activate them
# create_table("stocks")
# insert_data('stocks', '2006-01-05', 'BUY', 'RDSA', 100, 35.14)
# find_entry(("RDSA",))

conn.close() # We can also close the connection if we are done with it. Just be sure any changes have been committed or they will be lost.
