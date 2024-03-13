import sys
import csv
import os

def get_files(folder):
    '''
    Open folder and returns list of file paths inside.

    :param folder:
    :return:
    '''
    pass

def read_file(file):
    '''
    reads csv file and puts in database
    :param file:
    :return:
    '''
    pass

def set_up():
    '''
    Sets up database by clearing existing tabels.
    :return:
    '''
    pass
def import_file(argv):  # task 1
    '''
    Delete existing tables, and create new tables. Then read the csv files
    in the given folder and import data into database.

    argv - folder of csv files
    Table - Number of users,Number of machine, Number of Course
    '''
    path = argv[2]
    files = os.listdir(path)

    csv_files = [i for i in files if i.endswith('.csv')]
    #cursor.execute()

    sql_command = """
    """

    # return bool??


def deleteStudent(argv):  # task 4
    '''
    deletes student in both Student & User table
    :param argv: UCINetID
    :return: Bool
    '''
    sql_command = """
        

    """

    # return bool??


def updateCourse (argv):  # task 7
    '''
    Update the title of a course
    :param argv: CourseId, Title
    :return: Bool
    '''
    sql_command = """
        
    """


def adminEmails(argv):  # task 10
    '''
    Given a machine ID, find all administrators of that machine. List the emails of those
    administrators. Ordered by netid ascending.

    :param argv: machineId
    :return: Table - UCINETId,first name,middle name,last name,list of email
    '''
    sql_command = """
        
    """


if __name__ == "__main__":
    # argv[0] = project.py
    # argv[1] = <function name>

    if len(sys.argv) >= 2:
        if sys.argv[1] == 'import':
            import_file(sys.argv[2])
        else:
            function_name = globals()[sys.argv[1]]
            function_name(sys.argv)
