# IMPORTANT!!!!!!!!
# This program uses a database file and the default location and name is 
# <current dir>/db/test.db
# If db folder is not found or there are insufficient rights, program will crash
# Change default location in sql.py file by changing path-variable

# Import libraries and functions
import sql
from colorama import just_fix_windows_console, Fore

# Fixes colorama for windows
just_fix_windows_console()

# Creates tables in the Database if those don't exist already
sql.createTables()

# Single person found
def person(person):
    print("\nShowing person's data")    
    print(f"\tPerson ID:\t{person[0]}")
    print(f"\tSurname:\t{person[2]}")   
    print(f"\tFirst name:\t{person[1]}")       
    value = sql.countCars(person[0])
    print(f"\tNumber of cars:\t{value[0]}") 
    print("\nSelect option:")   
    print("\t(1) Return to main menu")
    print("\t(2) Change the first name")
    print("\t(3) Change the last name")
    print("\t(4) Add a car")
    if value[0] > 0:
        print("\t(5) Show owned cars")
    print(Fore.RED + "\t(9) Delete Person" + Fore.GREEN)
    print("\t(0) Quit")
    selection = 0
    while selection == 0:
        selection = input("> ")
        if selection.isnumeric() == True:
            selection = int(selection)
            
            # User wants to quit
            if selection == 0:
                print("\nThank you for using Person Database" + Fore.RESET)
                exit()
            
            # User want to return to main menu
            elif selection == 1:
                # No need to do anything here right now
                pass

            # User wants to change the first name
            elif selection == 2:
                # Ask for new name until one has been given
                name = ""
                while name == "":
                    name = input("Please give new first name: ")
                # Change the first name
                sql.changeName(person[0], name, "fname")
                # Inform user
                print("First name changed")
                # Now this will return user back to main menu, this is not the best practise, but 
                # as the reason for this program is to focus on sqlite3, we just have to endure this. 
                
            # User wants to change the last name
            elif selection == 3:
                # Ask for new name until one has been given
                name = ""
                while name == "":
                    name = input("Please give new surname: ")
                # Change the first name
                sql.changeName(person[0], name, "sname")
                # Inform user
                print("Surname changed")
                # Now this will return user back to main menu, this is not the best practise, but 
                # as the reason for this program is to focus on sqlite3, we just have to endure this. 
            
            # User wants to add a car
            elif selection == 4:
                # As the car brand is not optional, we ask for it as long as it takes to get one
                brand = ""
                while brand == "":
                    brand = input("Please give the brand: ")
                # As the model of the car is optional, we ask it for just once and go with it
                model = input("Please give the model (Enter for none): ")
                # Send the necessary data to be inserted in the Car table
                sql.insertCar(person[0], brand, model)
                # Now this will return user back to main menu, this is not the best practise, but 
                # as the reason for this program is to focus on sqlite3, we just have to endure this. 

            # User wants to see the list of cars
            elif selection == 5 and value[0] > 0:
                # Get the list of cars this person owns
                cars = sql.showCars(person[0])
                # Print the headers
                print("\tCar ID\tBrand"," " * 17,"Model")
                print("\t------","-" * 22, " ", "-----")
                # Print out the list of cars
                for car in cars:
                    print(f"\t{car[0]}\t{car[1]:20}\t{car[2]}")    
                print()
                # At this point, we could insert sql commands to manipulate the Car table data, but
                # I think this would be a perfect place for you to practise this. So feel free to add
                # UPDATE and DELETE commands to Car table here. :)
            
            # User wants to delete this person
            elif selection == 9:
                sql.deletePerson(person[0])
                print("Person deleted from database")

            # Any other number will produce error
            else:
                print("Invalid selection")    
        else:
            print("Invalid selection")


# Multiple persons found
def listofpersons(persons):
    # Print the list of results, start by creating table header
    print("Showing list of persons")
    print("\tPersonID\tFirst Name\tSurname")
    print("\t--------\t----------\t-------")
    # As we are working with list of tuples, loop through the list
    for person in persons:
        # print values inside this tuple
        print(f"\t{person[0]}\t\t{person[1]}\t\t{person[2]}")
    # Let's go to loop until user has selected a person from the list
    selection = 0
    while selection == 0:
        # Get the ID
        selection = input("Select ID: ")
        # Make sure selection is a number
        if selection.isnumeric():
            # Convert selection to int
            selection = int(selection)
            # Check if selection can be found in Person table
            value = sql.checkPid(selection)
            # If return value is anything but one, set selection back to 0 to stay in loop and print error
            if value[0] != 1:
                selection = 0
                print("Person ID not found")
        # Selection is not a number, set selection back to 0 to stay in loop and print error
        else:
            selection = 0
            print("Invalid ID")
    # Selection is a valid person id, so get information from selectPerson function. 
    # In this case we need to send the selection as a string or the function crashes.
    value = sql.selectPerson(str(selection))    
    # Return the single tuple that we got
    return value

    
def main():
    # Loop program until user ends it
    selection = -1
    while selection != 0:
        # Change text color to green and print options list for user to choose
        print(Fore.GREEN + "Person Database")
        print("\nSelect option:")
        print("\t(1) Search person")
        print("\t(2) Insert new person")
        print("\t(3) Show all the car information")
        print("\t(0) Quit")
        selection = input("> ")
        # Selection needs to be numeric for this program to work
        if selection.isnumeric() == True:
            # Convert selection from string to int
            selection = int(selection)
            
            # User wants to quit
            if selection == 0:
                # No need to do anything here right now
                pass
            
            # User wants to search the database
            elif selection == 1:
                # Get search parameter from user
                print("Please provide (part of) name or person id (Enter for all)")
                search = input("> ")
                # Fetch data from database
                value = sql.selectPerson(search)
                # If empty list was returned           
                if len(value) == 0:
                    print("There was no results, please try again.")
                # Only one tuple of values returned
                elif len(value) == 1:                
                    # Send the selected tuple to function person to show more info and options
                    person(value[0])
                    selection = -1
                # Multiple tuples returned in a list
                else:
                    # Send tuples to listofpersons function where user selects one person
                    p = listofpersons(value)
                    # Send the selected tuple to function person to show more info and options
                    person(p[0])
                    selection = -1
            
            # User wants to add a person to database
            elif selection == 2:
                # Get the required info, names cannot be null or empty
                sname = ""
                while sname == "":
                    if sname == "":
                        print("Please insert surname")
                    sname = input("Surname: ")
                fname = ""
                while fname == "":
                    if fname == "":
                        print("Please insert first name")
                    fname = input("First name: ")
                # Insert data to database
                value = sql.insertPerson(fname, sname)
                # Get confirmation
                print(f"{fname} {sname} added to database with ID number {value}")            
            
            # User wants to see everything about the cars
            elif selection == 3:
                # Get a list of all cars and owners
                value = sql.showCars()
                # Loop through results
                for item in value:
                    # If car model is None (NULL), we do not print it.
                    if item[3] is None :
                        print(item[0], item[1], "owns", item[2])
                    # All selected columns have values, so we print them all.
                    else:
                        print(item[0], item[1], "owns", item[2], item[3])
            # Any other number will produce error
            else:                
                print("Invalid choice")
        # Selection wasn't numeric, print error
        else:
            print("Invalid choice")
        print()

# Program starts
main()
# Program ends
print("\nThank you for using Person Database" + Fore.RESET) 
      




