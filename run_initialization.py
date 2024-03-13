import mysql.connector
from constants import Constants

# This script will initialize your local DB to have the table created and data loaded
# please make sure that you have filled in the constants correctly to run this query successfully
sql_file_path = 'cs122a_db.sql'

# Create a connection to the database
def run_initialization():
    try:
        db_connection = mysql.connector.connect(user=Constants.USER, password=Constants.PASSWORD, database=Constants.DATABASE)

        cursor = db_connection.cursor()
        print("Successfully connected to the database")
        print("Initialization begin")

        # Open and read the SQL file
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        # Execute each statement in the SQL file
        for statement in sql_script.split(';'):
            # Ignore empty statements (which can occur due to splitting by ';')
            if statement.strip():
                print("running: ", statement)
                cursor.execute(statement)

        db_connection.commit()
        print("Initialization end successfully")

    except mysql.connector.Error as error:
        print(f"Failed to execute SQL script: {error}")

    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed")