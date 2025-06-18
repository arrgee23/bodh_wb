import sqlite3
import os
import json

def create_table():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS questions""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        paper TEXT NOT NULL,
        question_no TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def process_json_folder(folder_path):
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    passed = 0
    failed = 0
    for file_name in sorted(os.listdir(folder_path)):
        
        if file_name.endswith(".json"):
            print(f"Processing file: {file_name}")
            file_path = os.path.join(folder_path, file_name)
            paper = file_name.split(".")[0][:-4]
            print(f"Paper name: {paper}")
            with open(file_path, "r") as file:
                data = json.load(file)
                questions = data.get("questions", [])
                for question in questions:
                    try:
                        question_text = question.get("question", "")
                        question_number = question.get("question_number","")
                        options = question.get("options", [])
                        if len(options) != 4:
                            print(f"Skipping question: {question_number} due to invalid options: {options}")
                            continue
                        
                        correct_option = question.get("answer", "").lower()
                        correct_option_text = None
                        if correct_option == "a":
                            correct_option_text = options[0]
                        elif correct_option == "b":
                            correct_option_text = options[1]
                        elif correct_option == "c":
                            correct_option_text = options[2]
                        elif correct_option == "d":
                            correct_option_text = options[3]
                        else:
                            print(f"Skipping question: {question_number} due to invalid answer: {correct_option}")
                            continue

                        cursor.execute("""
                        INSERT INTO questions (question, option1, option2, option3, option4, correct_option, paper, question_no)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (question_text, 
                              options[0], 
                              options[1], 
                              options[2], 
                              options[3], 
                              correct_option_text,
                              paper,
                              question_number))
                        passed += 1
                    except:
                        failed += 1
                        #print(f"Error processing question: {question}. Error: {e}")

            print(f"Processed file: {file_name}, Passed: {passed}, Failed: {failed}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    folder_path = "/Users/rahul/Documents/bodh/data/papers/iit"  # Replace with the path to your folder containing JSON files
    process_json_folder(folder_path)
    print("Questions have been successfully added to the database.")