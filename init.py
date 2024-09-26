import sqlite3
import bcrypt

def sys_init():
    #connect to database
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()

   # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            role TEXT
        )
           ''')        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz (
            qid INTEGER PRIMARY KEY,
            qName TEXT UNIQUE,
            time INTEGER
        )
                   ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            quid INTEGER PRIMARY KEY,
            quiz INTEGER,
            desc TEXT,
            FOREIGN KEY(quiz) REFERENCES artist(qid)
        )
              ''')
    cursor.execute('''     
        CREATE TABLE IF NOT EXISTS answers (
            aid INTEGER PRIMARY KEY,
            quest INTEGER,
            desc TEXT,
            isCorrect INTEGER,
            FOREIGN KEY(quest) REFERENCES artist(quid)
        )
        ''')
        
    

    password1_hash = bcrypt.hashpw(b'secret1', bcrypt.gensalt())
    password2_hash = bcrypt.hashpw(b'secret2', bcrypt.gensalt())
    # Insert some dummy data with hashed passwords
    cursor.execute(
       "INSERT OR IGNORE INTO users (username, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?)",
       ('user1', password1_hash, 'John', 'Doe', 'user'))
    cursor.execute(
       "INSERT OR IGNORE INTO users (username, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?)",
       ('user2', password2_hash, 'Jane', 'Smith', 'admin'))
    cursor.execute(
        "INSERT OR IGNORE INTO quiz (qName, time) VALUES (?,?)",
        ('Quiz1', '10'))
    cursor.execute(
        "INSERT OR IGNORE INTO quiz (qName, time) VALUES (?,?)",
        ('Quiz2', '15'))
    
    
     # Commit the changes
    conn.commit()

   # Close the connection
    conn.close()