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
            CREATE TABLE IF NOT EXISTS release_year (
            release_id INTEGER PRIMARY KEY,
            release TEXT
        );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS country (
                country_id INTEGER PRIMARY KEY,
                country TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watched (
                watched_id INTEGER PRIMARY KEY,
                watched TEXT
            );
        ''')
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

def show_all (cursor): #this shows everything the database has
    try:
        cursor.execute("""
            SELECT drama_name, release, country, episode, watched, rating
                FROM drama
                LEFT JOIN
                release_year ON drama.release_id = release_year.release_id
                LEFT JOIN
                country ON drama.country_id = country.country_id
                LEFT JOIN
                watched ON drama.watched_id = watched.watched_id
                ORDER BY release ASC
        """)
        rows = cursor.fetchall()
        if not rows:
            eg.msgbox("No dramas found in the database.", "Drama List")
            return

        col_widths = [40, 8, 15, 10, 20, 8]  
        headers = ["Drama", "Rating", "Country", "Episodes", "Watched", "Release"]

        header_row = "".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        line = "-" * sum(col_widths)

        formatted_rows = []
        for row in rows:
            formatted_row = "".join(str(col)[:col_widths[i]-1].ljust(col_widths[i]) for i, col in enumerate(row))
            formatted_rows.append(formatted_row)

        output = f"{header_row}\n{line}\n" + "\n".join(formatted_rows)

        eg.codebox(f"All the Dramas {show_all}", "All the Dramas", output)

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def show_country(cursor, country_choice):
    try:
        cursor.execute("""
            SELECT drama_name, release, country, episode
            FROM drama
            LEFT JOIN release_year ON drama.release_id = release_year.release_id
            LEFT JOIN country ON drama.country_id = country.country_id
            WHERE country = ?
            ORDER BY release ASC
        """, (country_choice,))
        rows = cursor.fetchall()

        if not rows:
            eg.msgbox(f"No dramas found from {country_choice}.", "Country Results")
            return

        col_widths = [45, 8, 15, 10]  
        headers = ["Drama", "Release", "Country", "Episodes"]

        header_row = "".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        line = "-" * sum(col_widths)

        formatted_rows = []
        for row in rows:
            formatted_row = "".join(str(col)[:col_widths[i]-1].ljust(col_widths[i]) for i, col in enumerate(row))
            formatted_rows.append(formatted_row)

        output = f"{header_row}\n{line}\n" + "\n".join(formatted_rows)

        eg.codebox(f"Dramas that are from {country_choice}", "Country", output)

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def show_year(cursor, year_choice):
    try:
        cursor.execute("""
            SELECT drama_name, release, country, episode, watched
            FROM drama
            LEFT JOIN
            release_year ON drama.release_id = release_year.release_id
            LEFT JOIN
            country ON drama.country_id = country.country_id
            LEFT JOIN
            watched ON drama.watched_id = watched.watched_id
            WHERE release = ?
        """, (year_choice,))
        rows = cursor.fetchall()
        if not rows:
            eg.msgbox(f"No dramas found from year {year_choice}.", "Year Results")
            return
        col_widths = [35, 8, 20, 8, 10]  
        headers = ["Drama", "Release", "Country", "Episodes", "Watched"]

        header_row = "".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        line = "-" * sum(col_widths)

        formatted_rows = []
        for row in rows:
            formatted_row = "".join(str(col)[:col_widths[i]-1].ljust(col_widths[i]) for i, col in enumerate(row))
            formatted_rows.append(formatted_row)

        output = f"{header_row}\n{line}\n" + "\n".join(formatted_rows)

        eg.codebox(f"Dramas that are from {year_choice}", "Years", output)

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def show_watched(cursor, watched_choice):
    try:
        cursor.execute("""
            SELECT drama_name, release, country, episode, watched
            FROM drama
            LEFT JOIN
            release_year ON drama.release_id = release_year.release_id
            LEFT JOIN
            country ON drama.country_id = country.country_id
            LEFT JOIN
            watched ON drama.watched_id = watched.watched_id
            WHERE watched = ?
            ORDER BY release ASC
        """, (watched_choice,))
        rows = cursor.fetchall()
        if not rows:
            eg.msgbox(f"No dramas found with status {watched_choice}.", "Status Results")
            return
        col_widths = [35, 8, 20, 10, 14]  
        headers = ["Drama", "Rating", "Country", "Episodes", "Watched"]

        header_row = "".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        line = "-" * sum(col_widths)

        formatted_rows = []
        for row in rows:
            formatted_row = "".join(str(col)[:col_widths[i]-1].ljust(col_widths[i]) for i, col in enumerate(row))
            formatted_rows.append(formatted_row)

        output = f"{header_row}\n{line}\n" + "\n".join(formatted_rows)

        eg.codebox(f"Dramas you {watched_choice}", "Watched Status Results", output)
    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def show_rating(cursor, rating_choice):
    try:
        cursor.execute("""
            SELECT drama_name, rating, country, episode, watched, release
            FROM drama
            LEFT JOIN
            release_year ON drama.release_id = release_year.release_id
            LEFT JOIN
            country ON drama.country_id = country.country_id
            LEFT JOIN
            watched ON drama.watched_id = watched.watched_id
            WHERE rating = ?
        """, (rating_choice,))
        rows = cursor.fetchall()
        if not rows:
            eg.msgbox(f"No dramas found with rating {rating_choice}.", "Rating Results")
            return
        col_widths = [40, 8, 15, 10, 20, 8]  
        headers = ["Drama", "Rating", "Country", "Episodes", "Watched", "Release"]

        header_row = "".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        line = "-" * sum(col_widths)

        formatted_rows = []
        for row in rows:
            formatted_row = "".join(str(col)[:col_widths[i]-1].ljust(col_widths[i]) for i, col in enumerate(row))
            formatted_rows.append(formatted_row)

        output = f"{header_row}\n{line}\n" + "\n".join(formatted_rows)

        eg.codebox(f"Dramas with rating {rating_choice}", "Rating Results", output)

    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to retrieve dramas: {e}", title="Database Error")

def add_drama(cursor, conn):
    drama_name = eg.enterbox("Enter drama name:", "Add Drama")
    if not drama_name:
        return

    release_years = [str(y) for y in range(2010, 2030)]
    release = eg.choicebox("Select release year:", "Add Drama", choices=release_years)
    if not release:
        return

    countries = ["China", "South Korea", "Philippines", "Thailand","Japan"]
    country = eg.choicebox("Select country:", "Add Drama", choices=countries)
    if not country:
        return

    episode = eg.integerbox("Enter number of episodes:", "Add Drama", lowerbound=0, upperbound=10000 )
    if episode is None:
        return

    watched_statuses = ["Watched", "Plan on Watching", "On-Hold", "Dropped"]
    watched = eg.choicebox("Select watched status:", "Add Drama", choices=watched_statuses)
    if not watched:
        return

    rating = eg.integerbox("Enter rating (1-10):", "Add Drama", lowerbound=1, upperbound=10)
    if rating is None:
        return

    cursor.execute("SELECT release_id FROM release_year WHERE release = ?", (release,))
    release_id = cursor.fetchone()
    if not release_id:
        eg.msgbox("Release year not found in database.", "Error")
        return

    cursor.execute("SELECT country_id FROM country WHERE country = ?", (country,))
    country_id = cursor.fetchone()
    if not country_id:
        eg.msgbox("Country not found in database.", "Error")
        return

    cursor.execute("SELECT watched_id FROM watched WHERE watched = ?", (watched,))
    watched_id = cursor.fetchone()
    if not watched_id:
        eg.msgbox("Watched status not found in database.", "Error")
        return

    try:
        cursor.execute("""
            INSERT INTO drama (drama_name, release_id, country_id, episode, watched_id, rating)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (drama_name, release_id[0], country_id[0], episode, watched_id[0], rating))
        conn.commit()
        eg.msgbox("Drama added successfully!", "Success")
    except sqlite3.Error as e:
        eg.exceptionbox(msg=f"Failed to add drama: {e}", title="Database Error")

if __name__ == "__main__":
    conn , cursor = setup_database()

    if not conn:
        exit()

    while True:
        choice = eg.buttonbox(
            "Welcome to the Drama Database what would you like to do?",
            "Main Menu",
            choices=["Show all drama","Country","Year","Watched Status","Rating","Add Drama","Exit"]
        )
        if choice == "Show all drama":
            show_all(cursor)
        elif choice == "Add Drama":
            add_drama(cursor, conn)
        elif choice == "Country":
            country_choice = eg.buttonbox(
                "Pick a country to see:",
                "Country",
                choices=["China" , "South Korea" , "Philippines" , "Thailand", "Japan"]
            )
            if country_choice:
                show_country(cursor, country_choice)
        elif choice == "Year":
            year_choice = eg.choicebox(
                "Choose a year to see:",
                "Year",
                choices=[str(i) for i in range(2010, 2030)]
            )
            if year_choice:
                show_year(cursor, year_choice)
        elif choice == "Watched Status":
            watched_choice = eg.buttonbox(
                "Choose a status to see:",
                "Watched Status",
                choices=["Watched","Plan on Watching" , "On-Hold" , "Dropped"]
            )
            if watched_choice:
                show_watched(cursor, watched_choice)
        elif choice == "Rating":
            rating_choice = eg.buttonbox(
                "Pick a rating",
                "Rating",
                choices=[str(i) for i in range(1, 11)]
            )
            if rating_choice:
                show_rating(cursor, int(rating_choice))
        elif choice == "Exit":
            eg.msgbox("Thank you for using Drama Database")
            break