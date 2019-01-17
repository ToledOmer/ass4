import os
import sqlite3
import create_db

DB_Path = "schedule.db"
def is_in_proccess(course, _conn):
    c = _conn.cursor()
    courses_in_proccess = c.execute("""
        SELECT * FROM classrooms WHERE current_course_time_left != ?
    """, (0,)).fetchall()
    if courses_in_proccess :
        for i in courses_in_proccess:
            if i[2] == course[0]:
                return True
    return False

def all_class_available(_conn):
    c = _conn.cursor()
    available_classes = c.execute("""
        SELECT * FROM classrooms WHERE current_course_time_left=(?)
    """, (0,)).fetchall()

    return [row for row in available_classes]

def assign_course(_conn, course, classroom, iteration_counter):
    if course:
        print("({})".format(iteration_counter), classroom[1] + ": ", course[1], "is schedule to start")
        c = _conn.cursor()
        c.execute("""
                    UPDATE classrooms SET current_course_id=(?), current_course_time_left=(?) WHERE id=(?)
                            """, [course[0], course[5], classroom[0]])
        _conn.commit()

        # students allowed to take that course should be deducted
        # from the total amount of available students since each student is allowed to participate only in
        # a single course
        c.execute("""
                        SELECT count FROM students WHERE grade = (?)
                                """, (course[2],))
        nun_of_students = c.fetchone()[0] - course[3]
        if nun_of_students<0:
            c.execute("""UPDATE students SET count = (?) WHERE grade = (?)""", (0, course[2]))
            _conn.commit()
        else:
            c.execute("""UPDATE students SET count = (?) WHERE grade = (?)""", (nun_of_students,course[2]))
            _conn.commit()





def main():
    db_exist = os.path.isfile(DB_Path)
    conn = sqlite3.connect(DB_Path)
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT * FROM courses
                                """)
        course_tuples = cursor.fetchall()
        iteration_counter = 0
        while db_exist and (len(course_tuples) != 0):
            available_classes = all_class_available(conn)
            # occupied classes
            cursor.execute("""
                                           SELECT cl.location, co.course_name, cl.id
                                           FROM classrooms as cl 
                                           JOIN courses as co
                                           ON cl.current_course_id = co.id AND current_course_time_left != 0
                                                          """)
            occupied_classes = cursor.fetchall()
            for i in occupied_classes:
                cursor.execute("""SELECT current_course_time_left FROM classrooms WHERE id=(?)""", (i[2],))
                time_left = cursor.fetchall()[0][0] - 1
                if time_left != 0 :
                    print("({})".format(iteration_counter), i[0] + ": occupied by", i[1])
                cursor.execute("""UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)""",
                               (time_left, i[2]))
                conn.commit()

            cursor.execute(""" 
                                        SELECT * FROM courses  
                                                                """)
            for classroom in available_classes:
                cursor.execute(""" 
                                    SELECT * FROM courses WHERE class_id=(?) 
                                                            """, (classroom[0],))
                course = cursor.fetchone()
                assign_course(conn, course, classroom, iteration_counter)



            # gets all the classes where course is ended for print
            cursor.execute("""
                                           SELECT cl.*, co.*
                                           FROM classrooms as cl 
                                           JOIN courses as co
                                           ON cl.current_course_id = co.id AND current_course_time_left = (?)
                                                          """, (0,))

            ended_courses = cursor.fetchall()
            for course in ended_courses:
                print("({})".format(iteration_counter), course[1] + ":", course[5], 'is done')
                # remove the course
                cursor.execute("""
                                                    DELETE FROM courses WHERE id =(?)
                                """, (course[4],))
                cursor.execute("""UPDATE classrooms SET current_course_id = (?) WHERE id = (?)""",
                               (0, course[0]))
                conn.commit()


                available_classes = all_class_available(conn)
                for classroom in available_classes:
                    cursor.execute(""" 
                                        SELECT * FROM courses WHERE class_id=(?) 
                                                                """, (course[0],))
                    ncourse = cursor.fetchone()
                    if ncourse:
                        if not is_in_proccess(ncourse, conn):
                            assign_course(conn, ncourse, classroom, iteration_counter)


            # print tables
            cursor.execute("""
                                   SELECT * FROM courses
                                                """)
            course_tuples = cursor.fetchall()
            print("courses")
            create_db.print_table(course_tuples)

            cursor.execute("""
                                                               SELECT * FROM classrooms
                                                       """)
            classrooms_tuples = cursor.fetchall()
            print("classrooms")
            create_db.print_table(classrooms_tuples)

            cursor.execute("""
                                SELECT * FROM students
                                           """)
            students_tuples = cursor.fetchall()
            print("students")
            create_db.print_table(students_tuples)



            iteration_counter += 1
            # check if there are more courses and exit while if not
            # cursor.execute("""
            #                         SELECT * FROM courses
            #                                 """)
            # course_tuples = cursor.fetchall()

if __name__ == '__main__':
    main()



