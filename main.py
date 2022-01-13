import mysql.connector
from mysql.connector import Error

#Gets initial connection to MySql database
def get_connection(hostname, username, password, database):
    connection = None

    try:
        connection = mysql.connector.connect(host=hostname, user=username, passwd=password, database=database)

    except Error as err:
        print(f"Error: '{err}'")

    return(connection)

#Initializes table if not created already
def init_table(connection):
    cursor = connection.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS workHours (
            id int AUTO_INCREMENT,
            date DATE,
            hours int,
            PRIMARY KEY(id)
        );
    """
    
    try:
        cursor.execute(query)
        connection.commit()

    except Error as err:
        print(f"Error: '{err}'")

#Insert a new hours value into the table
def insert_hours(date, hours, connection):
    cursor = connection.cursor()

    query = """
        INSERT INTO workHours (date, hours) VALUES (%s, %s);
    """

    val = (date, hours)

    try:
        cursor.execute(query, val)
        connection.commit()

    except Error as err:
        print(f"Error: '{err}'")

#Returns all data from the table
def get_values(connection):
    cursor = connection.cursor()

    query = """
        SELECT * FROM workHours
    """

    try:
        cursor.execute(query)
        resultSet = cursor.fetchall()

    except Error as err:
        print(f"Error: '{err}'")
        resultSet = None

    return(resultSet)

#Prints out all data from the table
def print_values(connection):
    dataSet = get_values(connection)

    for x in dataSet:
        print("{}. Date: {} - Hours: {}".format(x[0], x[2], x[1]))

#Delete one piece of data from the table
def delete_value(connection):
    print("Which date to delete? (Enter the ID from the list)")
    chosen = int(input())

    cursor = connection.cursor()

    query = """
        DELETE FROM workHours WHERE id = %s
    """

    val = (chosen, )

    try:
        cursor.execute(query, val)
        connection.commit()
    
    except Error as err:
        print(f"Error: '{err}'")

#Main driver
def main():
    # Enter database login info
    print("Enter hostname: ")
    hostname = str(input())

    print("Enter username: ")
    username = str(input())

    print("Enter password: ")
    password = str(input())

    print("Enter database to access: ")
    database = str(input())

    connection = get_connection(hostname, username, password, database)

    #Check that connection set up correctly
    if connection != None:
        init_table(connection)

        loop = True

        while (loop):
            print("\n--SELECT OPTIONS--")
            print("1. Enter work data")
            print("2. Delete a value from the database")
            print("3. Print all data in the database")
            print("4. Exit")

            usrChoice = int(input())
            print()

            #Add a date and hour pair
            if usrChoice == 1:
                #Enter each value
                print("Enter work date (Y-M-D): ")
                date = str(input())

                print("Enter hours worked: ")
                hours = int(input())

                insert_hours(date, hours, connection)

                print("Done!")

            #Delete one value from the table            
            elif usrChoice == 2:
                print_values(connection)
                delete_value(connection)

            #Prints all values in the table
            elif usrChoice == 3:
                print_values(connection)

            #Exits
            elif usrChoice == 4:
                loop = False

            else:
                print("That isn't a valid choice!")
        

if __name__ == "__main__":
    main()
