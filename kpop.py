# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'kpop.db'

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  

TABLES = (" idol "
           "LEFT JOIN ethnicitys ON idol.ethnicity_id = ethnicitys.ethnicity_id "
           "LEFT JOIN groups ON idol.group_id = groups.group_id "
           "LEFT JOIN ages ON idol.age_id = ages.age_id ")

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
    menu_option = input('Welcome to the Kpop database \n\n'
                        'This menu contains information about Kpop:\n'
                        '   - Groups\n'
                        "   - Idol's stage name\n"
                        "   - Idol's real name\n"
                        "   - Idol's ages\n"
                        "   - Idol's Birthdays\n"
                        "   - Idol's Ethnicity\n"
                        "   - Idol's height\n"
                        "   - Idol's instagram\n\n"
                        'Please enter a letter that is from A -I to navigate throught the menu.\n'
                        "Please type 'DONE' to exit the database\n"
                        'A: All Information\n'
                        'B: Kpop groups members\n'
                        'C: Idols Height\n'
                        'D: Ethinicty\n'
                        'E: Idols Age\n'
                        'F: Top 10 oldest\n'
                        'G: Top 10 tallest\n'
                        'H: Top 10 Youngest\n'
                        "I: All the lee's in kpop\n"
                        'DONE: Exit\n\n'
                        'Where would you like to go? ')
    menu_option = menu_option.upper()
    if menu_option == 'A':
        print_query('All information')
    elif menu_option == 'B':
        print('Here are the Kpop groups:\n'
              ' - nct 127\n'
              ' - nct dream\n'
              ' - wayv\n'
              ' - ateez\n'
              ' - enhypen\n'
              ' - seventeen\n'
              ' - straykids\n')
        kpop_group = input('Which kpop group would you like to see: ')
        print_parameter_query("kpop_group, real_name, stage_name, age","kpop_group = ? ORDER BY age DESC", kpop_group.lower())
    elif menu_option == 'C':
        print('The height available are 165 - 187')
        height = input('What height  would you like to see: ')
        print_parameter_query("kpop_group, real_name, stage_name, age, height","height = ? ORDER BY age DESC", height)
    elif menu_option == 'D':
        print('Here are the Ethnicitys of the Kpop Idols:\n'
              ' - South Korea\n'
              ' - China\n'
              ' - USA\n'
              ' - Japan\n'
              ' - Australia\n'
              ' - Canada\n'
              ' - Thailand\n')
        ethnicity = input('Which ethnicity would you like to see? ')
        print_parameter_query("kpop_group, real_name, stage_name, age, ethnicity","ethnicity = ? ORDER BY age DESC", ethnicity.lower())
    elif menu_option == 'E':
        print('The ages available are 19 - 29')
        age = input('What age would you like to see: ')
        print_parameter_query("kpop_group, real_name, stage_name, age","age = ? ORDER BY age DESC", age)       
    elif menu_option == 'F':
        print_query('Top 10 oldest')
    elif menu_option == 'G':
        print_query("Top 10 tallest")
    elif menu_option == 'H':
        print_query('Top 10 Youngest')
    elif menu_option == 'I':
        print_query("All the lee in kpop")
    elif menu_option == 'DONE':
        print('Thanks for using me! \nPlease come again!!!')
