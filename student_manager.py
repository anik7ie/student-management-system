def read_file_lines(filename):
    lines = []
    try:
        f = open(filename, "r")
        for line in f:
            lines.append(line.strip())
        f.close()
    except FileNotFoundError:
        return []
    return lines

def parse_course_line(line):
    if not line:
        return None
    parts = line.split(",")
    if len(parts) < 3:
        return None
    
    return {
        "code": parts[0],
        "name": parts[1],
        "credits": int(parts[2]),
        "teachers": parts[3:]
    }

def parse_student_line(line):
    if not line:
        return None
    parts = line.split(",")
    if len(parts) < 7:
        return None
    return {
        "id": parts[0],
        "last": parts[1],
        "first": parts[2],
        "middle": parts[3],
        "email": parts[4],
        "year": parts[5],
        "prog": parts[6]
    }

def parse_passed_line(line):
    if not line:
        return None
    parts = line.split(",")
    if len(parts) != 4:
        return None
    
    return {
        "course": parts[0],
        "student": parts[1],
        "date": parts[2],
        "grade": int(parts[3])
    }

def load_data():
    courses = []
    students = []
    passed = []
    
    for line in read_file_lines("courses.txt"):
        course = parse_course_line(line)
        if course:
            courses.append(course)
    
    for line in read_file_lines("students.txt"):
        student = parse_student_line(line)
        if student:
            students.append(student)
    
    for line in read_file_lines("passed.txt"):
        record = parse_passed_line(line)
        if record:
            passed.append(record)
    
    return courses, students, passed

def show_options():
    return prompt_choice_0_5()

def get_input_data(prompts):
    data = []
    for prompt in prompts:
        data.append(input(prompt))
    return data

def save_to_file(filename, line):
    f = open(filename, "a")
    f.write(line)
    f.close()


def prompt_name(prompt_text, allow_empty=False):
    while True:
        text = input(prompt_text).strip()
        if is_valid_name_part(text, allow_empty=allow_empty):
            return text
        print("Names should contain only letters and start with capital letters.")

def prompt_minlen(prompt_text, min_len, error_text):
    while True:
        text = input(prompt_text)
        t = text.strip()
        if len(t) >= min_len:
            return t
        print(error_text)

def prompt_choice_0_5():
    while True:
        print("You may select one of the following:")
        print(" 1) Add student")
        print(" 2) Search student")
        print(" 3) Search course")
        print(" 4) Add course completion")
        print(" 5) Show student's record")
        print(" 0) Exit")
        choice = input("\nWhat is your selection? ").strip()
        if choice in ["0","1","2","3","4","5"]:
            return choice
        print("Please enter a number between 0 and 5.")

def is_valid_name_part(text, allow_empty=False):
    if allow_empty and text == "":
        return True
    if text == "":
        return False
    if not text[0].isupper():
        return False
    for ch in text:
        if not ch.isalpha():
            return False
    return True

def is_valid_program(code):
    if code is None:
        return False
    code = code.strip().upper()
    valid = ["CE", "EE", "SE", "ET", "ME"]
    for v in valid:
        if code == v:
            return True
    return False

def generate_next_student_id(students):
    max_id = 0
    for s in students:
        try:
            num = int(s["id"])
            if num > max_id:
                max_id = num
        except (ValueError, TypeError):
            continue
    return str(max_id + 1)

def generate_email(first, last):
    return first.lower() + "." + last.lower() + "@lut.fi"

def add_student(students, passed):
    print("\n--- Add student ---")
    first = prompt_name("Enter the first name of the student: ", allow_empty=False)
    last = prompt_name("Enter the last name of the student: ", allow_empty=False)
    middle = prompt_name("Enter the middle name (just press enter and leave it blank if no middle name) of the student: ", allow_empty=True)

    print("Select student's major:")
    print("CE: Computational Engineering")
    print("EE: Electrical Engineering")
    print("ET: Energy Technology")
    print("ME: Mechanical Engineering")
    print("SE: Software Engineering")

    while True:
        prog = input("What is your selection? ").strip().upper()
        if prog in ["CE","EE","ET","ME","SE"]:
            break
        print("Please select one of the following majors: CE, EE, ET, ME, SE.")

    year = get_current_year(students, passed)
    student_id = generate_next_student_id(students)
    email = generate_email(first, last)

    student = {
        "id": student_id,
        "last": last,
        "first": first,
        "middle": middle,
        "email": email,
        "year": year,
        "prog": prog
    }

    students.append(student)

    # Save in the same csv format as before
    line = student["id"] + "," + student["last"] + "," + student["first"] + "," + student["middle"] + "," + student["email"] + "," + student["year"] + "," + student["prog"] + "\n"
    save_to_file("students.txt", line)
    print("Added!")
def match_student(student, query):
    if student["id"] == query:
        return True
    q = query.strip().lower()
    if q == "":
        return False
    if q in student["last"].lower():
        return True
    if q in student["first"].lower():
        return True
    middle = student.get("middle", "")
    if middle and q in middle.lower():
        return True
    return False

def match_course(course, query):
    q = query.strip()
    if q == "":
        return False

    # Code match (partial, case-insensitive)
    q_low = q.lower()
    if q_low in course["code"].lower():
        return True

    # Case-insensitive contains for name and teachers
    if q_low in course["name"].lower():
        return True

    teachers = course.get("teachers", [])
    for t in teachers:
        if q_low in t.lower():
            return True
    return False

def format_student_name(student):
    parts = [student["first"]]
    if student["middle"]:
        parts.append(student["middle"])
    parts.append(student["last"])
    
    full_name = ""
    count = 0
    for part in parts:
        full_name = full_name + part
        count = count + 1
        if count < len(parts):
            full_name = full_name + " "
            
    return full_name

def show_student(student):
    print("\nID:", student["id"])
    print("Name:", format_student_name(student))
    print("Email:", student["email"])
    print("Program:", student["prog"], "(" + student["year"] + ")")

def show_course(course):
    print("\nCode:", course["code"])
    print("Name:", course["name"])
    print("Credits:", course["credits"])
    
    if course["teachers"]:
        t_str = ""
        teachers = course["teachers"]
        count = 0
        for t in teachers:
            t_str = t_str + t
            count = count + 1
            if count < len(teachers):
                t_str = t_str + ", "
        print("Teachers:", t_str)
    else:
        print("Teachers: None")

def find_student(students):
    print("\n--- Search student ---")
    query = prompt_minlen("Give at least 3 characters of the students first, middle or last name: ", 3,
                         "Give at least 3 characters of the students first, middle or last name:")

    
    matches = []
    for student in students:
        if match_student(student, query):
            matches.append(student)
    
    if matches:
        print("Found", len(matches), "result(s):")
        for student in matches:
            show_student(student)
    else:
        print("No matching students.")

def find_course(courses):
    print("\n--- Search course ---")
    query = prompt_minlen("Give at least 3 characters of the course code, name or teacher: ", 3,
                         "Give at least 3 characters of the course code, name or teacher:")

    
    matches = []
    for course in courses:
        if match_course(course, query):
            matches.append(course)
    
    if matches:
        print("Found", len(matches), "result(s):")
        for course in matches:
            show_course(course)
    else:
        print("No matching courses.")

def check_exists(collection, id_field, target):
    for item in collection:
        if item[id_field] == target:
            return True
    return False

def is_valid_grade(text):
    valid_grades = ["1", "2", "3", "4", "5"]
    for v in valid_grades:
        if text == v:
            return True
    return False

def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0

def days_in_month(year, month):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    if month in [4, 6, 9, 11]:
        return 30
    if month == 2:
        if is_leap_year(year):
            return 29
        return 28
    return 0

def parse_date_yyyy_mm_dd(text):
    try:
        parts = text.split("-")
        if len(parts) != 3:
            return None
        y = int(parts[0]); m = int(parts[1]); d = int(parts[2])
        if y < 1 or m < 1 or m > 12:
            return None
        dim = days_in_month(y, m)
        if d < 1 or d > dim:
            return None
        return (y, m, d)
    except:
        return None

def date_to_ordinal(date_tuple):
    y, m, d = date_tuple
    days = 0
    for year in range(1, y):
        if is_leap_year(year):
            days = days + 366
        else:
            days = days + 365
    for month in range(1, m):
        days = days + days_in_month(y, month)
    days = days + d
    return days

def get_latest_passed_date(passed):
    latest = None
    for r in passed:
        d = parse_date_yyyy_mm_dd(r["date"])
        if not d:
            continue
        if latest is None:
            latest = d
        else:
            if date_to_ordinal(d) > date_to_ordinal(latest):
                latest = d
    return latest

def get_current_year(students, passed):
    latest = get_latest_passed_date(passed)
    if latest:
        return str(latest[0])
    max_year = 0
    for s in students:
        try:
            y = int(s["year"])
            if y > max_year:
                max_year = y
        except (ValueError, TypeError):
            continue
    if max_year == 0:
        return "0"
    return str(max_year)

def rewrite_passed_file(passed):
    f = open("passed.txt", "w")
    for r in passed:
        line = r["course"] + "," + r["student"] + "," + r["date"] + "," + str(r["grade"]) + "\n"
        f.write(line)
    f.close()

def add_grade(students, courses, passed):
    print("\n--- Add Grade ---")
    course_code = input("Course: ").strip()
    student_id = input("Student ID: ").strip()
    date_text = input("Date (YYYY-MM-DD): ").strip()
    grade_text = input("Grade (1-5): ").strip()

    if not is_valid_grade(grade_text):
        print("Please enter a grade between 1 and 5.")
        return

    if not check_exists(students, "id", student_id):
        print("No such student. Please enter an existing student ID.")
        return

    if not check_exists(courses, "code", course_code):
        print("No such course. Please enter an existing course code.")
        return

    d = parse_date_yyyy_mm_dd(date_text)
    if not d:
        print("Please enter date in format YYYY-MM-DD.")
        return

    today = get_latest_passed_date(passed)
    if today:
        d_ord = date_to_ordinal(d)
        today_ord = date_to_ordinal(today)
        if d_ord > today_ord:
            print("Please enter date in format YYYY-MM-DD.")
            return
        if (today_ord - d_ord) > 30:
            print("Please enter date in format YYYY-MM-DD.")
            return

    new_grade = int(grade_text)

    # If record exists, update only if new grade is better
    updated = False
    for r in passed:
        if r["course"] == course_code and r["student"] == student_id:
            if new_grade > int(r["grade"]):
                r["grade"] = new_grade
                r["date"] = date_text
                updated = True
            else:
                print("Existing grade is better or equal, no update")
                return

    if updated:
        rewrite_passed_file(passed)
        print("Updated!")
        return

    record = {
        "course": course_code,
        "student": student_id,
        "date": date_text,
        "grade": new_grade
    }
    passed.append(record)
    save_to_file("passed.txt", course_code + "," + student_id + "," + date_text + "," + grade_text + "\n")
    print("Added!")

def get_student_records(student_id, passed):
    records = []
    for record in passed:
        if record["student"] == student_id:
            records.append(record)
    return records

def filter_best_grades(records):
    best = {}
    for record in records:
        code = record["course"]
        if code not in best:
             best[code] = record
        else:
            current_best = best[code]
            if record["grade"] > current_best["grade"]:
                best[code] = record
    return best

def get_course_info(courses, code):
    for course in courses:
        if course["code"] == code:
            return course
    return None

def program_full_name(code):
    mapping = {
        "CE": "Computational Engineering",
        "EE": "Electrical Engineering",
        "SE": "Software Engineering",
        "ET": "Energy Technology",
        "ME": "Mechanical Engineering"
    }
    return mapping.get(code, code)

def teachers_as_string(course):
    teachers = course.get("teachers", [])
    if not teachers:
        return "None"
    s = ""
    i = 0
    for t in teachers:
        s = s + t
        i = i + 1
        if i < len(teachers):
            s = s + ", "
    return s

def show_transcript(students, courses, passed):
    print("\n--- Transcript ---")
    student_id = input("Student ID: ").strip()

    student = None
    for s in students:
        if s["id"] == student_id:
            student = s
            break

    if not student:
        print("No matching students.")
        return

    # Student header (full program name)
    print("\nID:", student["id"])
    print("Name:", format_student_name(student))
    print("Email:", student["email"])
    print("Program:", program_full_name(student["prog"]), "(" + student["year"] + ")")

    records = get_student_records(student_id, passed)
    if not records:
        print("\nNo passed courses")
        return

    best = filter_best_grades(records)

    total_credits = 0
    gpa_points = 0
    gpa_credits = 0

    for course_code in best:
        record = best[course_code]
        course = get_course_info(courses, course_code)
        if not course:
            continue

        credits = int(course["credits"])
        grade = int(record["grade"])

        print("\n" + course_code + ": " + course["name"])
        print("  Teachers:", teachers_as_string(course))
        print("  Grade:", grade, "| Date:", record["date"], "| Credits:", credits)

        total_credits = total_credits + credits
        gpa_points = gpa_points + (grade * credits)
        gpa_credits = gpa_credits + credits

    print("\nTotal:", total_credits, "credits")
    if gpa_credits > 0:
        gpa = gpa_points / gpa_credits
        print("GPA:", "{:.2f}".format(gpa))
courses, students, passed = load_data()
print("Loaded: " + str(len(students)) + " students, " + str(len(courses)) + " courses")

running = True
while running:
    choice = show_options()
    
    if choice == "1":
        add_student(students, passed)
    elif choice == "2":
        find_student(students)
    elif choice == "3":
        find_course(courses)
    elif choice == "4":
        add_grade(students, courses, passed)
    elif choice == "5":
        show_transcript(students, courses, passed)
    elif choice == "0":
        print("Bye!")
        running = False
    else:
        print("Invalid")
