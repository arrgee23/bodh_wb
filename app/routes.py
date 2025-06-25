#from flask import Flask, render_template, request, redirect, url_for, jsonify
#import sqlite3
#import random
#from api.routes import api

#app = Flask(__name__)

from flask import Blueprint, render_template
import sqlite3
import json

main = Blueprint('main', __name__)

def form_questions():
    """
    read questions from the db and load into a list of dictionaries
     of the form:
     [
       {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Kolkata", "Chennai"],
        "answer": "Delhi"
    }]
     assume the table already exists
    with the following schema:
    Schema Info:
    (0, 'question_number', 'INTEGER', 0, None, 0)
    (1, 'question', 'TEXT', 0, None, 0)
    (2, 'has_image', 'BOOLEAN', 0, None, 0)
    (3, 'image_detections', 'TEXT', 0, None, 0)
    (4, 'options', 'TEXT', 0, None, 0)
    (5, 'answer', 'TEXT', 0, None, 0)
    (6, 'page_number', 'INTEGER', 0, None, 0)
    (7, 'question_topic', 'TEXT', 0, None, 0)
    (8, 'question_sub_topic', 'TEXT', 0, None, 0)
    (9, 'question_difficulty', 'TEXT', 0, None, 0)
    (10, 'question_type', 'TEXT', 0, None, 0)
"""
    
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, options, answer FROM questions")
    rows = cursor.fetchall()
    conn.close()
    questions = []
    for row in rows:
        # options are stored as a JSON string, so parse them
        options = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        questions.append({
            "question": row[0],
            "options": options,
            "answer": row[2]
        })
    return questions

@main.route('/')
def index():
    return render_template("index.html")

@main.route("/test1")
def test1():
    # read from the database
    import sqlite3
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = form_questions(cursor.fetchall())
    conn.close()
    return render_template("mocktest-env.html", questions=questions)

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