


#from flask import Flask, render_template, request, redirect, url_for, jsonify
#import sqlite3
#import random
#from api.routes import api

#app = Flask(__name__)

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route("/test1")
def test1():
    return render_template("mocktest-env.html")

"""
# Route to display the test
@app.route("/")
def index():
    
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    questions = cursor.fetchall()
    conn.close()
    
    return render_template("index.html")





# Route to handle test submission
@app.route("/submit", methods=["POST"])
def submit():
    answers = request.form
    score = 0
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    for qid, user_answer in answers.items():
        cursor.execute("SELECT correct_option FROM questions WHERE id = ?", (qid,))
        correct_answer = cursor.fetchone()[0]
        if user_answer == correct_answer:
            score += 1
    conn.close()
    return f"Your score is {score}/10"
"""