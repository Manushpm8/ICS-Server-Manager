import sys
from utilities import execute_command


def addEmail(db_connection, argv):  # task 3
    '''
    Add email to a user

    argv - UCINetID, email
    return: bool
    '''

    sql_command = f"""
                INSERT INTO users (UCINetID, email)
                VALUES ('{argv[2]}', '{argv[3]}');
            """
    print(sql_command)
    res = execute_command(db_connection, sql_command)
    print(res)
    print(res[0])


def insertUse(db_connection, argv):  # task 6
    '''
    Insert a new use record for student use machine for project.

    argv: ProjID, UCINetID, MachineID, start, end
    ex: 2005 testID 102 2023-01-09 2023-03-10
    :return: Bool
    '''
    sql_command = f"""
            INSERT INTO use (ProjID, UCINetID, MachineID, start, end)
            VALUES ({argv[2]}, '{argv[3]}', {argv[4]}, '{argv[5]}', '{argv[6]}')
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
    sql_command = f"""
        SELECT CourseID, Title, COUNT(DISTINCT students) AS studentCount
        FROM courses
        ORDER BY studentCount, courseID DESC
        LIMIT {argv[2]};
        """

    res = execute_command(db_connection, sql_command)
    print(res[1])


def machineUsage(db_connection, argv):  # task 12
    '''
    Given a course id, count the number of usage of each machine in that course.  Each unique
    record in the MachineUse table counts as one usage. Machines that are not used in the course
    should have a count of 0 instead of NULL. Ordered by machineId descending.

    argv: machineId
    :return: Table - machineID,hostname,ipAddr,count
    '''

    sql_command = """
            SELECT M.machineID, M.hostname, M.ipAddr, IF(M.useCount = NULL, 0, M.useCount)
            FROM (SELECT COUNT(DISTINCT *) as useCount
                FROM use as U
                GROUP BY U.machineID
            ), machine as M
            ORDER BY M.MachineID DESC   
        """

    res = execute_command(db_connection, sql_command)
    print(res[1])

