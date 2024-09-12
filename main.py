from flask import Flask, render_template, request, jsonify, redirect, session



app = Flask(__name__)
app.secret_key = 'your_secret_key'

