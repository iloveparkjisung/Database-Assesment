# Import the libraries to connect to the database and present the information in tables
import sqlite3
from tabulate import tabulate
import easygui as eg

# This is the filename of the database to be used
DB_NAME = 'dramadatabase.db'
def setup_database():
    """
    Connects to the SQLite database and ensures the contacts table exists.
    If the database file doesn't exist, SQLite will create it.
    This function returns the connection and cursor objects for later use.
    """
    try:
        # Connect to the database file named 'contacts.db'.
        # This will create the file if it doesn't exist.
        conn = sqlite3.connect('dramadatabase.db')
        
        # Create a cursor object to execute SQL commands.
        cursor = conn.cursor()
        
        # This prevents an error if you run the script multiple times.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS drama (
                drama_name TEXT PRIMARY KEY,
                release_id INTEGER,
                country_id INTEGER,
                episode INTEGER,
                watched_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (release_id) REFERENCES release_year (release_id),
                FOREIGN KEY (country_id) REFERENCES country (country_id),
                FOREIGN KEY (watched_id) REFERENCES watched (watched_id) 
            );
        ''')
         
        # Commit the changes to save the table creation to the database file.
        conn.commit()
        
        # Return the connection and cursor for use in other functions.
        return conn, cursor
        
    except sqlite3.Error as e:
        # Use EasyGui to show an error message if the database connection fails.
        eg.exceptionbox(msg=f"A database error occurred: {e}", title="Database Error")
        # Return None to signal that a fatal error occurred.
        return None, None

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

def show_all (cursor):
    try:
        cursor.execute("SELECT drama_name, release, country, episode, watched, rating FROM drama")
        rows = cursor.fetchall()

        if not rows:
            eg.msgbox("No dramas found in the database.", "Drama List")
            return

        drama_list = ""
        for row in rows:
            drama_list += str(row) + "\n"
        eg.msgbox(drama_list, "Drama List")

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")


def show_country (cursor):
    try:
        cursor.execute("SELECT drama_name, release, country, episode, watched, rating FROM drama")
        rows = cursor.fetchall()

        if country_choice == "China":
            
            return
    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def show_year (cursor):
    try:
        cursor.execute("SELECT drama_name, release, country, episode, watched, rating FROM drama")
        rows = cursor.fetchall()

        if country_choice == "China":
            
            return
    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

if __name__ == "__main__":
    conn , cursor = setup_database()

    if not conn:
        exit()

    while True:
        choice = eg.buttonbox(
            "Welcome to the Drama Database what would you like to do?",
            "Main Menu",
            choices=["Show all drama","Country","Year","Watched Status","Rating","Exit"]
        )

        if choice == "Show all drama":
            show_all(cursor)
        if choice == "Country":
            country_choice = eg.buttonbox(
                "Pick a country to see:",
                "Country",
                choices=["China" , "South Korea" , "Philippines" , "Thailand"]
            )
        if choice == "Year":
            year_choice = eg.choicebox(
                "Choose a year to see:",
                "Year",
                choices=["0","2010","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"]
            )
        if choice == "Watched Status":
            status_choice = eg.buttonbox(
                "Choose a status to see:",
                "Watched Status",
                choices=["Completed","Plan on watching" , "On-hold" , "Dropped"]
            )
        if choice == "Rating":
            rating_choice = eg.buttonbox(
                "Pick a rating",
                "Rating",
                choices=[]
            )
        elif choice == "Exit":
            eg.msgbox("Thank you for using Drama Database") 
            break #using break quits the code
