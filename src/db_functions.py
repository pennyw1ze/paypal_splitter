import sqlite3

# Build the database
def build_database():
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS users( 
                telegram_id INTEGER PRIMARY KEY,
                netflix_amount REAL DEFAULT 0,
                spotify_amount REAL DEFAULT 0,
                ripetizioni_amount REAL DEFAULT 0
              )''')

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Add a user to the database
def add_user(telegram_id):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Add user ( or replace if already exists )
    c.execute("INSERT OR REPLACE INTO users VALUES (?, 0, 0, 0)", (telegram_id,))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Get user data
def get_user(telegram_id):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    c.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
    user = c.fetchone()

    # Close connection
    conn.close()

    return user

# Update user data
def update_user(telegram_id, netflix_amount, spotify_amount, ripetizioni_amount):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Update user
    c.execute("UPDATE users SET netflix_amount=?, spotify_amount=?, ripetizioni_amount=? WHERE telegram_id=?", (netflix_amount, spotify_amount, ripetizioni_amount, telegram_id))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Get all users
def get_all_users():
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get all users
    c.execute("SELECT * FROM users")
    users = c.fetchall()

    # Close connection
    conn.close()

    return users

