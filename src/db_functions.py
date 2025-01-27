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
    
    c.execute('''CREATE TABLE IF NOT EXISTS translate(
                id INTEGER PRIMARY KEY,
                name TEXT
              )''')
    c.execute('''CREATE TABLE IF NOT EXISTS username(
                telegram_id INTEGER PRIMARY KEY,
                username TEXT
              )''')

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Check if a user is in the database
def check_user_table(telegram_id):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if user is in the database
    c.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
    user = c.fetchone()

    # Close connection
    conn.close()

    return user

# Add a user to the database
def add_user_table(telegram_id):
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

# Get all names
def get_all_translate():
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get all users
    c.execute("SELECT * FROM translate")
    translate = c.fetchall()

    # Close connection
    conn.close()

    return translate

# Add a name to the database
def add_translate(id, name):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Add user ( or replace if already exists )
    c.execute("INSERT OR REPLACE INTO translate VALUES (?, ?)", (id, name))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Add a username to the database
def add_username(id, username):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Add user ( or replace if already exists )
    c.execute("INSERT OR REPLACE INTO username VALUES (?, ?)", (id, username))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Check if a name is in the database
def check_translate_name(name):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check if user is in the database
    c.execute("SELECT * FROM translate WHERE name=?", (name,))
    user = c.fetchone()

    # Close connection
    conn.close()
    
    return user

# Add netflix amount
def add_netflix_amount(telegram_id, amount):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    user = get_user(telegram_id)

    # Update user
    c.execute("UPDATE users SET netflix_amount=? WHERE telegram_id=?", (amount, telegram_id))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Add spotify amount
def add_spotify_amount(telegram_id, amount):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    user = get_user(telegram_id)

    # Update user
    c.execute("UPDATE users SET spotify_amount=? WHERE telegram_id=?", (amount, telegram_id))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Add ripetizioni amount
def add_ripetizioni_amount(telegram_id, amount):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    user = get_user(telegram_id)

    # Update user
    c.execute("UPDATE users SET ripetizioni_amount=? WHERE telegram_id=?", (amount, telegram_id))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()