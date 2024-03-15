import sys
from constants import Constants
import mysql.connector
from mew_main import *
from jocelyn_main import *
from manush_main import *

from run_initialization import run_initialization
from utilities import getCsvDataQuery

def main():
    args = sys.argv[1:]
    func = args[0]
    sql_file_path = 'cs122a_db.sql'

    db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)
    cursor = db_connection.cursor()

    if (func == "import"):

        try:
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
            print('False')
            
    else:
        function_selected = globals()[sys.argv[1]]
        function_selected(db_connection, sys.argv)

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("MySQL connection is closed")

    return 0

if __name__ == "__main__":
    main()