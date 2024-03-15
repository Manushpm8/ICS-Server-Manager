import csv


def getCsvDataQuery(file_path):
    query = "INSERT INTO"
    if ('admins.csv' in file_path):
        query += " `Administrators` "
    elif ('courses.csv' in file_path):
        query += " `Courses` "
    elif ('emails.csv' in file_path):
        query += " `UserEmail` "
    elif ('machines.csv' in file_path):
        query += " `Machines` "
    elif ('manage.csv' in file_path):
        query += " `AdministratorManageMachines` "
    elif ('projects.csv' in file_path):
        query += " `Projects` "
    elif ('students.csv' in file_path):
        query += " `Students` "
    elif ('use.csv' in file_path):
        query += " `StudentUseMachinesInProject` "
    elif ('users.csv' in file_path):
        query += " `Users` "
    
    query += "VALUES \n"

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)

        for line in csv_reader:
            query += "("
            for value in line:
                query += "\'" + value + "\', "
            query = query[:-2] + "), \n"

        query = query[:-3] + ";"
    
    return query



def execute_command(db_connection, cursor, sql_command):
    '''
    Executes sql command in connection.

    :return: Bool, optional results
    '''
    try:
        # print("Successfully connected to the database")
        # print("Initialization begin")

        cursor.execute(sql_command)

        result = cursor.fetchall()
        # print(result)

        db_connection.commit()
        # print("Initialization end successfully")

        return "Success", result
    except Exception as e:
        print(e)
        return "Fail", []
    


def printRows(result):
    '''
    Formats result printing from table to csv

    - arg: result table
    - returns:  None
    '''
    for record in result:
        formatted_record = ','.join(str(value) for value in record)
        print(formatted_record)