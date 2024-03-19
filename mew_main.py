import sys
from utilities import execute_command, printRows


def addEmail(db_connection, cursor, argv):  # task 3
    '''
    Add email to a user email table.

    argv - UCINetID, email
    return: bool
    '''

    sql_command = f"""
                INSERT INTO UserEmail (UCINetID, email)
                VALUES ('{argv[2]}', '{argv[3]}');
            """

    res = execute_command(db_connection, cursor, sql_command)
    print(res[0])


def insertUse(db_connection, cursor, argv):  # task 6
    '''
    Insert a new use record for student use machine for project.

    argv: ProjID, UCINetID, MachineID, start, end
    ex: 2005 testID 102 2023-01-09 2023-03-10
    :return: Bool
    '''
    sql_command = f"""
            INSERT INTO StudentUseMachinesInProject
                (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate)
            VALUES ({argv[2]}, '{argv[3]}', {argv[4]}, '{argv[5]}', '{argv[6]}')
        """
    
    res = execute_command(db_connection, cursor, sql_command)
    print(res[0])


def popularCourse(db_connection, cursor, argv):  # task 9
    '''
    List the top N course that has the most students attended.
    Ordered by studentCount, courseID descending.

    argv: N
    :return: Table - CourseId,title,studentCount
    '''
    sql_command = f"""
        SELECT C.CourseID, C.Title, COUNT( DISTINCT S.StudentUCINetID) AS studentCount
        FROM Courses as C
        JOIN Projects as P ON P.CourseID = C.CourseID
        JOIN StudentUseMachinesInProject as S ON S.ProjectID = P.ProjectID
        GROUP BY C.CourseID, C.Title
        ORDER BY studentCount DESC, C.CourseID
        LIMIT {argv[2]};
        """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)


def machineUsage(db_connection, cursor, argv):  # task 12
    '''
    Given a course id, count the number of usage of each machine in that course.  Each unique
    record in the MachineUse table counts as one usage. Machines that are not used in the course
    should have a count of 0 instead of NULL. Ordered by machineId descending.

    argv: courseID
    :return: Table - machineID,hostname,ipAddr,count
    '''

    sql_command = f"""
        SELECT M.MachineID, M.Hostname, M.IPAddress, IFNULL(Count(M.MachineID), 0) as useCount
            FROM StudentUseMachinesInProject as U
            LEFT JOIN Machines as M ON M.MachineID=U.MachineID
            LEFT JOIN Projects as P ON P.ProjectID=U.ProjectID
            WHERE P.CourseID = {argv[2]}
            GROUP BY M.MachineID, M.Hostname, M.IPAddress, P.CourseID
        UNION
        SELECT M1.MachineID, M1.Hostname, M1.IPAddress, 0
            FROM Machines as M1
            WHERE M1.MachineID NOT IN (
                SELECT M2.MachineID
                FROM StudentUseMachinesInProject as U2, Machines as M2, Projects as P2
                WHERE M2.MachineID=U2.MachineID and P2.ProjectID=U2.ProjectID and P2.CourseID = {argv[2]}
                GROUP BY M2.MachineID, M2.Hostname, M2.IPAddress, P2.CourseID
            ) 
        ORDER BY MachineID DESC; 
        """
    sql_test_1 = f'''
    SELECT M.MachineID, M.Hostname, M.IPAddress, IFNULL(Count(M.MachineID), 0) as useCount
            FROM StudentUseMachinesInProject as U
            LEFT JOIN Machines as M ON M.MachineID=U.MachineID
            LEFT JOIN Projects as P ON P.ProjectID=U.ProjectID
            GROUP BY M.MachineID, M.Hostname, M.IPAddress, P.CourseID
            ORDER BY M.MachineID DESC
    '''
    sql_test_6 = f'''
    SELECT M.MachineID, M.Hostname, M.IPAddress, Count(M.MachineID) as useCount
            FROM StudentUseMachinesInProject as U
            LEFT JOIN Machines as M ON M.MachineID=U.MachineID
            LEFT JOIN Projects as P ON P.ProjectID=U.ProjectID
            WHERE P.CourseID = {argv[2]}
            GROUP BY M.MachineID, M.Hostname, M.IPAddress, P.CourseID
    UNION
    SELECT M1.MachineID, M1.Hostname, M1.IPAddress, 0
        FROM Machines as M1
        WHERE M1.MachineID NOT IN (
            SELECT M2.MachineID
            FROM StudentUseMachinesInProject as U2, Machines as M2, Projects as P2
            WHERE M2.MachineID=U2.MachineID and P2.ProjectID=U2.ProjectID and P2.CourseID = {argv[2]}
            GROUP BY M2.MachineID, M2.Hostname, M2.IPAddress, P2.CourseID
        ) 
    ORDER BY MachineID DESC; 
    '''
    # GROUP BY M.MachineID, M.Hostname, M.IPAddress, P.CourseID
    test_round = False
    if test_round:
        test = execute_command(db_connection, cursor, sql_test_6)
        printRows(test)
    else:
        res = execute_command(db_connection, cursor, sql_command)
        printRows(res)
