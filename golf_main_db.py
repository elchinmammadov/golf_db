# Fields for customer db: Unique customer ID, name, surname, mobile, house number/name, street name, town, country, postcode, golf proficiency level, member subscription type (i.e. member or non-member),
# Fields for golf courses & time slots: unique ID of golf course, golf course name, golf field, game date, game start time, game end time, booked or not, attendance

import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table. You will get an error if you run script twice because the table is already created
def create_table(table_name):
    c.execute('''CREATE TABLE %s
                (date text,
                trans text,
                symbol text,
                qty real,
                price real)''' % table_name)
    conn.commit() # Save (commit) the changes

def insert_data(table_name, date, trans, symbol, qty, price):
    params = (date, trans, symbol, qty, price)
    c.execute("INSERT INTO %s VALUES (?, ?, ?, ?, ?)" % table_name, params) # Insert a row of data
    conn.commit()

def find_entry(table_name, entry):
    c.execute('SELECT * FROM %s WHERE symbol=?' % table_name, entry)
    print c.fetchall() # use c.fetchone() to fetch one en

def find_all_entries(table_name):
    for row in c.execute('SELECT * FROM %s' % table_name):
        print row

def find_all_entries_and_sort(table_name, entry):
    for row in c.execute('SELECT * FROM %s ORDER BY ?' % table_name, entry):
        print row

def delete_table(table_name):
    c.execute("DROP TABLE IF EXISTS %s" % table_name)



# Below are the working statements to manipulate with data. Just remove the hashtag signs to activate them
# create_table("options")
# insert_data('stocks', '2006-01-05', 'BUY', 'RDSA', 100, 35.14)
# find_entry("stocks",("RDSA",))
# delete_table("stocks")
# find_all_entries("stocks")
# find_all_entries_and_sort("stocks",("price",))

conn.close() # We can also close the connection if we are done with it. Just be sure any changes have been committed or they will be lost.
