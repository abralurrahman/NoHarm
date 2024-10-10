import sqlite3

def create_database():
    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the choices table with IP address and geolocation columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS choices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_choice_1 TEXT NOT NULL,
            patient_choice_2 TEXT NOT NULL,
            patient_choice_3 TEXT NOT NULL,
            ip_address TEXT,  
            city TEXT,        
            region TEXT,      
            country TEXT      
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

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def add_columns_if_not_exist():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the ip_address, city, region, and country columns exist in the choices table
    cursor.execute("PRAGMA table_info(choices);")
    columns = [col[1] for col in cursor.fetchall()]

    if 'ip_address' not in columns:
        cursor.execute('ALTER TABLE choices ADD COLUMN ip_address TEXT')
    
    if 'city' not in columns:
        cursor.execute('ALTER TABLE choices ADD COLUMN city TEXT')
    
    if 'region' not in columns:
        cursor.execute('ALTER TABLE choices ADD COLUMN region TEXT')
    
    if 'country' not in columns:
        cursor.execute('ALTER TABLE choices ADD COLUMN country TEXT')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()  # Create tables if they don't exist
    add_columns_if_not_exist()  # Add columns to existing tables if they don't exist
    print("Database and tables created/updated successfully.")
