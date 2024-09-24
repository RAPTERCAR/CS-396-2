from flask import Flask, render_template, request, jsonify, redirect, session
from init import sys_init


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