import os
import sqlite3
import create_db

DB_Path = "schedule.db"


def all_class_available(_conn):
    c = _conn.cursor()
    available_classes = c.execute("""
        SELECT id FROM classrooms WHERE current_course_time_left=(?)
    """, (0,)).fetchall()

    return [row for row in available_classes]

def main():
    db_exist = os.path.isfile(DB_Path)
    conn = sqlite3.connect(DB_Path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT * FROM courses
                                """)
        course_tuples = cursor.fetchall()
        print(course_tuples)



        while db_exist and (course_tuples is not None):
            cursor.execute("""
                           SELECT * FROM courses
                                        """)
            course_tuples = cursor.fetchall()


            create_db.print_table(course_tuples)
            cursor.execute("""
                        SELECT * FROM students
                                   """)
            students_tuples = cursor.fetchall()
            create_db.print_table(students_tuples)

            cursor.execute("""
                                           SELECT * FROM classrooms
                                   """)
            classrooms_tuples = cursor.fetchall()

            create_db.print_table(classrooms_tuples)
            #
            available_classes = all_class_available(conn)


            cursor.execute("""
                                   SELECT * FROM classrooms WHERE current_course_time_left=(?)
                                                  """, (0,))
            ended_courses = cursor.fetchall()
            for course in ended_courses:
                print(course, 'is done')
            # gets all the classes where course is ended
            cursor.execute("""
                                   SELECT id FROM classrooms WHERE current_course_time_left=(?)
                                                  """, (0,))
            id_ended_courses = cursor.fetchall()
            for id_course in id_ended_courses:
                # remove the course

                cursor.execute("""
                                    DELETE FROM courses where id =(?)
                """(id_course,))


            cursor.execute("""
                            SELECT id FROM classrooms WHERE current_course_time_left=(?)
                                                             """, (0,))

            num_of_available_classes = len(available_classes)

            # for classroom in available_classes:

            # print(available_classes)
            # cursor.execute("""
            #
            #
            #                         """)
                #print the courses that about to start

                #print if occupied and by which course and which course is done


if __name__ == '__main__':
    main()



