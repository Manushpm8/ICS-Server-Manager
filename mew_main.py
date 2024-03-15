import sys

def execute_command(db_connection, sql_command):
    '''
    Executes sql command in connection.

    :return: Bool, optional results
    '''
    try:
        cursor = db_connection.cursor()
        print("Successfully connected to the database")
        print("Initialization begin")

        cursor.execute(sql_command)
        result = cursor.fetchall()

        # print(result)

        db_connection.commit()
        print("Initialization end successfully")
        return 'Success', result
    except Exception as e:
        print(e)
        return 'Fail'

def printRows(result):
    '''
    Formats result printing from table to csv

    - arg: result table
    - returns:  None
    '''
    for row in result:
        print(','.join(row.split()))


def addEmail(db_connection, argv):  # task 3
    '''
    Add email to a user email table.

    argv - UCINetID, email
    return: bool
    '''

    sql_command = """
                INSERT INTO UserEmail (UCINetID, email)
                VALUES (argv[2], argv[3]);
            """
    res = execute_command(db_connection, sql_command)
    print(res[0])


def insertUse(db_connection, argv):  # task 6
    '''
    Insert a new use record for student use machine for project.

    argv: ProjID, UCINetID, MachineID, start, end
    ex: 2005 testID 102 2023-01-09 2023-03-10
    :return: Bool
    '''
    sql_command = """
            INSERT INTO StudentUseMachinesInProject
                (ProjectID, StudentUCINetID, MachineID, StartDate, EndDate)
            VALUES (argv[2], argv[3], argv[4], DATE(argv[5]), DATE(argv[6]))
        """
    res = execute_command(db_connection, sql_command)
    print(res[0])


def popularCourse(db_connection, argv):  # task 9
    '''
    List the top N course that has the most students attended.
    Ordered by studentCount, courseID descending.

    argv: N
    :return: Table - CourseId,title,studentCount
    '''
    sql_command = """
        SELECT C.CourseID, C.Title, COUNT( DISTINCT S.UCINetID) AS studentCount
        FROM Courses as C
        JOIN Projects as P ON P.CourseID = C.CourseID
        JOIN StudentUseMachinesInProject as S ON S.ProjectID = P.ProjectID
        GROUP BY C.CourseID, C.Title
        ORDER BY studentCount DESC, C.CourseID
        LIMIT argv[2];
        """

    res = execute_command(db_connection, sql_command)
    printRows(res)


def machineUsage(db_connection, argv):  # task 12
    '''
    Given a course id, count the number of usage of each machine in that course.  Each unique
    record in the MachineUse table counts as one usage. Machines that are not used in the course
    should have a count of 0 instead of NULL. Ordered by machineId descending.

    argv: machineId
    :return: Table - machineID,hostname,ipAddr,count
    '''

    sql_command = """
        SELECT M1.MachineID, M1.Hostname, M1.IPAddress, M1.IFNULL(useCount, 0)
        FROM
            (SELECT M.MachineID, M.Hostname, M.IPAddress, COUNT(DISTINCT P.ProjectID) as useCount
            FROM StudentUseMachinesInProject as U
            JOIN Machines as M ON MachineID=U.MachineID
            JOIN Projects as P ON P.ProjectID=U.ProjectID
            WHERE P.CourseID = argv[2]
            GROUP BY M.MachineID, M.Hostname, M.IPAddress
            ORDER BY M.MachineID DESC) as M1;
        """

    res = execute_command(db_connection, sql_command)
    printRows(res)


if __name__ == "__main__":
    # argv[0] = project.py
    # argv[1] = <function name>

    if len(sys.argv) > 1:
        function_name = globals()[sys.argv[1]]
        function_name(sys.argv)
