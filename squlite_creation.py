import sqlite3

conn = sqlite3.connect("questions.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    correct_option TEXT NOT NULL
)
""")

# Add sample questions
sample_questions = [
    ("What is the capital of France?", "Paris", "London", "Berlin", "Madrid", "Paris"),
    ("What is 2 + 2?", "3", "4", "5", "6", "4"),
    # Add more questions here
]

cursor.executemany("""
INSERT INTO questions (question, option1, option2, option3, option4, correct_option)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_questions)

conn.commit()
conn.close()