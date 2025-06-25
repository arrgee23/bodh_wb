import json
import sqlite3

class DatabaseHandler:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def form_questions(self):
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
    
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT question, options, answer FROM questions")
        rows = cursor.fetchall()
        conn.close()
        questions = []
        for row in rows:
            # options are stored as a JSON string, so parse them
            options = json.loads(row[1]) if isinstance(row[1], str) else row[0]
            questions.append({
                "question": row[0],
                "options": options,
                "answer": row[2]
            })
        return questions


if __name__ == "__main__":
    db_handler = DatabaseHandler("/Users/rahul/Documents/repo/bodh_wb/app/v2.db")
    a = db_handler.fetch_all("select * from sqlite_master")  # This will fetch all rows from the questions table
    #print(a)  # This will print the fetched rows from the database
    questions = db_handler.form_questions()
    print(questions[:2])  # This will print the list of questions fetched from the database