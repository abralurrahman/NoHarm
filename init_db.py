import sqlite3

def create_database():
    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the user_responses table for consolidated responses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            choice1 TEXT,
            choice2 TEXT,
            choice3 TEXT,
            reconsider_choice TEXT,
            save_life_years TEXT,
            advantage_disadvantaged TEXT,
            benefit_future TEXT,
            first_come TEXT,
            treatment_success TEXT,
            treatment_effort TEXT,
            medication_effect TEXT,
            random_selection TEXT,
            gender TEXT,
            age INTEGER,
            religion TEXT,
            general_health TEXT,
            illness TEXT,
            children TEXT,
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

    # Check columns in the user_responses table and add missing ones
    cursor.execute("PRAGMA table_info(user_responses);")
    user_responses_columns = [col[1] for col in cursor.fetchall()]

    # Define required columns and their SQL types
    required_columns = {
        "choice1": "TEXT",
        "choice2": "TEXT",
        "choice3": "TEXT",
        "reconsider_choice": "TEXT",
        "save_life_years": "TEXT",
        "advantage_disadvantaged": "TEXT",
        "benefit_future": "TEXT",
        "first_come": "TEXT",
        "treatment_success": "TEXT",
        "treatment_effort": "TEXT",
        "medication_effect": "TEXT",
        "random_selection": "TEXT",
        "gender": "TEXT",
        "age": "INTEGER",
        "religion": "TEXT",
        "general_health": "TEXT",  # Fixed typo (removed extra space)
        "illness": "TEXT",
        "children": "TEXT",
        "ip_address": "TEXT",
        "city": "TEXT",
        "region": "TEXT",
        "country": "TEXT"
    }

    # Add missing columns
    for column, column_type in required_columns.items():
        if column not in user_responses_columns:
            cursor.execute(f'ALTER TABLE user_responses ADD COLUMN {column} {column_type}')

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()  # Create tables if they don't exist
    add_columns_if_not_exist()  # Add columns to existing tables if they don't exist
    print("Database and tables created/updated successfully.")
