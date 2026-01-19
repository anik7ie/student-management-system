# Student Management System

A Python-based command-line interface (CLI) for managing students, courses, and grades.

## Features

-   **Add Student**: Register new students with their details and major.
-   **Search**: Find students by name or courses by code/name/teacher.
-   **Add Grade**: Record course completion and grades.
-   **Transcript**: View a student's academic record, including GPA calculation.
-   **Data Persistence**: Saves data to local text files (`students.txt`, `passed.txt`).

## Project Structure

-   `project.py`: Main application logic.
-   `students.txt`: Database of registered students.
-   `courses.txt`: List of available courses.
-   `passed.txt`: Record of completed courses and grades.

## How to Run

Ensure you have Python 3 installed.

```bash
python3 project.py
```

## Usage

Follow the on-screen prompts to navigate the menu:

1.  **Add student**: Enter details for a new student.
2.  **Search student**: Search by partial name.
3.  **Search course**: Search by course code or name.
4.  **Add course completion**: Enter student ID, course code, grade, and date.
5.  **Show student's record**: View a transcript and GPA.
0.  **Exit**: Close the application.
