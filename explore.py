#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file reads in and executes the queries from a sql file created solely for
exploring a database. In our case this file will read in and execute the
queries from a file called explore.sql on the database london_osm.db.
"""

import sqlite3
import pprint


def executeQueriesFromFile(filename, dbname):
    open_file = open(filename, 'r')
    sql_file = open_file.read()

    sql_commands = sql_file.split(';')
    db_conn = sqlite3.connect(dbname)
    cursor = db_conn.cursor()

    for command in sql_commands:
        try:
            cursor.execute(command)
            db_conn.commit()
            pprint.pprint(cursor.fetchall())
        except Exception, msg:
            print "Command skipped: ", msg
    db_conn.close()
    open_file.close()


if __name__ == '__main__':
    executeQueriesFromFile('explore.sql', 'london_osm.db')
