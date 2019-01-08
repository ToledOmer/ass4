import atexit
import os
import sqlite3
import sys


DB_Path = "schedule.db"
def main(path):
    db_exist = os.path.isfile(DB_Path)
    conn = sqlite3.connect(DB_Path)
    with conn:
        cursor = conn.cursor()
        if not db_exist:
            cursor.execute("""
                    CREATE TABLE courses (            
                        id INTEGER PRIMARY KEY,
                        course_name TEXT NOT NULL,
                        student TEXT NOT NULL,
                        number_of_students INTEGER NOT NULL,
                        class_id INTEGER REFERENCES classrooms(id),
                        course_length INTEGER NOT NULL                   
                    )""")
            cursor.execute("""
                    CREATE TABLE students (
                        grade TEXT PRIMARY KEY,
                        count INTEGER NOT NULL
                    )""")
            cursor.execute("""
                    CREATE TABLE classrooms (
                        id INTEGER PRIMARY KEY,
                        location TEXT NOT NULL,
                        current_course_id INTEGER NOT NULL,
                        current_course_time_left INTEGER NOT NULL
                    )""")

            with open(path) as config_file:
                for line in config_file.readlines():
                    new_line = line.strip().split(", ")
                    if new_line[0] == "S":
                        conn.execute("""
                                       INSERT INTO students (grade,count) VALUES (?, ?)
                                   """, new_line[1:])
                    if new_line[0] == "C":
                        conn.execute("""
                                        INSERT INTO courses (id, course_name, student, number_of_students, class_id, course_length) VALUES (?, ?, ?, ?, ?, ?)
                                """, new_line[1:])
                    if new_line[0] == "R":
                        new_line.append(0)
                        new_line.append(0)
                        conn.execute("""
                                    INSERT INTO classrooms (id, location, current_course_id,current_course_time_left) VALUES (?,?, ?, ?)
                                """, new_line[1:])

            cursor.execute("""
                            SELECT * FROM courses
                    """)
            course_tuples = cursor.fetchall()
            print_table(course_tuples)
            cursor.execute("""
                                   SELECT * FROM students
                           """)
            students_tuples = cursor.fetchall()
            print_table(students_tuples)

            cursor.execute("""
                                   SELECT * FROM classrooms
                           """)
            classrooms_tuples = cursor.fetchall()
            print_table(classrooms_tuples)
        else:
            exit()



def print_table(list_of_tuples):
 for item in list_of_tuples:
    print(item)


# the repository singleton

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: no config file")
    if not os.path.exists((sys.argv[1])):
        print("Error: config file doesn't exist")
        exit()
    main(sys.argv[1])



