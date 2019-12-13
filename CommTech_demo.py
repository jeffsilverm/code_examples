#! /usr/bin/env python3
# _-_ utf-8 _-_
#

"""
This program times how long it takes to load a large number of long CSV
records in a database
"""

import random
import string

import mysql.connector
import sys
from typing import List

NUM_OF_FIELDS = 4
NUM_OF_RECORDS = 5
LENGTH_OF_FIELD = 7
if len(sys.argv) > 1:
    NUM_OF_RECORDS = int(sys.argv[1])
    if len(sys.argv) > 2:
        NUM_OF_FIELDS = int(sys.argv[2])
        if (len(sys.argv)) > 3:
            LENGTH_OF_FIELD = int(sys.argv[3])
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


# noinspection PyUnresolvedReferences
def execute_command(cursor: mysql.connector.cursor.MySQLCursor, command: str,
                    args=None) -> None:
    """
    This is my version of the cursor.execute() method.  The big advantage
    this has over the "stock" version is that this version is wrapped by a
    try..except block that does a little more intelligent and helpful error
    handler
    """
    try:
        cursor.execute(command, args)
    # There are some errors that the caller can catch an handle, such as
    # dropping a table that's already dropped.
    except mysql.connector.errors.ProgrammingError as m:
        print(str(m), f"\nCommand was {command}\n", file=sys.stderr)
        raise
    # This will catch anything that goes wrong
    except Exception as e:
        print(str(e), f"\nUNRECOVERABLE ERROR! Command was {command}\n",
              file=sys.stderr)


# noinspection PyUnresolvedReferences
def create_table(num_fields: int, lof: int,
                 cursor: mysql.connector.cursor.MySQLCursor) -> List[str]:
    """
    Create the table records_table.
    """
    # If the table already exists, then creating it will fail.  However,
    # dropping it if it doesn't exist will work.  Testing to see if it exists
    # before creating it seems problematic because if the table already exists
    # and it's wrong, then that will create hard to debug problems later on
    drop_table(cursor=cursor)
    # table is a string that looks like:
    # "CREATE TABLE records_table ('f0' CHAR(4), 'f1' CHAR(4), 'f2' CHAR(4),
    # 'f3' CHAR(4) );"
    # noinspection SqlNoDataSourceInspection
    table = f"CREATE TABLE {TABLE_NAME} ("
    # column_names is a list of field names ['f0', 'f1', 'f2', 'f3' ]"
    column_names = []
    #
    for i in range(num_fields):
        field_name = "f" + str(i)
        column_names.append(field_name)
    table += f" CHAR({lof}), ".join(column_names) + f" CHAR({lof}) );"
    execute_command(cursor, table)
    # To see the tables in the database from the command line
    #       SHOW TABLES;
    # To see if the table was created properly from the command line,
    # use the SQL command
    #       DESCRIBE records_table;
    # To get rid of the table (for testing purposes only)
    #       DROP TABLE records_table;
    return column_names


def generate_list(num_fields: int, lof: int) -> List:
    """Generate an input for the database using random data.
    The input is a list of lists of random strings, stored in
    memory (NOT ANY MORE)
    The output is a single record with num_fields fields, each of which is a
    random string of lof characters

    In stackoverflow (https://stackoverflow.com/questions/1477294/generate
    -random-utf-8-string-in-python),
    I found a way to generate a string of all printable UTF-8 characters -
    what fun!
    # noinspection
    print(''.join(tuple(chr(i) for i in range(32, 0x110000) if chr(
    i).isprintable())))
    random.sample(''.join(tuple(chr(i) for i in range(32, 0x110000) if chr(
    i).isprintable())), 1000)
    :param: int: num_fields    How many fields to put in a record
    :param: int:    lof     Length of fields.  Each field has random ASCII
    characters
    :return:    list    list of {num_fields} strings, each {lof} characters
    """
    # db_lines = []
    # for i in range(num_recs):
    line = []
    for i in range(num_fields):
        # noinspection PyUnusedLocal
        random_string: str = \
            ''.join(random.choice(string.printable.rstrip()) for j in range(
                    lof))
        line.append(random_string)
    # lines.append(line)
    return line
    # return db_lines


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def drop_table(cursor: mysql.connector.cursor.MySQLCursor) -> None:  # noqa
    """There may be some additional cleanup in the future"""
    try:
        # noinspection SqlNoDataSourceInspection
        execute_command(cursor, f"DROP TABLE {TABLE_NAME};")
    except mysql.connector.errors.ProgrammingError as q:
        if "Unknown table" not in str(q):
            print(
                    f"Something went horribly wrong when the table "
                    f"{TABLE_NAME} "
                    f"was dropped",
                    file=sys.stderr)
            raise
        else:
            print(f"Dropped a table that was already dropped.  Keep going.",
                  file=sys.stderr)
    return


def populate_table(cursor: mysql.connector.cursor.MySQLCursor,
                   cnx_: mysql.connector,
                   column_names: list, num_of_records: int,
                   num_of_fields: int, length_of_field: int) -> None:
    """
    param: cnx_   Connection to the database
    param:  cursor  Placeholder to where you are in the database
    param:  column_names    A list of the names of the columns
    param:  num_of_records  How many records to put in this database.
    param:  num_of_fields   How many fields in each record
    param:  length_of_field How long are the fields (chars)
    """
    # Storing millions of lines of text in RAM sounds like a
    # recipe for page faulting.
    template = (num_of_fields - 1) * ", %s"
    begin_end_flag = False
    # noinspection SqlNoDataSourceInspection
    execute_command(cursor=cursor, command="SET autocommit = 1; ")
    for line in range(num_of_records):
        # The trick of wrapping a lot of INSERTS with BEGIN and END comes from
        # https://mariadb.com/kb/en/library/how-to-quickly-insert-data-into
        # -mariadb/
        # and has to do with reducing the size of the transaction log
        begin_end_flag = (line % 1000 == 0)
        if begin_end_flag:
            # noinspection SqlNoDataSourceInspection
            execute_command(cursor=cursor, command="BEGIN WORK;")
        db_line: List[str] = generate_list(num_fields=num_of_fields,
                                           lof=length_of_field)
        # noinspection SqlNoDataSourceInspection
        insert_command = f"INSERT INTO {TABLE_NAME}  ( " + \
                         ", ".join(column_names) + ") VALUES ( %s " \
                         + template + ");"
        execute_command(cursor=cursor, command=insert_command, args=db_line)
        if begin_end_flag:
            execute_command(cursor=cursor, command="COMMIT;")
    # If the END command was not done just before exiting the loop, then do
    # it here because otherwise the transacation will be open when it gets
    # committed
    if not begin_end_flag:
        try:
            print("At last COMMIT; before commit", file=sys.stderr)
            execute_command(cursor=cursor, command="COMMIT;")
        except mysql.connector.errors.ProgrammingError as p:
            print("The last COMMIT; raised a "
                  "mysql.connector.errors.ProgrammingError, ignoring.  "
                  f"{str(p)}",
                  file=sys.stderr)
    # Make sure data is committed to the database
    cnx_.commit()


def main(num_of_records: int = NUM_OF_RECORDS, num_of_fields:
         int = NUM_OF_FIELDS,
         length_of_field: int = LENGTH_OF_FIELD) -> None:
    """Create a connection to the database
    """
    cnx: mysql.connector = create_connection()
    cursor: mysql.connector.cursor.MySQLCursor = cnx.cursor()
    column_names: List = create_table(
            num_fields=num_of_fields,
            lof=LENGTH_OF_FIELD, cursor=cursor)
    populate_table(cursor=cursor, cnx_=cnx,
                   column_names=column_names,
                   num_of_records=num_of_records,
                   num_of_fields=num_of_fields,
                   length_of_field=length_of_field)

    # drop_table(cursor=cursor)
    cursor.close()
    cnx.close()


if "__main__" == __name__:
    main(num_of_records=NUM_OF_RECORDS, num_of_fields=NUM_OF_FIELDS,
         length_of_field=LENGTH_OF_FIELD)

# Note: if you get compile time warnings that are actually acceptable,
# then read
# https://intellij-support.jetbrains.com/hc/en-us/community/posts/205816889
# -Disable-individual-PEP8-style-checking-line-length-
