import sqlite3
import bcrypt


class User:

   def __init__(self, user_id, username, password_hash, first_name, last_name,
                role):
      self.id = user_id
      self.username = username
      self.password_hash = password_hash
      self.first_name = first_name
      self.last_name = last_name
      self.role = role

   def to_json(self):
      user_json = {
          "id": self.id,
          "username": self.username,
          "first_name": self.first_name,
          "last_name": self.last_name,
          "role": self.role
      }
      return user_json
   
      # Function to hash the password
def hash_password(password):
   return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


# Function to verify the password
def verify_password(password, hashed_password):
   return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


# Simulating a login functionality with hashed passwords
def login(username, password):
   # Connect to an SQLite database
   conn = sqlite3.connect('quiz.db')
   cursor = conn.cursor()

   query = "SELECT * FROM users WHERE username = ?"
   cursor.execute(query, (username,))  # Passing user input as parameters
   user_data = cursor.fetchone()

   if user_data:
      stored_password_hash = user_data[2]
      if verify_password(password, stored_password_hash):
         user = User(user_data[0], user_data[1], user_data[2], user_data[3],
                     user_data[4], user_data[5])
      else:
         user = None
   else:
      user = None

   # Close the connection
   conn.close()

   return user