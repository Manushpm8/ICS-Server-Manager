import sys
from utilities import execute_command, printRows

def insertStudent(db_connection, argv): #task 2
    '''
    Insert a new student into the related tables.

    argv - UCINetID, email, First, Middle, Last
    return: bool
    '''

    sql_command = f"""
        INSERT INTO User (UCINetID, email, First, Middle, Last)
        VALUES ('{argv[2]}', '{argv[3]}', '{argv[4]}', '{argv[5]}', '{argv[6]}')

        INSERT INTO Student (UCINetID)
        VALUES ('{argv[2]}')
    """
    
    res = execute_command(db_connection, sql_command)
    print(res[0])

def insertMachine(db_connection, argv): #task 5
    '''
    Insert a new machine.

    argv - MachineID, hostname, IPAddr, status, location
    return: bool
    '''
    
    sql_command = f"""
        INSERT INTO Machine (MachineID, hostname, IPAddr, status)
        VALUES ({argv[2]}, '{argv[3]}', '{argv[4]}', '{argv[5]}')
    """

    res = execute_command(db_connection, sql_command)
    print(res[0])

def listCourse(db_connection, argv): # task 8
    '''
    Given a student ID, list all unique courses the student attended. Ordered by courseId ascending.

    argv - UCINetID
    return: Table - CourseId,title,quarter
    '''
    
    sql_command = f"""
        SELECT DISTINCT
            c.CourseID, c.*
            
        FROM
            Student s, StudentUse u, Project p, Course c
            
        WHERE
            s.UCINetID = '{argv[2]}' and
            s.UCINetID = u.UCINetID and
            u.ProjectID = p.ProjectID and
            p.CourseID = c.CourseID
            
        ORDER BY
            c.CourseID ASC
        
    """

    res = execute_command(db_connection, sql_command)
    printRows(res)

def activeStudent(db_connection, argv): # task 11
    '''
    Given a machine Id, find all active students that used it more than N times (including N) in a 
    specific time range (including start and end date). Ordered by netid ascending. N will be at least 1.

    argv - MachineID, N, start, end
    return: Table - UCINetId,first name,middle name,last name
    '''
    
    sql_command = f"""
        SELECT
            s.UCINetID, s.*

        FROM Student s, StudentUse u, Machine m
        
        WHERE
            s.UCINetID = u.UCINetID and 
            u.MachineID = {argv[2]} and
            u.MachineID = m.MachineID and
            u.StartDate <= '{argv[4]}' and u.EndDate >= '{argv[5]}'
            
        GROUP BY
            s.UCINetID
            
        HAVING
            COUNT(*) > {argv[3]}
            
        ORDER BY
            s.UCINetID ASC 
    """

    res = execute_command(db_connection, sql_command)
    printRows(res)
