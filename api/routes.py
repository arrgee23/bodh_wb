from flask import Blueprint, jsonify, request
import sqlite3

api = Blueprint('api', __name__)

@api.route('/questions', methods=['GET'])
def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()

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

@api.route('/submit', methods=['POST'])
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
