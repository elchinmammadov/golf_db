# this script uses PostgreSQL database

import psycopg2
import psycopg2.extras as e # used for things like converting PostgreSQL data from lists into dictionary data types
import sys

def create_table_autoincrement(table_name):
    c.execute("CREATE TABLE %s (id serial PRIMARY KEY, num integer, data varchar);" % table_name)
    print(table_name + ' table has been created')

def delete_table(table_name):
    c.execute("DROP TABLE IF EXISTS %s" % table_name)
    print(table_name + ' table has been deleted')

def find_all_entries_print_as_tuples (table_name):
    c.execute('SELECT * from %s' % table_name)
    rows = c.fetchall()
    print(rows)

def find_all_entries(table_name):
    c.execute('SELECT * from %s' % table_name)
    rows = c.fetchall()
    for row in rows:
        print(row)

def find_data_in_specific_row(table_name):
    c.execute('SELECT * from %s' % table_name)
    rows = c.fetchall()
    print(rows[0])

def find_data_in_specific_row_and_column(table_name, row_num, column_num):
    c.execute('SELECT * from %s' % table_name)
    rows = c.fetchall()
    print(rows[row_num][column_num])

def find_data_via_dictionary_type_db(table_name,col_name): # to convert PostgreSQL data from lists (default) into dictionary type in python
    import psycopg2.extras as e
    c = conn.cursor(cursor_factory=e.DictCursor)
    c.execute('SELECT * from %s' % table_name)
    rows = c.fetchall()
    for row in rows:
        print (row[col_name])

def insert_data():
    c.execute("INSERT INTO new_table (id, name, surname, age) VALUES (%s, %s, %s, %s)",29, "John", "Smith", 32))
#def insert_data(table_name, id, name, surname, age): # inserts row of data into existing table
#    c.execute('INSERT INTO %s (id, name, surname, age) VALUES (%s, %s, %s, %s)' % (table_name, id, name, surname, age)) # Insert a row of data
#    c.execute('INSERT INTO new_table (id, name, surname, age) VALUES (%s, %s, %s, %s)', (30, 'Paul', 'Rogers', 30)

# script below shows PostgreSQL data as lists. To convert PostgreSQL data from lists (default) into dictionary type in python use function find_data_via_dictionary_type_db
try:
    conn = psycopg2.connect("dbname=sample_db user=postgres host=localhost password=bournemouth") # Connect to an existing database
    c = conn.cursor() # Open a cursor to perform database operations
    find_all_entries('new_table')
    insert_data()
    # insert_data('new_table', 29, 'Jake', 'Jones', 12)
    conn.commit() # Make the changes to the database persistent
    c.close() # Close communication with the database
    conn.close() # Close communication with the database
except Exception as exptn:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(exptn)

