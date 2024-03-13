# Homework 4, Part 1

This python project helps you set up your local environment to run and test your queries.

## Project Dependencies
- Python Version: 3.9
- Required packages: in the requirements.txt
- MySQL: make sure you have a MySQL server up and running on your machine

## Get Started

### 1. Configure your local development environment
The most recommended way is to configure everying using a Python IDE. 

PyCharm might be the easiest one to kick off. 
First, download PyCharm from the JetBrains website. 
Then refer to this link: https://www.jetbrains.com/help/pycharm/managing-dependencies.html to install the required packages for this project in the file requirements.txt

Of course other ways of running this project are welcomed, as long as you manage to run the whole thing up and finish the assignment.

### 2. Load the DB

First you need to substitute the information in `constants.py` in order to connect to your local MySQL successfully.

Then you can run `run_initialization.py` to load the data into MySQL.

### 3. Write queries

Edit `queries.py` to write your query. Several placeholder variables have been created, you can just fill in the corresponding queries for different questions.

### 4. Run the test

To test your queries, we prepare the tests for each query, in `tests/test_simple_queries.py`. To run these tests, simply run `run_tests.py`.

