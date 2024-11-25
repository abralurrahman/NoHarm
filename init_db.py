import sqlite3

def create_database():
    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the choices table for individual page-based choices
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page INTEGER NOT NULL,
            choice TEXT NOT NULL
        )
    ''')

    # Create the procedural_ratings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procedural_ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            save_life_years TEXT,
            advantage_disadvantaged TEXT,
            benefit_future TEXT,
            first_come TEXT,
            treatment_success TEXT,
            treatment_effort TEXT,
            medication_effect TEXT,
            random_selection TEXT
        )
    ''')

    # Create the demography table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demography (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            age INTEGER,
            religion TEXT,
            other_religion TEXT
        )
    ''')

    # Create the group_preferences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS group_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            general_health TEXT,
            illness TEXT,
            children TEXT
        )
    ''')

    # Create the geolocation table to store user IP and location data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS geolocation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            city TEXT,
            region TEXT,
            country TEXT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def add_columns_if_not_exist():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the `geolocation` table exists
    cursor.execute("PRAGMA table_info(geolocation);")
    geolocation_columns = [col[1] for col in cursor.fetchall()]

    if not geolocation_columns:
        cursor.execute('''
            CREATE TABLE geolocation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                city TEXT,
                region TEXT,
                country TEXT
            )
        ''')

    # Check if the choices table has the page column
    cursor.execute("PRAGMA table_info(choices);")
    choices_columns = [col[1] for col in cursor.fetchall()]

    if 'page' not in choices_columns:
        cursor.execute('ALTER TABLE choices ADD COLUMN page INTEGER')

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()  # Create tables if they don't exist
    add_columns_if_not_exist()  # Add columns to existing tables if they don't exist
    print("Database and tables created/updated successfully.")
