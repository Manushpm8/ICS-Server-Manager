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