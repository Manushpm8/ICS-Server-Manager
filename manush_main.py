import sys
from utilities import execute_command, printRows

def deleteStudent(db_connection, cursor, argv):  # task 4
    '''
    Delete the student in both the User and Student table.

    argv - UCINetID
    return: bool
    '''

    sql_command = f"""
                DELETE FROM User
                WHERE UCINetID = '{argv[2]}';
            """

    result = execute_command(db_connection, cursor, sql_command)
    print(result[0])

def updateCourse(db_connection, cursor, argv):  # task 7
    '''
    Update the title of a course.

    argv: CourseId, title
    :return: Bool
    '''
    sql_command = f"""
                UPDATE Course
                SET Title = '{argv[3]}'
                WHERE CourseID = {argv[2]};
            """

    result = execute_command(db_connection, cursor, sql_command)
    print(result[0])

def adminEmails(db_connection, cursor, argv):  # task 10
    '''
    Given a machine ID, find all administrators of that machine. List the emails of those administrators. Ordered by netid ascending. 

    argv: machineId
    :return: Table - UCINETId,first name,middle name,last name,list of email
    '''
    sql_command = f"""
                SELECT 
                    User.UCINetID,
                    User.FirstName,
                    User.MiddleName,
                    User.LastName,
                    GROUP_CONCAT(UserEmail.Email ORDER BY UserEmail.Email ASC SEPARATOR ';') AS ListOfEmail
                FROM 
                    Administrator
                INNER JOIN 
                    AdministratorManageMachines ON Administrator.UCINetID = AdministratorManageMachines.AdministratorUCINetID
                INNER JOIN 
                    User ON Administrator.UCINetID = User.UCINetID
                INNER JOIN 
                    UserEmail ON User.UCINetID = UserEmail.UCINetID
                WHERE 
                    AdministratorManageMachines.MachineID = {argv[2]}
                GROUP BY 
                    User.UCINetID
                ORDER BY 
                    User.UCINetID ASC;
            """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)
