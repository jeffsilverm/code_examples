#! /usr/bin/env python3
# _-_ utf-8 _-_
#

"""
This program times how long it takes to load a large number of long CSV
records in a database"""

import random
import string

import mysql.connector
import sys
from typing import List

NUM_OF_RECORDS = 4
NUM_OF_FIELDS = 4
LENGTH_OF_FIELD = 4
TABLE_NAME = "records_table"


def create_connection() -> mysql.connector:
    """Create a connection to the database"""

    """
    If the database does not exist, then create it and give yourself full 
    access to it.  For "real" purposes, you would not want full access, 
    but for the purposes of this demo where security is not an issue, 
    don't sweat the small stuff.
    root@jeffs-desktop:~# mysql -u root -p
Enter password: 
MariaDB [(none)]> show databases;
MariaDB [(none)]> use records;
MariaDB [records]> grant all on record.* to 'jeffs'@'localhost';
Query OK, 0 rows affected (0.001 sec)
MariaDB [records]> grant select on record.* to 'jeffs'@'localhost';
MariaDB [records]> grant insert on record.* to 'jeffs'@'localhost';
MariaDB [records]> grant update on record.* to 'jeffs'@'localhost';
MariaDB [records]> grant delete on record.* to 'jeffs'@'localhost';
MariaDB [records]> 

    
    """

    with open("credentials.txt", "r") as f:
        line = f.readline()
    # Get rid of any trailing line separation characters.
    # This will work with Mac OS X, MS-DOS, and UNIX
    line = line.rstrip('\r\n')
    username, password = line.split(",")

    # To see *anything* in the records database using SQL commands
    #    use records;
    cnx_: mysql.connector.connection.MySQLConnection = \
        mysql.connector.connect(user=username,
                                password=password,
                                host='127.0.0.1',
                                database='records')
    return cnx_


def execute_command(cursor: mysql.connector.cursor.MySQLCursor, command) -> \
        None:
    """
    This is my version of the cursor.execute() method.  The big advantage
    this has over the "stock" version is that this version is wrapped by a
    try..except block that does a little more intelligent and helpful error
    handler
    """
    try:
        cursor.execute(command)
    except mysql.connector.errors.ProgrammingError as m:
        print(str(m), f"\nCommand was {command}\n", file=sys.stderr)
        raise


def create_table(num_fields: int, lof: int, cnx_: mysql.connector) -> None:
    """
    Create the table records_table.
    """
    table = f"CREATE TABLE {TABLE_NAME} ("
    for i in range(num_fields):
        field_name = "f" + str(i) + f" CHAR({str(lof)})"
        # Leave off the trailing ,
        table += field_name + (", " if i < (num_fields - 1) else "")
    table += ");"
    execute_command(cnx_.cursor(), table)
    # To see the tables in the database from the command line
    #       SHOW TABLES;
    # To see if the table was created properly from the command line,
    # use the SQL command
    #       DESCRIBE records_table;
    # To get rid of the table (for testing purposes only)
    #       DROP TABLE records_table;
    return None


def generate_list(num_fields, lof) -> List:
    """Generate an input for the database using random data.
    The input is a list of lists of random strings, stored in
    memory (NOT ANY MORE)
    The output is a single record with num_fields fields, each of which is a
    random string of lof characters
    """
    # db_lines = []
    # for i in range(num_recs):
    line = []
    for f in range(num_fields):
        random_string: str = ''.join(random.choice(string.printable)
                                     for i in range(lof))
        line.append(random_string)
    # lines.append(line)
    return line
    # return db_lines


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def drop_table(cursor: mysql.connector.cursor.MySQLCursor) -> None:
    """There may be some additional cleanup in the future"""
    execute_command(cursor, f"DROP TABLE {TABLE_NAME};")


def main(num_of_records: int = NUM_OF_RECORDS, num_of_fields:
          int = NUM_OF_FIELDS,
          length_of_field: int = LENGTH_OF_FIELD) -> None:
    """Create a connection to the database
    """
    cnx: mysql.connector = create_connection()
    cursor: mysql.connector.cursor.MySQLCursor = cnx.cursor()
    create_table(num_fields=num_of_fields, lof=LENGTH_OF_FIELD, cnx_=cnx)

    # Storing millions of lines of text in RAM sounds like a recipe for page
    # faulting.
    for line in range(num_of_records):
        db_line: List[str] = generate_list(num_fields=num_of_fields,
                                           lof=length_of_field)
        raise NotImplementedError("THIS IS WRONG - GO BACK AND RTFM ABOUT HOW TO DO AN INSERT "
              "FROM PYTHON")
        values = "VALUES ("
        insert_command = "INSERT INTO employees ("
        for i in range(num_of_fields - 1):
            insert_command += "%, "
            values += db_line[i] + ", "
        insert_command += f"% ) {values} {db_line[num_of_fields-1]} );"
        execute_command(cursor=cursor, command=insert_command)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    drop_table(cnx)
    cnx.close()


if "__main__" == __name__:
    main(num_of_records=NUM_OF_RECORDS, num_of_fields=NUM_OF_FIELDS,
         length_of_field=LENGTH_OF_FIELD)
