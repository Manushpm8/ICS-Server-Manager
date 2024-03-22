import sys
from utilities import execute_command, printRows

def insertStudent(db_connection, cursor, argv): #task 2
    '''
    Insert a new student into the related tables.

    argv - UCINetID, email, First, Middle, Last
    return: bool
    '''

    user_insert = f"""
        INSERT INTO User (UCINetID, FirstName, MiddleName, LastName)
        SELECT '{argv[2]}', '{argv[4]}', '{argv[5]}', '{argv[6]}'
        WHERE NOT EXISTS (
            SELECT 1 FROM User WHERE UCINetID = '{argv[2]}'
        );
    """

    email_insert = f"""
        INSERT INTO UserEmail (UCINetID, Email)
        VALUES ('{argv[2]}', '{argv[3]}');
    """

    student_insert = f"""
        INSERT INTO Student (UCINetID)
        VALUES ('{argv[2]}');
    """

    user = execute_command(db_connection, cursor, user_insert)
    user_inserted = user[2].rowcount > 0

    if user_inserted and user[0] == "Success":
        execute_command(db_connection, cursor, email_insert)
        execute_command(db_connection, cursor, student_insert)
        print("Success")
    else:
        print("Fail")

def insertMachine(db_connection, cursor, argv): #task 5
    '''
    Insert a new machine.

    argv - MachineID, hostname, IPAddr, status, location
    return: bool
    '''
    
    sql_command = f"""
        INSERT INTO Machine (MachineID, hostname, IPAddr, status)
        SELECT '{argv[2]}', '{argv[3]}', '{argv[4]}', '{argv[5]}'
        WHERE NOT EXISTS (
            SELECT 1 FROM Machine WHERE MachineID = '{argv[2]}'
        );
    """

    machine = execute_command(db_connection, cursor, sql_command)
    machine_inserted = machine[2].rowcount > 0

    if machine_inserted and machine[0] == "Success":
        print("Success")
    else:
        print("Fail")

def listCourse(db_connection, cursor, argv): # task 8
    '''
    Given a student ID, list all unique courses the student attended. Ordered by courseId ascending.

    argv - UCINetID
    return: Table - CourseId,title,quarter
    '''
    
    sql_command = f"""
        SELECT DISTINCT
            c.CourseID, c.Title, c.Quarter    
        FROM
            StudentUse su, Project p, Course c 
        WHERE
            su.UCINetID = '{argv[2]}' and
            su.ProjectID = p.ProjectID and
            p.CourseID = c.CourseID
        ORDER BY
            c.CourseID ASC;
    """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)

def activeStudent(db_connection, cursor, argv): # task 11
    '''
    Given a machine Id, find all active students that used it more than N times (including N) in a 
    specific time range (including start and end date). Ordered by netid ascending. N will be at least 1.

    argv - MachineID, N, start, end
    return: Table - UCINetId,first name,middle name,last name
    '''
    
    sql_command = f"""
        SELECT
            u.UCINetID, u.FirstName, u.MiddleName, u.LastName
        FROM 
            StudentUse su, User u
        WHERE
            su.MachineID = {argv[2]} and
            su.StartDate >= '{argv[4]}' and
            su.EndDate <= '{argv[5]}' and
            su.UCINetID = u.UCINetID
        GROUP BY
            u.UCINetID
        HAVING
            Count(*) >= {argv[3]}
    """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)
