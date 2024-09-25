from flask import Flask, render_template, request, jsonify, redirect, session
from init import sys_init
from uLogin import login, User

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
            return render_template('home.html', user_info=user)
        
    else:
        return redirect('/?messages=Please login again!')