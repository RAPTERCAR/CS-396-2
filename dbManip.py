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
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "SELECT * FROM quiz WHERE qid = ?"
    cursor.execute(query,(ID,))
    out = cursor.fetchall()
    s = "quiz: " + str(out) + "<br>"
    query = "SELECT * FROM questions WHERE quiz = ?"
    cursor.execute(query,(ID,))
    out = cursor.fetchall()
    query = "SELECT * FROM answers WHERE quest = ?"
    for all in out:
        s = s + "Q:" + str(all) + "<br>"
        quest = all[0]
        cursor.execute(query,(quest,))
        outty = cursor.fetchall()
        for any in outty:
            s = s + "A:" + str(any) + "<br>"
    conn.close()
    return s
        
        
        
    




#user functions