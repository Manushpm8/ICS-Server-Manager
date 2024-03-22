import sys
import mysql.connector
import csv


# SQL SET UP -------------------------------------------------------------------------------------------------------------------------------

USER = "test"
PASSWORD = "password"
DATABASE = "cs122a"
DB_SETUP = """
    DROP DATABASE IF EXISTS cs122a;
    CREATE DATABASE cs122a;
    USE cs122a;

    -- User Table
    CREATE TABLE User (
        UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
        FirstName VARCHAR(50),
        MiddleName VARCHAR(50),
        LastName VARCHAR(50)
    );

    CREATE TABLE UserEmail (
    UCINetID VARCHAR(20) NOT NULL,
    Email    VARCHAR(255),
    PRIMARY KEY (UCINetID, Email),
    FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
        ON DELETE CASCADE
    );

    -- Student Delta Table
    CREATE TABLE Student (
        UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
        FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
        ON DELETE CASCADE
    );

    -- Administrator Delta Table
    CREATE TABLE Administrator (
        UCINetID VARCHAR(20) PRIMARY KEY NOT NULL,
        FOREIGN KEY (UCINetID) REFERENCES User(UCINetID)
        ON DELETE CASCADE
    );

    -- Course Table
    CREATE TABLE Course (
        CourseID INT PRIMARY KEY NOT NULL ,
        Title VARCHAR(100),
        Quarter VARCHAR(20)
    );

    -- Project Table
    CREATE TABLE Project (
        ProjectID INT PRIMARY KEY NOT NULL,
        Name VARCHAR(100),
        Description TEXT,
        CourseID INT NOT NULL,
        FOREIGN KEY (CourseID) REFERENCES Course(CourseID)
        ON DELETE CASCADE
    );

    -- Machine Table
    CREATE TABLE Machine (
        MachineID INT PRIMARY KEY NOT NULL,
        Hostname VARCHAR(255),
        IPAddress VARCHAR(15),
        OperationalStatus VARCHAR(50),
        Location VARCHAR(255)
    );


    -- Use Relationship Table
    CREATE TABLE StudentUse (
        ProjectID INT,
        UCINetID VARCHAR(20),
        MachineID INT,
        StartDate DATE,
        EndDate DATE,
        PRIMARY KEY (ProjectID, UCINetID, MachineID),
        FOREIGN KEY (ProjectID) REFERENCES Project(ProjectID)
        ON DELETE CASCADE,
        FOREIGN KEY (UCINetID) REFERENCES Student(UCINetID)
        ON DELETE CASCADE,
        FOREIGN KEY (MachineID) REFERENCES Machine(MachineID)
        ON DELETE CASCADE
    );

    -- Administrator Machine Management Table
    CREATE TABLE AdministratorManageMachines (
        AdministratorUCINetID VARCHAR(20),
        MachineID INT,
        PRIMARY KEY (AdministratorUCINetID, MachineID),
        FOREIGN KEY (AdministratorUCINetID) REFERENCES Administrator(UCINetID)
        ON DELETE CASCADE,
        FOREIGN KEY (MachineID) REFERENCES Machine(MachineID)
        ON DELETE CASCADE
    );

"""


# UTILITY FILE -----------------------------------------------------------------------------------------------------------

def getCsvDataQuery(file_path):
    query = "INSERT INTO"
    if ('admins.csv' in file_path):
        query += " Administrator "
    elif ('courses.csv' in file_path):
        query += " Course "
    elif ('emails.csv' in file_path):
        query += " UserEmail "
    elif ('machines.csv' in file_path):
        query += " Machine "
    elif ('manage.csv' in file_path):
        query += " AdministratorManageMachines "
    elif ('projects.csv' in file_path):
        query += " Project "
    elif ('students.csv' in file_path):
        query += " Student "
    elif ('use.csv' in file_path):
        query += " StudentUse "
    elif ('users.csv' in file_path):
        query += " User "

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


def execute_command(db_connection, cursor, sql_command):
    '''
    Executes sql command in connection.

    :return: Bool, optional results
    '''
    try:
        # print("Successfully connected to the database")
        # print("Initialization begin")

        cursor.execute(sql_command)

        result = cursor.fetchall()
        # print(result)

        db_connection.commit()
        # print("Initialization end successfully")

        return "Success", result, cursor
    except Exception as e:
        print(e)
        return "Fail", []


def printRows(result):
    '''
    Formats result printing from table to csv

    - arg: result table
    - returns:  None
    '''

    if result[0] == 'Fail':
        print(result)
    elif result[0] == 'Success':
        for record in result[1]:
            formatted_record = ','.join(str(value) for value in record)
            print(formatted_record)
    else:
        for record in result:
            formatted_record = ','.join(str(value) for value in record)
            print(formatted_record)


# MANUSH FILE -------------------------------------------------------------------------------------------------------------------

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

    delete = execute_command(db_connection, cursor, sql_command)
    student_deleted = delete[2].rowcount > 0

    if student_deleted and delete[0] == "Success":
        print("Success")
    else:
        print("Fail")


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

    update = execute_command(db_connection, cursor, sql_command)
    course_updated = update[2].rowcount > 0

    if course_updated and update[0] == "Success":
        print("Success")
    else:
        print("Fail")


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


# MEW FILE ----------------------------------------------------------------------------------------------------------------------

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

    result = execute_command(db_connection, cursor, sql_command)
    print(result[0])


def insertUse(db_connection, cursor, argv):  # task 6
    '''
    Insert a new use record for student use machine for project.

    argv: ProjID, UCINetID, MachineID, start, end
    ex: 2005 testID 102 2023-01-09 2023-03-10
    :return: Bool
    '''
    sql_command = f"""
            INSERT INTO StudentUse
                (ProjectID, UCINetID, MachineID, StartDate, EndDate)
            VALUES ({argv[2]}, '{argv[3]}', {argv[4]}, '{argv[5]}', '{argv[6]}');
        """

    result = execute_command(db_connection, cursor, sql_command)
    print(result[0])


def popularCourse(db_connection, cursor, argv):  # task 9
    '''
    List the top N course that has the most students attended.
    Ordered by studentCount, courseID descending.

    argv: N
    :return: Table - CourseId,title,studentCount
    '''
    sql_command = f"""
        SELECT 
            C.CourseID, C.Title, COUNT(DISTINCT S.UCINetID) AS studentCount
        FROM 
            Course as C
        JOIN 
            Project as P ON P.CourseID = C.CourseID
        JOIN 
            StudentUse as S ON S.ProjectID = P.ProjectID
        GROUP BY 
            C.CourseID, C.Title
        ORDER BY 
            studentCount DESC, C.CourseID DESC
        LIMIT 
            {argv[2]};
        """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)


def machineUsage(db_connection, cursor, argv):  # task 12
    '''
    Given a course id, count the number of usage of each machine in that course.  Each unique
    record in the MachineUse table counts as one usage. Machine that are not used in the course
    should have a count of 0 instead of NULL. Ordered by machineId descending.

    argv: courseID
    :return: Table - machineID,hostname,ipAddr,count
    '''

    sql_command = f"""
        SELECT M.MachineID, M.Hostname, M.IPAddress, Count(M.MachineID) as useCount
            FROM StudentUse as U
            LEFT JOIN Machine as M ON M.MachineID=U.MachineID
            LEFT JOIN Project as P ON P.ProjectID=U.ProjectID
            WHERE P.CourseID = {argv[2]}
            GROUP BY M.MachineID, M.Hostname, M.IPAddress, P.CourseID
        UNION
        SELECT M1.MachineID, M1.Hostname, M1.IPAddress, 0
            FROM Machine as M1
            WHERE M1.MachineID NOT IN (
                SELECT M2.MachineID
                FROM StudentUse as U2, Machine as M2, Project as P2
                WHERE M2.MachineID=U2.MachineID and P2.ProjectID=U2.ProjectID and P2.CourseID = {argv[2]}
                GROUP BY M2.MachineID, M2.Hostname, M2.IPAddress, P2.CourseID
            ) 
        ORDER BY MachineID DESC; 
        """

    res = execute_command(db_connection, cursor, sql_command)
    printRows(res)


# JOCELYN FILE ------------------------------------------------------------------------------------------------------------------------

def insertStudent(db_connection, cursor, argv):  # task 2
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


def insertMachine(db_connection, cursor, argv):  # task 5
    '''
    Insert a new machine.

    argv - MachineID, hostname, IPAddr, status, location
    return: bool
    '''

    sql_command = f"""
        INSERT INTO Machine (MachineID, Hostname, IPAddress, OperationalStatus, Location)
        VALUES ('{argv[2]}', '{argv[3]}', '{argv[4]}', '{argv[5]}', '{argv[6]}')
    """

    result = execute_command(db_connection, cursor, sql_command)
    print(result[0])

def listCourse(db_connection, cursor, argv):  # task 8
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


def activeStudent(db_connection, cursor, argv):  # task 11
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


def main():
    args = sys.argv[1:]
    func = args[0]
    sql_file_path = 'cs122a.sql'

    db_connection = mysql.connector.connect(user = USER, password = PASSWORD, database = DATABASE)
    cursor = db_connection.cursor()

    if func == "import":
        sql_command = f"""
                SELECT
                    (SELECT COUNT(*) FROM User) AS NumberOfUsers,
                    (SELECT COUNT(*) FROM Machine) AS NumberOfMachines,
                    (SELECT COUNT(*) FROM Course) AS NumberOfCourses;
            """

        try:
            # print("Successfully connected to the database")
            # print("Initialization begin")

            for statement in DB_SETUP.split(';'):
                if statement.strip():
                    # print("running: ", statement)
                    cursor.execute(statement)

            folder = args[1]

            cursor.execute(getCsvDataQuery(f"{folder}/users.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/students.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/admins.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/courses.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/projects.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/machines.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/emails.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/use.csv"))
            cursor.execute(getCsvDataQuery(f"{folder}/manage.csv"))
            cursor.execute(sql_command)

            result = cursor.fetchall()
            printRows(result)

            db_connection.commit()
            # print("Initialization end successfully")

        except mysql.connector.Error as error:
            print(f"Failed to execute SQL script: {error}")
            print('False')

    else:
        try:
            function_selected = globals()[sys.argv[1]]
            function_selected(db_connection, cursor, sys.argv)
        except mysql.connector.Error as error:
            print(f"Failed to execute SQL script: {error}")
            print('False')

    if db_connection.is_connected():
        cursor.close()
        db_connection.close()
        # print("MySQL connection is closed")

    return 0


if __name__ == "__main__":
    main()