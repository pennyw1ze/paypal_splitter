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


# Get telegram id from name
def get_id(name):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    c.execute("SELECT * FROM translate WHERE name=?", (name,))
    user = c.fetchone()

    # Close connection
    conn.close()

    # Handle case where user is not found
    if user is None:
        return None
    
    return user[0]

# Remove amount from a user
def process_payment(telegram_id, amount):
    # Connect to database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get user
    user = get_user(telegram_id)
    user = list(user)
    # Remove amount from netflix, if it's negative set it to 0 and proceed in remooving the rest
    # from spotify, if it is negative set it to 0 and proceed in remooving the rest from ripetizioni
    # if it is negative set it to 0
    if user[1] - amount > 0:
        user[1] -= amount
    else:
        amount -= user[1]
        user[1] = 0
        if user[2] - amount > 0:
            user[2] -= amount
        else:
            amount -= user[2]
            user[2] = 0
            if user[3] - amount > 0:
                user[3] -= amount
            else:
                user[3] = 0
    # Update user
    c.execute("UPDATE users SET netflix_amount=?, spotify_amount=?, ripetizioni_amount=? WHERE telegram_id=?", (user[1], user[2], user[3], telegram_id))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()