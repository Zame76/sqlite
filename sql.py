# Import sqlite library
import sqlite3

# Path and name of the database
path = "db/test.db"



# Create table Person if it doesn't exists
def createTables():
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()

    # In this file I am going to create SQL clauses in pieces and explain what each piece does
    # so that people not versed in SQL might learn something. Generally SQL languages follow the
    # same format, but there are some small variations in syntax. But when you learn how to 
    # do something in one SQL software, it is usually quite simple to find out how to use syntax
    # of other SQL softwares to do the same.

    # Note! Usually in SQL the language syntax is written in uppercase letters, but since to me
    # it is really, really irritating to have code yelling at me, I don't do this unless I am 
    # getting paid for it. So, I will use uppercase where applicaple when explaing the code, but 
    # in action, all code will be lowercase or sometimes capitalized.

    # CREATE TABLE command creates a table in the Sqlite database.
    clause = "create table "
    # IF NOT EXISTS states that table will be created only if it has not been created already, 
    # this prevents error as duplicate names in tables are not allowed in the same database.
    clause += "if not exists "
    # At this time we are going to create a table named Person, start parenthese at the end of 
    # this line means that we are going to start declaring the columns this table will have.
    clause += "Person ("
    # First column to be used in this table is pid (short for person id).
    # It will be INTEGER like most of id's usually are.
    clause += "pid integer "
    # As it is an id, we will make it as PRIMARY KEY. This will help database in searches as it
    # will be used as index and usually it will connect to other tables in a relational fashion.
    # Primary keys cannot be null and they are unique, so each row will need to have a different
    # id.
    # Comma at the end means that we have now declared this column and are expecting to declare
    # another one.
    clause += "primary key, "
    # The next column we are going to name as firstname and it will contain TEXT. Text is varied
    # amount of letters and sometimes mixed with numbers or special characters in a string.     
    clause += "firstname text "
    # NOT NULL states that this column cannot store NULL values, so there has to be something in
    # it. Note that empty string is not NULL value, so this "" can be stored here. Again comma
    # in the end means that we are going to declare the next column next
    clause += "not null, "
    # Now we declare TEXT based surname column that also cannot have NULL values. Now this is
    # enough columns for this example table, so we end creation by end parenthese.
    clause += "surname text not null)"
    
    # So in the end this SQL clause we are going to execute looks like this:
    # CREATE TABLE IF NOT EXISTS Person (pid INTEGER PRIMARY KEY, firstname TEXT NOT NULL, surname TEXT NOT NULL)

    # Execute the created SQL clause
    sql.execute(clause)
    
    # Create Car table
    # As with Person table we only create Car table if it hasn't already been created.
    clause = "create table if not exists Car ("
    # Now we create column car id cid, which will be INTEGER and PRIMARY KEY for this table. This 
    # time though we use AUTOINCREMENT to increase this value automatically when row is inserted.
    clause += "cid integer primary key autoincrement, "
    # Next column will be owner, which is going to be our connection to the Person table. As
    # it is INTEGER, we will connect this to pid in Person table. It also cannot be NULL, so 
    # every car has to have an owner
    clause += "owner integer not null, "
    # Car usually has a brand so we store that as TEXT in this column, that also cannot be NULL 
    clause += "brand text not null, "
    # Car also has a model, which we can store in this column, but this time it is not forced
    clause += "model text)"
    # You could also implement a foreign key here to force these two tables to really be connected
    # and in some situations that would be really handy, as it would prevent changes in one table from
    # happening if it would affect the data in another. Please, search the internet with sqlite foreing
    # key for more information.
    # Execute the created SQL clause
    sql.execute(clause)
    # In SQL nothing happens in the database until the changes have been committed. So we need to send
    # commit command to make this change happen. In some SQL dedicated editors, there may be an option 
    # for autocommit that maybe defaulted as true, but this is not the case here.
    conn.commit()
    # Close the database connection
    conn.close()



# Insert person to database
def insertPerson(fname, sname):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    
    # Let's take a closer look how to insert data in the Sqlite3 database.
    # We start by command INSERT INTO that is followed by the table name, Person.
    clause = "insert into Person "
    # Now this step is completely *optional*, but personally I like to do this. In the parentheses, we will
    # list names of all the columns of table, in which we are going to insert data. This is to avoid any
    # future problems if/when someone adds more columns to this table. In this way, this code will work
    # unless these columns are removed or renamed. But if you wish, you can comment or remove this line and 
    # it will not affect running this code, unless you go and alter the Person table
    clause += "(pid, firstname, surname) "
    # VALUES keyword states that in the next part of this clause, we are going to give the data to be inserted
    # in the table Person. We need to enclose the data in parentheses.
    clause += "values ("
    # First value to be inserted is pid (person id). As it is unique primary key and an id, we really just need
    # to increase the maximum value of this column by one. In the create table part, we could have achieved this
    # by adding AUTOINCREMENT keyword to this column, but I wanted to show this hack that can also be used, even
    # though it might be a bit slower way to implement this. Anyhow, we can insert the result of another SQL 
    # clause in this column as long as it is enclosed in parentheses. So here we run SELECT command to get MAX
    # pid value FROM Person table and add one to that.
    clause += "(select max(pid)+1 from Person), "
    # Next we prepare this clause to get the two values this function receives when called. Question mark is 
    # quite commonly used to prevent SQL injection attacks that can otherwise happen when malicious user can 
    # write whatever they want in the program. When this clause gets executed, the variables to be inserted in
    # place of question mark, will be stored in the corresponding column. So if it contains malicous SQL code,
    # it will not be executed. End parenthesis here will mark the end of the insert clause.
    clause += "?, ?)"

    # Now this insert clause will be looking like this
    # INSERT INTO Person (pid, firstname, surname) VALUES ((SELECT MAX(pid)+1 FROM Person), ?, ?)

    # Execute the created SQL clause, note that the variables function got, are in the execution command
    # as tuples. So if you need to insert just one item, it needs to be a tuple, ie. (arg,) 
    # The question marks in the clause will be replaced in the order of these variables
    sql.execute(clause,(fname, sname))
    # Commit the changes in database
    conn.commit()
    # Close the database connection
    conn.close()
    # Now that this insert is complete, we can get the last row id used and return it
    value = sql.lastrowid
    return value



# Search the Person table and return results
def selectPerson(search = '%'): 
    # In this function, we will be using a wildcard, so I will explain wildcards here. Usually in SQL, there
    # are two kind of wild cards, first wild card, underscore, replaces one character and second one, percent, 
    # will replace every characted until a character or end of string is reached. When using wildcards, it is 
    # important to use comparison command LIKE instead of =.
    # Let's make few comparisons in sqlite3 terminal: (return values are 0 (False) and 1 (True))

    # Comparisons with = comparison
    # select 'bear' = 'bear';        -> 1 (bear is the same as bear)
    # select 'bear' = 'beer';        -> 0 (bear is not the same as beer)
    # select 'bear' = 'be_r';        -> 0 (bear is not the same as be_r)
    # select 'bear' = '%';           -> 0 (bear is not the same as %)

    # Comparisons with like comparison
    # select 'bear' like 'be_r';     -> 1 (bear is the same as be_r)
    # select 'bear' like '_e_r';     -> 1 (bear is the same as _e_r)
    # select 'bear' like '____';     -> 1 (bear is the same as ____)
    # select 'bear' like '________'; -> 0 (bear is not the same as ________)
    # select 'bear' like 'b%';       -> 1 (bear is the same as b%)
    # select 'bear' like 'b%r';      -> 1 (bear is the same as b%r)
    # select 'bear' like '%r';       -> 1 (bear is the same as %r)
    # select 'bear' like '%e_r';     -> 1 (bear is the same as %e_r)
    # select 'bear' like '%';        -> 1 (bear is the same as %)
    # and so on, please feel free to experiment more

    # Also note that SELECT commands deals with tuples. When something is found it will return a list of tuples.

    # If search parameter is numeric, it means user wants to get info based on person's id
    if search.isnumeric() == True:
        # Convert search parameter to integer
        search = int(search)        
        # Create the SQL clause
        # SELECT command tells the database to fetch data, asterisk get's all columns of the table.
        # SELECT pid, firstname, surname would be the same as asterisk in this case
        clause = "select * "
        # FROM keyword will point as to the correct table in the database, in this case Person
        clause += "from Person "
        # Now, at this point, this clause is fully functional and would return everything stored in the
        # Person table. However, as we are searching through the with search parameter, WHERE clause is 
        # needed to narrow down the results. So in this point, we will require the search parameter to
        # strictly match our search parameter as no wildcard is interpreted as numeric and thus would not 
        # make through numeric check above.
        clause += "where pid = ?"
        # Set numeric to true
        numeric = True
    # Search parameter is not numeric, so look into name columns
    else:
        # Replace spaces in the search paramet with wild card and add one wild card to the end
        search = search.replace(" ", "%") + "%"
        # Create the SQL clause 
        # As in the prior case, this SELECT is set to get all the columns FROM Person table. At this point,
        # this is fully working SELECT clause, which when run would return every column and every row this
        # table has as a tuple. But we 
        clause = "select * from Person "
        # Now in this WHERE clause, there are many things happening. Let's start with LOWER() function.
        # It transforms everything inside to lower case. Inside the first lower function there is a 
        # concatenation operator ||. So, in this case the logic concatenates firstname and surname and
        # then turns it in lowercase. Ie. John Doe would become JohnDoe and then johndoe.
        clause += "where lower(firstname || surname)" 
        # Now we use like operator to check the if the search parameter added with the wildcards above,
        # matches the otherpart of this where clause.
        clause += "like lower(?) "
        # Here we check for the possibility that user has started to insert surname first to the search 
        # parameter, otherwise it works the same as above. Ie. check if doejohn matches to search parameter.
        clause += "or lower(surname || firstname) like lower(?)"
        # Set numeric to False
        numeric = False
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # Execute the proper sql clause based on the value of numeric variable        
    if numeric == True:
        # As we have a numeric search parameter, our SQL clause now looks like this:
        # SELECT * FROM Person WHERE pid = ?
        # So we need to send our search as a tuple of single value to successfully execute this select
        value = sql.execute(clause, (search,)).fetchall()
        # This will return a tuple of single item as a list or an empty list if nothing matches
    else:
        # We do not have a numeric search parameter, so the SQL clause looks like this:
        # SELECT * FROM Person WHERE LOWER(firstname || surname) LIKE LOWER(?) or LOWER(surname || firstname) LIKE lower(?) 
        # As there are two positions that needs to get the search parameter, we create a tuple of
        # double search parameters.
        value = sql.execute(clause, (search, search)).fetchall()
        # This will return a tuple with single or more values as a list or an empty list if nothing matches.
    # Close database connection
    conn.close()
    # Return the result of executed select as list of tuples
    return value



# Check if given pid is in Person table
def checkPid(pid):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()    
    # This by itself is fully working SELECT clause, which would return the COUNT of rows where pid is not 
    # NULL. In this case, it would count all the rows in the table as pid cannot be NULL. This would return 
    # an integer wrapped inside a tuple.
    clause = "select count(pid) from Person "
    # Let's narrow down the results with WHERE condition. This function receives person's id as parameter,
    # so we can run a count of given pid in the table. Now the count will be 1, if the given pid is in the
    # table. If given pid is not in the table, count will be 0. This effectively acts as verification of
    # pid's existence 
    clause += "where pid = ?"
    # Since this SELECT clause results into exactly one integer, we can use fetchone()-function instead of 
    # fetchall(). Also as a reminder ? replacer needs to be a tuple.
    value = sql.execute(clause, (pid,)).fetchone()
    # Close database connection
    conn.close()
    # Return the result of executed select as list of tuples    
    return value



# Get the number of cars given person owns
def countCars(pid):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()    
    # This by itself is fully working SELECT clause, which would return the COUNT of rows where cid is not 
    # NULL. In this case, it would count all the rows in the table as cid cannot be NULL. This would return 
    # an integer wrapped inside a tuple.
    clause = "select count(cid) from Car "
    # Let's narrow down the results with WHERE condition. This function receives person's id as parameter
    # and as owner is person id we can just limit results to those rows where pid = owner
    clause += "where owner = ?"
    # Since this SELECT clause results into exactly one integer, we can use fetchone()-function instead of 
    # fetchall(). Also as a reminder ? replacer needs to be a tuple.
    value = sql.execute(clause, (pid,)).fetchone()
    # Close database connection
    conn.close()
    # Return the result of executed select as list of tuples    
    return value



# Update name of the person
def changeName(pid, name, switch):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # Now here we have to update the person's name. To do that we need information on whom to update, which 
    # name is going to be updated and what the new name is. All of this information comes in the arguments 
    # of this function. This also is a nice example, why building sql clause in blocks is quite handy feature.
    # We start with UPDATE command which is followed by the name of the table we want to update. Next comes 
    # the keyword SET, which tells that we are about to tell which columns are going to be updated.
    clause = "update Person set "
    # We got switch variable as argument, and that is telling us which name we are about to update. If it is
    # "fname", we update first name otherwise the surname gets updated
    if switch == "fname":
        # Updating happens by telling the column name to be updated followed by equal sign and the question mark,
        # which will later be replaced with data 
        clause += "firstname = ? "
    else:
        clause += "surname = ? "
    # Now at this point, we actually have a working UPDATE sql clause. The problem with this, is that it would
    # update every single entry in the column with the value we are going to give. I have once done this mistake
    # and learned a very valuable lesson to be focused when working with databases. So, make sure you have WHERE
    # condition to limit the updating process, unless you really want to replace every value of this column with
    # this data. In this case, we limit the changes by targeting the given person id.
    clause += "where pid = ?"
    # Now, we have fully functional UPDATE clause, which will look like this. Assuming it is first name we are 
    # updating
    # UPDATE Person SET firstname = ? WHERE pid = ?
    # Of course, we could have gotten both names as arguments in this function and done the updating together.
    # In that case we could replace if-else structure with clause block "firstname = ?, surname = ?"
    sql.execute(clause, (name, pid))
    # Commit the changes in database
    conn.commit()
    # Close database connection
    conn.close()




# Insert new car for the person
def insertCar(owner, brand, model = ""):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # I made deeper cut in INSERT INTO command in insertPerson() function, so check that for more information.
    clause = "insert into Car "
    # Depending on if model has been provided or not, we need to execute this update differently
    if model == "": 
        # In this case, we omit the model as it is empty.
        clause += "(owner, brand) values (?, ?)"
        sql.execute(clause,(owner, brand))
    else:
        # In this case, model has been provided so we change the ending of this update clause and execute it
        # with all three values
        clause += "(owner, brand, model) values (?, ?, ?)"
        sql.execute(clause,(owner, brand, model))
    # Commit the changes in database
    conn.commit()
    # Close database connection
    conn.close()



# Get data of person's cars
def showCars(pid):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # This is a simple SELECT clause that is better explained in the selectPerson() and checkPid() functions
    clause = "select cid, brand, model from Car where owner = ?"
    # Run the sql clause and get the results 
    value = sql.execute(clause, (pid,)).fetchall()
    # Commit the changes in database
    conn.commit()
    # Close database connection
    conn.close()
    # Return the results
    return value



# Delete person from database
def deletePerson(pid):
    # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # Now we take a look at the most dangerous command sql has. DELETE erases data from database and if 
    # written incorrectly, it can cause enourmous damage. Important thing to know about DELETE is that
    # it deals at row level. When you DELETE something, the whole row gets erased. If you just want to 
    # delete one column, use UPDATE command to empty it or ALTER TABLE to remove the whole column. If 
    # you delete column with ALTER TABLE, you will have to look through the code to find and correct any
    # references to it, or the program might crash.
    # At this stage, this clause is actually working sql command, and it ***will*** delete everything in 
    # your table. So if this is not something you want to do, ***double check*** that you have a WHERE 
    # condition attached with this command.So if left like this, this clause will delete everything from 
    # the table Car. 
    clause = "delete from Car "
    # So, we add WHERE clause here, which means that we are only deleting the rows where the owner is 
    # the person who we are deleting. We can run this command even if this Person does not have any cars,
    # in that case nothing will be deleted. This is just a clean up to Car table, to remove any traces of
    # persons, that can't be found in Person table anymore.
    clause += "where owner = ?"
    # Now, delete rows based on owner in the Car table. The actual delete clause looks like this:
    # DELETE FROM Car WHERE owner = ?
    sql.execute(clause,(pid,))
    # We have cleansed the Car table of this person, so now it is time to delete this person from Person
    # table.
    clause = "delete from Person where pid = ?"
    sql.execute(clause,(pid,))
    # Commit the changes in database
    conn.commit()
    # Close database connection
    conn.close()



# Show all information about cars
def showCars():
    # In this function, we will take a closer look on how to fetch data from multiple tables connected
    # to each other. 
     # Connect to database
    conn = sqlite3.connect(path)
    # Create cursor to run sql commands
    sql = conn.cursor()
    # We start with normal SELECT command
    clause = "select "
    # Now the command expects us to list columns we want to fetch and here we start using aliases for
    # the tables. We want to get firstname and surname from Person table, and brand and model from Car
    # table. We will use their aliases p and c here, which we will create later  
    clause += "p.firstname, p.surname, c.brand, c.model "
    # Now we state that we want to use Car table and give it alias of c
    clause += "from Car as c "
    # Here we will add the second table in the select and give it alias of p. In sql, there are usually
    # four different joins: left, right, inner and outer join. In this case we use the LEFT JOIN, which 
    # will determine the Car table (which is left table in this command) to be the primary table. 
    # This means that we will get results from Car table and add only corresponding values from Person 
    # table. So, there might be rows in the Person table that will be omitted, because they do not have
    # a car. 
    #
    # If we would use RIGHT JOIN here, it would make Person table (as it is right in this command) the 
    # primary one, and the results would have every row in the Person table. If that person wouldn't 
    # have a car, there will be null values for the fields from Car table where person wouldn't have 
    # a car. If there would be rows in Car table where owner column wouldn't have corresponding id in 
    # Person table, these rows would be omitted.
    #
    # In case of INNER JOIN, both tables are primary tables. If any of the requests fields in either of
    # the tables are NULL, the whole result will be omitted. So, persons without cars and cars without 
    # owners would not show.
    #
    # FULL OUTER JOIN is the most generous option here, as it will result in all of the rows in both 
    # Person and Car tables. If one table is missing corresponding entry, it will simply be replaced 
    # with NULL value. So, basically this join would return every row in both tables and combine them 
    # where connection is found. 
    #
    # If you are using different sql software, please search for syntax of these joins in that 
    # enviroment as they may vary.
    clause += "left join Person as p "
    # In our joining of two tables, we have to determine the one connecting value between tables. In 
    # this case we will use pid from Person and owner from Car as they are both the same value.
    clause += "on c.owner = p.pid"
    # At this point, I would like to point out that in this example we are connecting only two tables
    # together. But there is no limit how many tables we connect in one command as long as they can
    # be tied together. So table A can be joined to table B that is connected to table C or table C
    # is connected to table A. 
    # Also, you can update values in a table with another tables values, which can be handy at times:
    # UPDATE a
    #   SET a.column = b.column
    # FROM table1 AS a 
    #   JOIN table2 AS b 
    #       ON a.keycolumn = b.keycolumn
    value = sql.execute(clause).fetchall()
    # Commit the changes in database
    conn.commit()
    # Close database connection
    conn.close()
    return value