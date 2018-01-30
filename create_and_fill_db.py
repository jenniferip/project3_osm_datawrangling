#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file creates and fills the necessary database tables.

The function createTablesFromFile() takes in the following variables:
  - filename, this pertains to the sql file you wish to read in and execute its
    queries
  - dbname, which is the name of the database being altered or created, if no
    such database exists then the function will create a new one
With these variables, createTablesFromFile reads and executes the queries from
the sql file, in our case populate_db.sql which drops and creates tables, into
the database we specied, in our case london_osm.db.

The next function fillTables takes in the variables:
  - csv_file, which is the csv file you wish to read and transfer into the
    database
  - dbname, the name of the database you are filling
  - table, the name of the table you wish to fill with the information from
    the csv file
  - columns, is a string containing the name of the columns in the order they
    appear in the tuple
  - tup_shape, a string describing the number of columns in each row that will
    be inserted; it has the form (?, ?, ?) if say the table to be filled is
    made of three columns
fillTables reads in the csv file using DictReader from the csv module,
populates a list of tuples with the information to be inserted into the table,
and finally executes the insert query.
"""

import sqlite3
import csv
from pprint import pprint


def createTablesFromFile(filename, dbname):
    open_file = open(filename, 'r')
    sql_file = open_file.read()

    sql_commands = sql_file.split(';')
    db_conn = sqlite3.connect(dbname)
    cursor = db_conn.cursor()

    for command in sql_commands:
        try:
            cursor.execute(command)
            db_conn.commit()
        except Exception, msg:
            print "Command skipped: ", msg
    db_conn.close()
    open_file.close()


def fillTables(csv_file, dbname, table, columns, tup_shape):
    with open(csv_file, 'rb') as f:
        csv_dict = csv.DictReader(f)
        to_insert = set()
        for item in csv_dict:
            item_values = [(value.decode("utf-8"), ) for (key, value) in
                           item.items()]
            item_tuple = (None, )
            for i in range(len(item_values)):
                curr_item = item_values[i]
                item_tuple += curr_item
            to_insert.add(item_tuple[1:])

        db_conn = sqlite3.connect(dbname)
        cursor = db_conn.cursor()
        insert_string = "INSERT INTO {} {} VALUES {};".format(table, columns,
                                                              tup_shape)
        cursor.executemany(insert_string, to_insert)
        db_conn.commit()
        db_conn.close()


if __name__ == '__main__':
    sqlite_db_file = 'london_osm.db'

    createTablesFromFile('populate_db.sql', sqlite_db_file)
    fillTables('nodes.csv', sqlite_db_file, 'nodes',
               '(changeset, uid, timestamp, lon, version, user, lat, id)',
               '(?, ?, ?, ?, ?, ?, ?, ?)')
    fillTables('nodes_tags.csv', sqlite_db_file, 'nodes_tags',
               '(value, type, id, key)', '(?, ?, ?, ?)')
    fillTables('ways.csv', sqlite_db_file, 'ways',
               '(changeset, uid, timestamp, version, user, id)',
               '(?, ?, ?, ?, ?, ?)')
    fillTables('ways_tags.csv', sqlite_db_file, 'ways_tags',
               '(value, type, id, key)', '(?, ?, ?, ?)')
    fillTables('ways_nodes.csv', sqlite_db_file, 'ways_nodes',
               '(position, node_id, id)', '(?, ?, ?)')
