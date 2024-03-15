import sys
from constants import Constants
import mysql.connector
from mew_main import *
from jocelyn_main import *
from manush_main import *

from utilities import getCsvDataQuery

def main():
    args = sys.argv[1:]
    func = args[0]
    sql_file_path = 'cs122a_final.sql'

    db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)
    cursor = db_connection.cursor()

    if func == "import":
        sql_command = f"""
                SELECT
                    (SELECT COUNT(*) FROM Users) AS NumberOfUsers,
                    (SELECT COUNT(*) FROM Machines) AS NumberOfMachines,
                    (SELECT COUNT(*) FROM Courses) AS NumberOfCourses;
            """

        try:
            # print("Successfully connected to the database")
            # print("Initialization begin")

            with open(sql_file_path, 'r') as file:
                sql_script = file.read()

            for statement in sql_script.split(';'):
                if statement.strip():
                    # print("running: ", statement)
                    cursor.execute(statement)

            folder = args[1]
            
            cursor.execute(getCsvDataQuery(f"{folder}/users.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/students.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/admins.csv"))        
            cursor.execute(getCsvDataQuery(f"{folder}/courses.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/projects.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/machines.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/emails.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/use.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/manage.csv"))
            cursor.execute(sql_command)

            result = cursor.fetchall()
            printRows(result)

            db_connection.commit()
            # print("Initialization end successfully")

        except mysql.connector.Error as error:
            print(f"Failed to execute SQL script: {error}")
            print('False')
            
    else:
        function_selected = globals()[sys.argv[1]]
        function_selected(db_connection, cursor, sys.argv)

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        # print("MySQL connection is closed")

    return 0

if __name__ == "__main__":
    main()