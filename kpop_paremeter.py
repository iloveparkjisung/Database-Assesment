# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate

# This is the filename of the database to be used
DB_NAME = 'kpop.db'
# This is the SQL to connect to all the tables in the database
TABLES = (" idol "
           "LEFT JOIN ethnicitys ON idol.ethnicity_id = ethnicitys.ethnicity_id "
           "LEFT JOIN groups ON idol.group_id = groups.group_id "
           "LEFT JOIN ages ON idol.age_id = ages.age_id ")

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    print(tabulate(results,fields.split(",")))
    db.close()  

height = input('What height  would you like to see: ')
print_parameter_query("kpop_group, real_name, stage_name, age, height","height = ? ORDER BY age DESC", height)

age = input('What age would you like to see: ')
print_parameter_query("kpop_group, real_name, stage_name, age","age = ? ORDER BY age DESC", age)

kpop_group = input('Which kpop group would you like to see: ')
print_parameter_query("kpop_group, real_name, stage_name, age","kpop_group = ? ORDER BY age DESC", kpop_group)

ethnicity = input('Which ethnicity would you like to see? ')
print_parameter_query("kpop_group, real_name, stage_name, age, ethnicity","ethnicity = ? ORDER BY age DESC", ethnicity)
    