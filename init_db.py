import sqlite3

def create_database():
    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the survey table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS survey (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consent TEXT,
            patient_choice TEXT,
            procedure_rating TEXT,
            age INTEGER,
            gender TEXT,
            religion TEXT
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database and table created successfully.")
