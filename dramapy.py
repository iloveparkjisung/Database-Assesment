# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate
import easygui as eg

# This is the filename of the database to be used
DB_NAME = 'dramadatabase.db'

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  

TABLES = (" drama "
           "LEFT JOIN country ON drama.country_id = country.country_id "
           "LEFT JOIN release_year ON drama.release_id = release_year.release_id "
           "LEFT JOIN watched ON drama.watched_id = watched.watched_id ")

def print_query(view_name:str):
    ''' Prints the specified view from the database in a table '''
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    print(tabulate(results,headings))
    db.close() 

menu_option = ''
while menu_option != 'DONE':
    menu_option = input('Welcome to my drama database \n\n'
                        'This menu contains information about drama:\n'
                        '   - Names of dramas\n'
                        '   - Dramas from countries [South Korea, Philippines, Thailand, China]\n'
                        '   - Drama Ratings\n'
                        '   - Drama released 2013 - upcoming\n'
                        '   - Status of Drama\n\n'
                        'Please enter a letter that is from A to navigate through the menu.\n'
                        "Please type 'Exit' to exit the database\n"
                        'A  -   Search for dramas from countries available\n'
                        'EXIT   -   Bye Bye\n\n'
                        "Where would you like to go? "
                        )

menu_option = menu_option.upper()
if menu_option == 'A':
    print("Here are the available countries to search from:\n"
        "   -   China\n"
        "   -   South Korea\n"
        "   -   Philippines\n"
        "   -   Thailand\n")
    drama_country = input('Which country would you like to see?')
    print_parameter_query("drama_name, release, country, episode, watched, rating", "country = ? ORDER BY release DESC", country)

