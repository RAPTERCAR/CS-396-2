import sqlite3
import bcrypt
#admin functions
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
def viewAllQuiz():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM quiz'
    )
    out = cursor.fetchall()
    s = "ID  Name  TimeLimit<br>"
    for all in out:
        s = s + str(all) + "<br>"
    conn.close()
    return s
def viewSpecQuiz(ID):
    #conn = sqlite3.connect('quiz.db')
    #cursor = conn.cursor()
    query = "SELECT * FROM quiz WHERE id = ?"
    #cursor.execute(query,(ID,))
    




#user functions