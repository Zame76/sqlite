This is an experiment of Sqlite3

This utilizes pipenv virtual environment, so if you want to utilize this, run command "pipenv install" in this programs directory.
Otherwise, make sure you have Colorama package installed or remove all the references to it in main.py.

Also, the default directory and name of the database this program uses is 'db/test.py', so either make sure that there is 
subfolder called db in the working directory or change the default path in sql.py. If this default folder is not accessible, this
program will crash.

The main reason of this program is to see how sqlite3 works. This program has two working python files: main.py and sql.python
main.py has all the functionality, sql.py contains functions to run sql commands.

If not changed, it will create database called test.db in the default position.
Inside this database it will create tables Person and Car, if these do not exist already

run main.py to execute the program.

Both files have been commented to the best of my ability, sql.py has exceptionally long comments regarding to sql commands.
All sql commands in sql.py have been chopped in parts and explained to the best of my ability and therefore it is mostly
comments explaining what is happening in each function. 

Sqlite3
run sqlite shell with command sqlite3 <database>.db
Few useful commands:
.quit
    - exit shell
.help
    - shows all the control commands
.show
    - shows current values of various settings
.headers
    - options on or off
    - if on shows column names
.mode
    - formats the output of sql select commands
    - options are column, csv, html, insert, line, list, tabs, tcl
    - list is default, I like column
.tables
    - shows table names in the database
-schema <table>
    - shows the table creation command
- About sql commands
    - every sql command needs to end with ;
    - example of select statement
        * SELECT * FROM table WHERE column = value;
    - example of insert statement
        * INSERT INTO table (column1, column2) VALUES (value1, value2);
    - example of update statement
        * UPDATE table SET column1 = value1, column2 = value2 WHERE condition = expression;
    - example of delete statement
        * DELETE FROM table WHERE condition = expression;

When creating a sql clause, you should create and test it in the sqlite shell before appending it to your code.
This way you will see if it is going to work as intended or if you need to tweak it a little bit more.
   
Created with 
    Python 3.12.0
    Sqlite3 3.42.0
    Colorama 0.4.6