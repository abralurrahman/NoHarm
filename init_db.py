import sqlite3

def create_database():
    """
    Create the `user_responses` table in the database if it doesn't exist.
    """
    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the `user_responses` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            choice1 TEXT,                              -- Choice from Set 1
            choice2 TEXT,                              -- Choice from Set 2
            choice3 TEXT,                              -- Choice from Set 3
            reconsider_choice TEXT,                   -- Reconsidered choice during popup
            popup_decision TEXT,                      -- Tracks if the popup was shown
            save_life_years TEXT,                     -- Procedural rating: Save life years
            advantage_disadvantaged TEXT,             -- Procedural rating: Advantage to disadvantaged
            benefit_future TEXT,                      -- Procedural rating: Benefit others in the future
            first_come TEXT,                          -- Procedural rating: First-come, first-served
            treatment_success TEXT,                   -- Procedural rating: Maximize treatment success
            treatment_effort TEXT,                    -- Procedural rating: Minimize treatment effort
            medication_effect TEXT,                   -- Procedural rating: Maximize medication effect
            random_selection TEXT,                    -- Procedural rating: Random selection
            gender TEXT,                              -- Demographic: Gender
            age INTEGER,                              -- Demographic: Age
            religion TEXT,                            -- Demographic: Religion
            general_health TEXT,                      -- Group preference: General health status
            illness TEXT,                             -- Group preference: Severe illness last year
            children TEXT,                            -- Group preference: Children/planning children
            ip_address TEXT,                          -- User's IP address
            city TEXT,                                -- User's city (geo-location)
            region TEXT,                              -- User's region (geo-location)
            country TEXT,                             -- User's country (geo-location)
            reconsider_opposite_image TEXT,           -- Image suggested by the system during reconsideration
            final_decision TEXT,                      -- Final decision after reconsideration
            choice3_initial_choice TEXT,              -- Initial choice for Set 3
            choice3_final_choice TEXT                 -- Final choice for Set 3 after reconsideration
        )
    ''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def add_columns_if_not_exist():
    """
    Check and add missing columns to the `user_responses` table dynamically.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Retrieve the existing columns in the `user_responses` table
    cursor.execute("PRAGMA table_info(user_responses);")
    user_responses_columns = [col[1] for col in cursor.fetchall()]

    # Define required columns and their SQL types
    required_columns = {
        "choice1": "TEXT",
        "choice2": "TEXT",
        "choice3": "TEXT",
        "reconsider_choice": "TEXT",
        "popup_decision": "TEXT",
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
        "general_health": "TEXT",
        "illness": "TEXT",
        "children": "TEXT",
        "ip_address": "TEXT",
        "city": "TEXT",
        "region": "TEXT",
        "country": "TEXT",
        "reconsider_opposite_image": "TEXT",
        "final_decision": "TEXT",
        "choice3_initial_choice": "TEXT",
        "choice3_final_choice": "TEXT"
    }

    # Add missing columns to the table
    for column, column_type in required_columns.items():
        if column not in user_responses_columns:
            print(f"Adding missing column: {column}")
            cursor.execute(f'ALTER TABLE user_responses ADD COLUMN "{column}" {column_type}')

    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("Checking and updating the database schema...")
    create_database()  # Create tables if they don't exist
    add_columns_if_not_exist()  # Add missing columns to existing tables
    print("Database and tables created/updated successfully.")
