# Fields for customer db: Unique customer ID, name, surname, mobile, house number/name, street name, town, country, postcode, golf proficiency level, member subscription type (i.e. member or non-member),
# Fields for golf courses & time slots: unique ID of golf course, golf course name, golf field, game date, game start time, game end time, booked or not, attendance

import sqlite3
import csv

conn = sqlite3.connect('example.db')

c = conn.cursor()


def create_table(table_name): # creates data table with columns. You will get an error if you run script twice because the table is already created
    c.execute('''CREATE TABLE %s
                (date text NOT NULL,
                trans text NOT NULL,
                symbol char(5) NOT NULL,
                qty int NOT NULL,
                price real NOT NULL)''' % table_name)
    conn.commit() # Save (commit) the changes

def create_table_autoincrement(table_name): # creates data table with columns same as above but with additional Autoincrement feature based on extra row called 'id'. You will get an error if you run script twice because the table is already created
    c.execute('''CREATE TABLE %s
                (id integer PRIMARY KEY AUTOINCREMENT,
                date text NOT NULL,
                trans text NOT NULL,
                symbol char(5) NOT NULL,
                qty int NOT NULL,
                price real NOT NULL)''' % table_name)
    conn.commit() # Save (commit) the changes

def rename_table(table_name, new_table_name): # renames existing table
    c.execute('ALTER TABLE %s RENAME TO %s' % (table_name, new_table_name))

def delete_table(table_name): # deletes existing data table
    c.execute("DROP TABLE IF EXISTS %s" % table_name)

def insert_data(table_name, date, trans, symbol, qty, price): # inserts row of data into existing table
    params = (date, trans, symbol, qty, price)
    c.execute("INSERT INTO %s VALUES (?, ?, ?, ?, ?)" % table_name, params) # Insert a row of data
    conn.commit()

def delete_all_records(table_name): # deletes all rows of data from existing table
    c.execute("DELETE FROM %s" % table_name)

def delete_specific_records(table_name, column_name, record):
    c.execute("DELETE FROM %s WHERE %s = '%s'" % (table_name, column_name, record))
    conn.commit()

def add_table_column(table_name, column_name, data_type): # adds an extra column to existing data table
    c.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, data_type))

def update_specific_records(table_name, column_name, old_record, new_record): # updates all records in a specific table to a new value
    c.execute("UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (table_name, column_name, new_record, column_name, old_record))

def find_entry(table_name, entry):
    c.execute('SELECT * FROM %s WHERE symbol=?' % table_name, entry)
    print c.fetchall() # use c.fetchone() to fetch one en

def find_all_entries(table_name):
    for row in c.execute('SELECT * FROM %s' % table_name):
        print row

def find_all_entries_and_sort(table_name, entry):
    for row in c.execute('SELECT * FROM %s ORDER BY ?' % table_name, entry):
        print row

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

def find_last_created_row(table_name): # Shows highest value in the column of a specific table. Works even if you don't have have 'id' row and use AUTOINCREMENT for your table
    c.execute('INSERT INTO stocks (date, trans, symbol, qty, price) VALUES (?,?,?,?,?)', ('2006-01-05', 'SELL', 'RDSA', 100, 30.14)) # for some reason, lastrowid only works if you add an extra entry. I specifically omitted conn.commit() expression at the end of this function in order not to save changes.
    print(c.lastrowid)

def find_last_created_row_autoincrement(table_name): # Shows highest value in the column of a specific table. Won't work unless you have have 'id' row and use AUTOINCREMENT for your table
    c.execute('SELECT max(id) FROM %s' % table_name)
    max_id = c.fetchone()[0]
    print max_id

def open_db(db_name): # function to open a table
    conn = sqlite3.connect(db_name)
    # Let rows returned be of dict/tuple type
    conn.row_factory = sqlite3.Row
    print "Openned database %s as %r" % (db_name, conn)
    return conn
def copy_table_function(src_table_name, dest_table_name, src, dest): # function to copy a data from one table in one database into another table in another database. Don't use this function on its own. It needs to be used in conjunction with open_table function. Use copy_table function instead in order to copy the table.
    print "Copying %s %s => %s" % (src_table_name, src, dest)
    sc = src.execute('SELECT * FROM %s' % src_table_name)
    ins = None
    dc = dest.cursor()
    for row in sc.fetchall():
        if not ins:
            cols = tuple([k for k in row.keys() if k != 'id'])
            ins = 'INSERT OR REPLACE INTO %s %s VALUES (%s)' % (dest_table_name, cols, ','.join(['?'] * len(cols)))
            print 'INSERT stmt = ' + ins
        c = [row[c] for c in cols]
        dc.execute(ins, c)
    dest.commit()
def copy_table(src_table_name, dest_table_name, src_conn, dest_conn): # to copy table from noe database to another
    src_conn  = open_db(src_conn)
    dest_conn = open_db(dest_conn)
    copy_table_function(src_table_name, dest_table_name, src_conn, dest_conn)



# Below are the functions that I need to build:
# delete column by creating new table with that column and then migrating data from old table. Then delete old table and change name of new table to name of old table.
# reorder columns in the table by creating new table with the right column orders and then migrating data from old table. Then delete old table and change name of new table to name of old table.
# copy data to from selected columns from one table to another. Use copy_table() function as a template
# fix insert_data_from_csv_file("bonds") function
# make find_last_created_row() function more flexible. ATM I need to enter specific data into it. Instead, need to find first data row, then copy that data row values automatically, without manual entries.

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
# create_table("bonds")
# rename_table("options", "bonds")
# insert_data('bonds', '2006-01-05', 'SELL', 'RDSA', 100, 30.14)
# insert_selected_data('bonds', '2006-01-05', 'SELL', 'RDSA', 100, 30.14)
# find_entry("stocks",("RDSA",))
# add_table_column('bonds','temp','text')
# delete_all_records('bonds')
# delete_table("bonds")
# delete_specific_records("bonds", "symbol", "RHAT")
# update_specific_records('bonds', 'symbol', 'RDSA', 'GOOG')
# copy_table('stocks', 'bonds', 'example.db', 'example.db')
# find_all_entries('options')
# create_table_autoincrement('options')
# find_last_created_row_autoincrement('bonds')
find_last_created_row('stocks')
# find_all_entries_and_sort("bonds",("price",))
# print_cols_from_full_table("stocks")
# print_cols_from_empty_table("bonds")
# list_all_tables()
# max_value_in_column_of_table("stocks", "qty")


conn.close() # We can also close the connection if we are done with it. Just be sure any changes have been committed or they will be lost.
