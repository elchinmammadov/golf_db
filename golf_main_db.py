# Fields for customer db: Unique customer ID, name, surname, mobile, house number/name, street name, town, country, postcode, golf proficiency level, member subscription type (i.e. member or non-member),
# Fields for golf courses & time slots: unique ID of golf course, golf course name, golf field, game date, game start time, game end time, booked or not, attendance

import sqlite3
import csv

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

def print_cols_from_full_table(table_name): # Prints column names from table that has some data
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from %s' % table_name)
    r = c.fetchone()
    print r.keys()

def print_cols_from_empty_table(table_name): # Prints column names from table that has no data
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from %s' % table_name)
    r = c.fetchone()
    rows = c.description
    print [x[0] for x in rows]


def list_all_tables(): # Prints names of all tables in current database file
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())

def max_value_in_column_of_table(table_name, column_name): # Shows highest value in the column of a specific table.
    c.execute('SELECT max(%s) FROM %s' % (column_name, table_name))
    max_id = c.fetchone()[0]
    print max_id







# Below are the functions that I need to build:
# find last row with data in a specific table
# insert_data_from_csv_file("bonds")

def insert_data_from_csv_file(table_name): # DOESN"T WORK
    params = (date, trans, symbol, qty, price)
    reader = csv.reader(open('sample_trades.csv', 'r'), delimiter=',')
    for row in reader:
        to_db = [unicode(row[0], "utf8"), unicode(row[1], "utf8"), unicode(row[2], "utf8"), unicode(row[3], "utf8"), unicode(row[4], "utf8")]
        c.execute("INSERT INTO %s (?, ?, ?, ?, ?) VALUES (?, ?, ?, ?, ?)" % table_name, params, to_db) # Insert a row of data
        #c.execute("INSERT INTO PCFC (type, term, definition) VALUES (?, ?, ?);", to_db)
    conn.commit()
# insert_data_from_csv_file("stocks")


# Below are the working statements to manipulate with data. Just remove the hashtag signs to activate them
# create_table("stocks")
# insert_data('stocks', '2006-01-05', 'BUY', 'RDSA', 100, 35.14)
# find_entry("stocks",("RDSA",))
# delete_table("bonds")
# find_all_entries("stocks")
# find_all_entries_and_sort("stocks",("price",))
# print_cols_from_full_table("stocks")
# print_cols_from_empty_table("stocks")
# list_all_tables()
# max_value_in_column_of_table("stocks", "qty")


conn.close() # We can also close the connection if we are done with it. Just be sure any changes have been committed or they will be lost.
