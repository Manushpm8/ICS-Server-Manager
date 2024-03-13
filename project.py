import sys
from constants import Constants
import mysql.connector

from run_initialization import run_initialization
from utilities import getCsvDataQuery

def main():
    args = sys.argv[1:]
    func = args[0]

    run_initialization()
    connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)
    cursor = connection.cursor()

    if (func == "import"):
        cursor.execute(getCsvDataQuery("test_data/users.csv"))
        # cursor.execute(getCsvDataQuery("test_data/emails.csv"))
        cursor.execute(getCsvDataQuery("test_data/students.csv"))
        cursor.execute(getCsvDataQuery("test_data/admins.csv"))
        cursor.execute(getCsvDataQuery("test_data/courses.csv"))
        cursor.execute(getCsvDataQuery("test_data/projects.csv"))
        cursor.execute(getCsvDataQuery("test_data/machines.csv"))
        cursor.execute(getCsvDataQuery("test_data/use.csv"))
        cursor.execute(getCsvDataQuery("test_data/manage.csv"))
        result = cursor.fetchall()

        print(result)

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

    cursor.close()
    connection.close()

    return 0

if __name__ == "__main__":
    main()