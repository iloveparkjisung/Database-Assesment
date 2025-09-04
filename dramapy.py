# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate
import easygui as eg

# This is the filename of the database to be used
DB_NAME = 'dramadatabase.db'

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect('dramadatabase.db')
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
    db = sqlite3.connect("dramadatabase.db")
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
    menu_option = input('\nWelcome to my drama database \n\n'
                        'This menu contains information about drama:\n'
                        '   - Names of dramas\n'
                        '   - Dramas from countries [South Korea, Philippines, Thailand, China]\n'
                        '   - Drama Ratings\n'
                        '   - Drama released 2013 - upcoming\n'
                        '   - Status of Drama\n\n'
                        'Please enter a letter that is from A to navigate through the menu.\n'
                        "Please type 'Exit' to exit the database\n"
                        'A  -   View all information\n'
                        'B  -   Search for dramas from countries available\n'
                        'C  -   Search for years certain dramas were aired\n'
                        'D  -   Print out ratings below 5\n'
                        'E  -   Print out ratings 5 and above\n'
                        'F  -   Top 10 South Korean Drama\n'
                        'G  -   Top 10 Chinese Drama\n'
                        'H  -   Top 10 Thailand Drama\n'
                        'I  -   Top 10 Philippines Drama\n'
                        'Done   -   Bye Bye\n\n'
                        "Where would you like to go? ")
    menu_option = menu_option.upper()
    if menu_option == 'A':
        print_query('All information')
    elif menu_option == 'B':
        print("Here are the available countries to search from:\n"
            "   -   China\n"
            "   -   South Korea\n"
            "   -   Philippines\n"
            "   -   Thailand\n")
        while True:
            drama_country = input('Which country would you like to see? ')
            drama_country = drama_country.capitalize()
            db = sqlite3.connect(DB_NAME)
            cursor = db.cursor()
            cursor.execute("SELECT 1 FROM country WHERE UPPER(country) = ?", (drama_country.upper(),))
            exists = cursor.fetchone()
            db.close()
            if exists:
                print_parameter_query("drama_name, release, country, episode, watched, rating", "country = ? ORDER BY release DESC", drama_country)
                break
            else:
                print("Sorry unable to find country. Please check for the spelling")
    elif menu_option == 'C':
        print("Here are the available countries to search from:\n"
            "   -   0 [upcoming] , 2010 to 2025\n")
        while True:
            drama_year = input('Which year would you like to see? ')
            db = sqlite3.connect(DB_NAME)
            cursor = db.cursor()
            cursor.execute("SELECT 1 FROM release_year WHERE (release) = ?", (drama_year,))
            exists = cursor.fetchone()
            db.close()
            if exists:
                print_parameter_query("drama_name, release, country, episode, watched, rating", "release = ? ORDER BY release DESC", drama_year)
                break
            else:
                print("Sorry unable to find year. Please check if the year is right.")
    elif menu_option == 'D':
        print_query("Rating below 5")
    elif menu_option == 'E':
        print_query("Rating 5 and over")
    elif menu_option == 'F':
        print_query("Top 10 South Korean Drama")
    elif menu_option == 'G':
        print_query("Top 10 Chinese Drama")
    elif menu_option == 'H':
        print_query("Top 10 Thailand Drama")
    elif menu_option == 'I':
        print_query("Top 10 Philippines Drama")
    elif menu_option == 'DONE':
        print('Thanks for using me! \nPlease come again!!!')
    else:
        print("\nPlease try again!")
