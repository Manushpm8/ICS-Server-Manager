import sys
from utilities import execute_command, printRows


def deleteStudent(db_connection, cursor, argv):  # task 4
    '''
    Delete the student in both the User and Student table.

    argv - UCINetID
    return: bool
    '''

    sql_command = f"""
                DELETE FROM users
                WHERE UCINetID = '{argv[2]}';
            """
    
    res = execute_command(db_connection, cursor, sql_command)
    print(res[0])


def updateCourse(db_connection, cursor, argv):  # task 7
    '''
    Update the title of a course.

    argv: CourseId, title
    :return: Bool
    '''
    sql_command = f"""
                UPDATE Courses
                SET Title = '{argv[3]}'
                WHERE CourseID = {argv[2]};
            """

    res = execute_command(db_connection, cursor, sql_command)
    print(res[0])


def adminEmails(db_connection, cursor, argv):  # task 10
    '''
    Given a machine ID, find all administrators of that machine. List the emails of those administrators. Ordered by netid ascending. 

    argv: machineId
    :return: Table - UCINETId,first name,middle name,last name,list of email
    '''
    sql_command = f"""
                SELECT 
                    Users.UCINetID,
                    Users.FirstName,
                    Users.MiddleName,
                    Users.LastName,
                    GROUP_CONCAT(UserEmail.Email ORDER BY UserEmail.Email ASC SEPARATOR ';') AS ListOfEmail
                FROM 
                    Administrators
                INNER JOIN 
                    AdministratorManageMachines ON Administrators.UCINetID = AdministratorManageMachines.AdministratorUCINetID
                INNER JOIN 
                    Users ON Administrators.UCINetID = Users.UCINetID
                INNER JOIN 
                    UserEmail ON Users.UCINetID = UserEmail.UCINetID
                WHERE 
                    AdministratorManageMachines.MachineID = {argv[2]}
                GROUP BY 
                    Users.UCINetID
                ORDER BY 
                    Users.UCINetID ASC;
            """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)

