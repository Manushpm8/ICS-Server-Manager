import sys
import csv
import os


def addEmail(argv):  # task 3
    '''
    Add email to a user

    argv - UCINetID, email
    return: bool
    '''

    # try:
        # cursor.execute() except: return False

    sql_command = """
            INSERT INTO users (UCINetID, email)
            VALUES (argv[2], argv[3]);
        """

    return True


def insertUse(argv):  # task 6
    '''
    Insert a new use record for student use machine for project.

    :param argv: ProjID, UCINetID, MachineID, start, end
    ex: 2005 testID 102 2023-01-09 2023-03-10
    :return: Bool
    '''
    sql_command = """
            INSERT INTO use (ProjID, UCINetID, MachineID, start, end)
            VALUES (argv[2], argv[3], argv[4], argv[5], argv[6])
        """
    return True


def popularCourse(argv):  # task 9
    '''
    List the top N course that has the most students attended.
    Ordered by studentCount, courseID descending.

    :param argv: N
    :return: Table - CourseId,title,studentCount
    '''
    sql_command = """
        SELECT CourseID, Title, COUNT(DISTINCT students) AS studentCount
        FROM courses
        ORDER BY studentCount, courseID DESC
        LIMIT argv[2];
        """


def machineUsage(argv):  # task 12
    '''
    Given a course id, count the number of usage of each machine in that course.  Each unique
    record in the MachineUse table counts as one usage. Machines that are not used in the course
    should have a count of 0 instead of NULL. Ordered by machineId descending.

    :param argv: machineId
    :return: Table - machineID,hostname,ipAddr,count
    '''
    sql_command = """
            SELECT M.machineID, M.hostname, M.ipAddr, IF(M.useCount = NULL, 0, M.useCount)
            FROM (SELECT COUNT(DISTINCT *) as useCount
                FROM use as U
                GROUP BY U.machineID
            ), machine as M
            ORDER BY M.MachineID DESC   
            LIMIT argv[2];
        """



if __name__ == "__main__":
    # argv[0] = project.py
    # argv[1] = <function name>

    if len(sys.argv) > 1:
        function_name = globals()[sys.argv[1]]
        function_name(sys.argv)
