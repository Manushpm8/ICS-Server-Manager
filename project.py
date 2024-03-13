import sys
from constants import Constants
import mysql.connector

from run_initialization import run_initialization
from utilities import getCsvDataQuery

def main():
    args = sys.argv[1:]
    func = args[0]
    sql_file_path = 'cs122a_db.sql'

    db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)

    if (func == "import"):

        try:
            cursor = db_connection.cursor()
            print("Successfully connected to the database")
            print("Initialization begin")

            with open(sql_file_path, 'r') as file:
                sql_script = file.read()

            for statement in sql_script.split(';'):
                if statement.strip():
                    print("running: ", statement)
                    cursor.execute(statement)
            
            cursor.execute(getCsvDataQuery("test_data/users.csv"))
            cursor.execute(getCsvDataQuery("test_data/students.csv"))
            cursor.execute(getCsvDataQuery("test_data/admins.csv"))        
            cursor.execute(getCsvDataQuery("test_data/courses.csv"))
            cursor.execute(getCsvDataQuery("test_data/projects.csv"))
            cursor.execute(getCsvDataQuery("test_data/machines.csv"))
            cursor.execute(getCsvDataQuery("test_data/emails.csv"))
            cursor.execute(getCsvDataQuery("test_data/use.csv"))
            cursor.execute(getCsvDataQuery("test_data/manage.csv"))
            result = cursor.fetchall()

            print(result)

            db_connection.commit()
            print("Initialization end successfully")

        except mysql.connector.Error as error:
            print(f"Failed to execute SQL script: {error}")
            
    elif (func == "insertStudent"):
        print(func)
    elif (func == "addEmail"):
        print(func)
    elif (func == "deleteStudent"):
        print(func)
    elif (func == "insertMachine"):
        print(func)
    elif (func == "insertUse"):
        print(func)
    elif (func == "updateCourse"):
        print(func)
    elif (func == "listCourse"):
        print(func)
    elif (func == "popularCourse"):
        print(func)
    elif (func == "adminEmails"):
        print(func)
    elif (func == "activeStudent"):
        print(func)
    elif (func == "machineUsage"):
        print(func)

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("MySQL connection is closed")

    return 0

if __name__ == "__main__":
    main()