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
def addQuestion(ID,dets):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "INSERT OR IGNORE INTO questions (quiz, desc) VALUES (?, ?)"
    cursor.execute(query,(ID,dets))
    conn.commit()
    conn.close()
    print("added quiz")
    s = "added question"
    return s
def addAnswer(ID,dets,isCor):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "INSERT OR IGNORE INTO answers (quest, desc, isCorrect) VALUES (?, ?, ?)"
    cursor.execute(query,(ID,dets,isCor))
    print("added answer")
    query = "SELECT quiz FROM questions WHERE quid = ?"
    cursor.execute(query,(ID,))
    s = cursor.fetchone()
    x = s[0]
    print(x)
    conn.commit()
    conn.close()
    return x
def deleteQuiz(ID):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "DELETE FROM quiz WHERE qid = ?"
    cursor.execute(query,(ID,))
    s = "quiz deleted"
    conn.commit()
    conn.close()
    return s
def deleteQuestion(ID):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "DELETE FROM questions WHERE quid = ?"
    cursor.execute(query,(ID,))
    s = "question deleted"
    conn.commit()
    conn.close()
    return s
def deleteAnswer(ID):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "DELETE FROM answers WHERE aid = ?"
    cursor.execute(query,(ID,))
    s = "answer deleted"
    conn.commit()
    conn.close()
    return s
def addUser(uN,pas,fN,lN,r):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    byte = pas.encode('utf-8')
    pas2 = bcrypt.hashpw(byte, bcrypt.gensalt())
    cursor.execute(
       "INSERT OR IGNORE INTO users (username, password, first_name, last_name, role) VALUES (?, ?, ?, ?, ?)",
       (uN, pas2, fN, lN, r,))
    s = "ok"
    conn.commit()
    conn.close()
    return s
        
        
    




#user functions