import sys

def insertStudent(argv): #task 2
    sql_command = """
        INSERT INTO User (UCINetID, email, First, Middle, Last)
        VALUES (argv[2], argv[3], argv[4], argv[5], argv[6])

        INSERT INTO Student (UCINetID)
        VALUES (argv[2])
    """

    #return bool??

def insertMachine(argv): #task 5
    sql_command = """
        INSERT INTO Machine (MachineID, hostname, IPAddr, status)
        VALUES (argv[2], argv[3], argv[4], argv[5])

    """

    #return bool??

def listCourse(argv): # task 8
    sql_command = """
        SELECT DISTINCT
            c.CourseID, c.*
            
        FROM
            Student s, StudentUse u, Project p, Course c
            
        WHERE
            s.UCINetID = argv[2] and
            s.UCINetID = u.UCINetID and
            u.ProjectID = p.ProjectID and
            p.CourseID = c.CourseID
            
        ORDER BY
            c.CourseID ASC
        
    """

def activeStudent(argv): # task 11
    sql_command = """
        SELECT
            s.UCINetID, s.*

        FROM Student s, StudentUse u, Machine m
        
        WHERE
            s.UCINetID = u.UCINetID and 
            u.MachineID = argv[2] and
            u.MachineID = m.MachineID and
            m.OperationalStatus = 'active' and
            u.StartDate <= argv[4] and u.EndDate >= argv[5]
            
        GROUP BY
            s.UCINetID
            
        HAVING
            COUNT(*) > argv[3]
            
        ORDER BY
            s.UCINetID ASC 
    """

if __name__ == "__main__":
    #argv[0] = project.py
    #argv[1] = <function name>

    if len(sys.argv) >= 2:
        function_name = globals()[sys.argv[1]]
        function_name(sys.argv)
