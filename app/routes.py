#from flask import Flask, render_template, request, redirect, url_for, jsonify
#import sqlite3
#import random
#from api.routes import api

#app = Flask(__name__)

from flask import Blueprint, render_template
from database_handler import DatabaseHandler

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")

@main.route("/test1")
def test1():
    # read from the database
    db_handler = DatabaseHandler("v2.db")
    
    try:
        questions = db_handler.form_questions()
    except Exception as e:
        print(f"Error fetching questions: {e}")
        questions = [{
            "question": f"Error: {e}",
            "options": ["Please check the database connection."],
            "answer": ""
    }]
    return render_template("mocktest-env.html", questions=questions)