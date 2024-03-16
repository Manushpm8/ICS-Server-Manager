import csv


def getCsvDataQuery(file_path):
    query = "INSERT INTO"
    if ('admins.csv' in file_path):
        query += " Administrators "
    elif ('courses.csv' in file_path):
        query += " Courses "
    elif ('emails.csv' in file_path):
        query += " UserEmail "
    elif ('machines.csv' in file_path):
        query += " Machines "
    elif ('manage.csv' in file_path):
        query += " AdministratorManageMachines "
    elif ('projects.csv' in file_path):
        query += " Projects "
    elif ('students.csv' in file_path):
        query += " Students "
    elif ('use.csv' in file_path):
        query += " StudentUseMachinesInProject "
    elif ('users.csv' in file_path):
        query += " Users "
    
    query += "VALUES \n"

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        for line in csv_reader:
            query += "("
            for value in line:
                query += "\'" + value + "\', "
            query = query[:-2] + "), \n"

        query = query[:-3] + ";"
    
    return query