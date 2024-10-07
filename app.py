from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from init import sys_init
from uLogin import login, User
from dbManip import createQuiz, viewAllQuiz, viewSpecQuiz, addQuestion, addAnswer,deleteAnswer,deleteQuestion, deleteQuiz,addUser
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with app.app_context():
    sys_init()

@app.route('/')
def index():
    if request.args:
        return render_template('index.html', messages =request.args['messages'])
    else:
        return render_template('index.html', messages = '')
    
@app.route('/ajaxkeyvalue', methods=['POST'])
def ajax():
    data = request.json  # Assuming the AJAX request sends JSON data
    print(data)
    # Process the data
    username = data['username']
    password = data['password']

    print(username)
    print(password)


    user = login(username, password)
    if not user:
        response_data ={'status' : 'fail'}
    else:
        session['logged_in'] = True
        session['username'] = username
        session['user'] = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role,
        }
        response_data = {'status' :'ok', 'user': user.to_json()}


    return jsonify(response_data)

@app.route('/home')
def profile():

    user_data = session.get('user')

    if user_data:
        # Reconstruct the user object
        user = User(user_id=user_data['id'], username=user_data['username'],
                password_hash='', first_name=user_data['first_name'],
                last_name=user_data['last_name'], role=user_data['role'])

        print(user.role)
        if(user.role == "user"):
            return render_template('home.html', user_info=user)
        
        else:
            return render_template('admin.html', user_info=user)
        
    else:
        return redirect('/?messages=Please login again!')
    
@app.route('/data', methods=['POST','GET'])
def accessData():
    data = request.json #get data from libScript.js or patScript.js
    if data:
        #admin functions
        #create a quiz
        if (data['request'] == 'createQuiz'):
            qN = data['qName']
            tL = data['tLimit']
            print('test')
            temp = createQuiz(qN,tL)
            response = {'output' : temp}
            return jsonify(response)
        #view all quizzes
        if (data['request'] == 'viewAll'):
            print("test2")
            temp = viewAllQuiz()
            response = {'output' : temp}
            return jsonify(response)
        #view quiz details
        if (data['request'] == 'viewSpec'):
            print("test3")
            qid = data['ID']
            temp = viewSpecQuiz(qid)
            response = {'output' : temp}
            return jsonify(response)
        #add a question
        if (data['request'] == 'addQue'):
            print("test4")
            qid = data['ID']
            dets = data['Det']
            temp = addQuestion(qid,dets)
            temp2 = viewSpecQuiz(qid)
            response = {'output': temp, 'display': temp2}
            return jsonify(response)
        #add an answer
        if (data['request'] == 'addAns'):
            print("test5")
            qid = data['ID']
            dets = data['Det']
            isCor = data['Cor']
            temp = addAnswer(qid,dets,isCor)
            temp2 = viewSpecQuiz(temp)
            response = {'display': temp2}
            return jsonify(response)
        #delete quiz
        if (data['request'] == 'delQuiz'):
            print("test6")
            qid = data['ID']
            temp = deleteQuiz(qid)
            temp2 = viewAllQuiz()
            response = {'output': temp, 'display': temp2}
            return jsonify(response)
        #delete question
        if (data['request'] == 'delQuestion'):
            print("test7")
            qid = data['ID']
            temp = deleteQuestion(qid)
            temp2 = viewAllQuiz()
            response = {'output': temp, 'display': temp2}
            return jsonify(response)
        #delete answer
        if (data['request'] == 'delAnswer'):
            print("test8")
            qid = data['ID']
            temp = deleteAnswer(qid)
            temp2 = viewAllQuiz()
            response = {'output': temp, 'display': temp2}
            return jsonify(response)
        #add user
        if (data['request'] == 'addUser'):
            print("test9")
            uN = data['username']
            pas = data['password']
            fN = data['fName']
            lN = data['lName']
            r = data['role']

            temp = addUser(uN,pas,fN,lN,r)
            print(temp)
            response = {'status': temp}
            return jsonify(response)

        #User functions

        # Gather quiz names and time limits for all quizzes
        if (data['request'] == 'getQuiz'):
            conn = sqlite3.connect('quiz.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM quiz'
            )
            out = cursor.fetchall()
            quizzes = [{'name': quiz[1], 'time_limit': quiz[2]} for quiz in out]
            conn.close()
            return jsonify(quizzes)
        
@app.route('/search', methods=['POST'])
def search_quiz():
    search_term = request.json['searchTerm']
    print(f"Search term: {search_term}")  # Debug: print search term
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT qid, qName FROM quiz WHERE qName LIKE ?', ('%' + search_term + '%',)
    )
    out = cursor.fetchall()
    print(f"Query result: {out}")  # Debug: print query result
    quizzes = [{'id': quiz[0], 'name': quiz[1]} for quiz in out]
    print(f"Quizzes list: {quizzes}")  # Debug: print quizzes list
    if quizzes:
        return jsonify({'success': True, 'quizzes': quizzes})
    else:
        return jsonify({'success': False})
    

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/quest/<int:quiz_id>')
def get_questions(quiz_id):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = "SELECT * FROM questions WHERE quiz = ?"
    cursor.execute(query, (quiz_id,))
    questions = cursor.fetchall()
    questions_data = []
    # Gather question and answer data
    for question in questions:
        query = "SELECT * FROM answers WHERE quest = ?"
        cursor.execute(query, (question[0],))
        answers = cursor.fetchall()
        questions_data.append({
            'question': question,
            'answers': answers
        })
    
    # Fetch the time limit for the quiz
    query = "SELECT time FROM quiz WHERE qid = ?"
    cursor.execute(query, (quiz_id,))
    time_limit = cursor.fetchone()[0]
    
    conn.close()
    return jsonify({'questions': questions_data, 'time_limit': time_limit})

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    # Gather questions from desired quiz
    query = "SELECT * FROM questions WHERE quiz = ?"
    cursor.execute(query, (quiz_id,))
    questions = cursor.fetchall()
    total_questions = len(questions)
    score = 0
    # Count how many answers were correct
    for question in questions:
        query = "SELECT * FROM answers WHERE quest = ? AND isCorrect = 1"
        cursor.execute(query, (question[0],))
        correct_answer = cursor.fetchone()[2]
        user_answer = request.json.get('answers')[str(question[0])]
        if user_answer == correct_answer:
            score += 1
    # Convert score into a percentage
    percentage = (score / total_questions) * 100
    conn.close()
    # return score and the quiz id
    return jsonify({'score': percentage, 'quiz_id': quiz_id})

@app.route('/score', methods=['POST'])
def insert_score():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    # Retrieve the score and quiz ID from the request
    score = request.json.get('score')
    quiz_id = request.json.get('quiz_id')
    user_id = session['user']['id']
    # Insert the score into the database
    query = "INSERT INTO scores (quiz, user, score, attempt) VALUES (?, ?, ?, 1)"
    cursor.execute(query, (quiz_id, user_id, score))
    conn.commit()
    conn.close()
    # Return a response indicating that the score was inserted successfully
    return jsonify({'message': 'Score inserted successfully'})

@app.route('/get_scores', methods=['GET'])
def get_scores():
    # Assume you have a `current_user` object with the logged-in user's ID
    user_id = session['user']['id']

    # Query the 'scores' table to retrieve the user's scores, joining with the 'quizzes' table
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    query = """
        SELECT q.qName AS quiz_name, s.score
        FROM scores s
        JOIN quiz q ON s.quiz = q.qid
        WHERE s.user = ?
    """
    cursor.execute(query, (user_id,))
    scores = cursor.fetchall()
    conn.close()

    # Convert the list of tuples to a list of dictionaries
    scores_dict = [{'quiz_name': row[0], 'score': row[1]} for row in scores]

    # Return the scores as JSON
    return jsonify({'scores': scores_dict})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
