import sqlite3
import bcrypt

def createQuiz(qN,tL):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute(
       "INSERT OR IGNORE INTO quiz (qName, time) VALUES (?, ?)",
       (qN,tL))
    s = 'quiz added'
    print("should work")
    conn.commit()
    conn.close()
    return s
