from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import random
from api.routes import api

app = Flask(__name__)

# Register the API blueprint
app.register_blueprint(api, url_prefix='/api')


# Route to display the test
@app.route("/test")
def test():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
    questions = cursor.fetchall()
    conn.close()
    return render_template("test.html", questions=questions)


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


# Route to fetch questions as JSON
@app.route("/api/questions", methods=["GET"])
def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

    # Convert questions to a list of dictionaries
    questions_list = [
        {
            "id": row[0],
            "question": row[1],
            "options": row[2:6],
            "correct_option": row[6]
        }
        for row in questions
    ]

    return jsonify(questions_list)


# Route to submit answers as JSON
@app.route("/api/submit", methods=["POST"])
def submit_answers():
    data = request.json
    score = 0
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()

    for qid, user_answer in data.items():
        cursor.execute("SELECT correct_option FROM questions WHERE id = ?", (qid,))
        correct_answer = cursor.fetchone()[0]
        if user_answer == correct_answer:
            score += 1

    conn.close()
    return jsonify({"score": score, "total": len(data)})
