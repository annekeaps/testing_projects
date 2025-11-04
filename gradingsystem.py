"""
Student Grading System - Simplified Version
For Information System Students

This app demonstrates:
- Unit Testing: Test individual calculations (letter grade, grade point, etc.)
- Integration Testing: Test single subject grading (with weights)
- System Testing: Test multiple subjects grading (complete student report)
"""


class StudentRecord:
    """Student record to store grades"""
    
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = []  # List to store grades
    
    def add_grade(self, subject, score):
        """Add a grade for a subject"""
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        
        grade = {
            'subject': subject,
            'score': score
        }
        self.grades.append(grade)
    
    def get_grades(self):
        """Get all grades"""
        return self.grades


# ========================================
# PART 1: UNIT TESTABLE FUNCTIONS
# Test these functions one by one
# ========================================

def calculate_letter_grade(score):
    """
    Convert numeric score to letter grade
    
    Grading Scale:
    - 90-100 = A
    - 80-89 = B
    - 70-79 = C
    - 60-69 = D
    - 0-59 = E
    """
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")
    
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "E"


def calculate_grade_point(letter_grade):
    """
    Convert letter grade to grade point
    
    Grade Points:
    - A = 4.0
    - B = 3.0
    - C = 2.0
    - D = 1.0
    - E = 0.0
    """
    grade_points = {
        "A": 4.0,
        "B": 3.0,
        "C": 2.0,
        "D": 1.0,
        "E": 0.0
    }
    
    if letter_grade not in grade_points:
        raise ValueError("Invalid letter grade")
    
    return grade_points[letter_grade]


def calculate_average(scores):
    """
    Calculate average of scores
    Example: [80, 90, 70] -> 80.0
    """
    if not scores:
        return 0
    
    if len(scores) == 0:
        return 0
    
    total = sum(scores)
    average = total / len(scores)
    return average


def determine_status(average_score):
    """
    Determine student status based on average
    
    Status Rules:
    - >= 90 = "Excellent"
    - >= 80 = "Very Good"
    - >= 70 = "Good"
    - >= 60 = "Pass"
    - < 60 = "Fail"
    """
    if average_score < 0 or average_score > 100:
        raise ValueError("Average must be between 0 and 100")
    
    if average_score >= 90:
        return "Excellent"
    elif average_score >= 80:
        return "Very Good"
    elif average_score >= 70:
        return "Good"
    elif average_score >= 60:
        return "Pass"
    else:
        return "Fail"


def calculate_weighted_score(scores, weights):
    """
    Calculate weighted average
    
    Example:
    scores = [80, 90, 70]
    weights = [0.3, 0.5, 0.2]
    result = (80*0.3) + (90*0.5) + (70*0.2) = 83.0
    """
    if not scores or not weights:
        return 0
    
    if len(scores) != len(weights):
        raise ValueError("Scores and weights must have same length")
    
    if sum(weights) != 1.0:
        raise ValueError("Weights must sum to 1.0")
    
    weighted_total = 0
    for score, weight in zip(scores, weights):
        weighted_total += score * weight
    
    return weighted_total


# ========================================
# PART 2: INTEGRATION FUNCTION
# Grade ONE subject with multiple components
# ========================================

def grade_subject(subject_name, assignment_score, midterm_score, final_score):
    """
    Calculate grade for ONE subject
    
    Steps:
    1. Calculate weighted score (Assignment 30%, Midterm 30%, Final 40%)
    2. Convert to letter grade
    3. Convert to grade point
    
    This is INTEGRATION testing - combines multiple unit functions
    """
    # Validate scores
    if assignment_score < 0 or assignment_score > 100:
        raise ValueError("Assignment score must be 0-100")
    if midterm_score < 0 or midterm_score > 100:
        raise ValueError("Midterm score must be 0-100")
    if final_score < 0 or final_score > 100:
        raise ValueError("Final score must be 0-100")
    
    # Calculate weighted final score
    scores = [assignment_score, midterm_score, final_score]
    weights = [0.3, 0.3, 0.4]
    final = calculate_weighted_score(scores, weights)
    
    # Convert to letter and grade point
    letter = calculate_letter_grade(final)
    point = calculate_grade_point(letter)
    
    result = {
        "subject": subject_name,
        "assignment": assignment_score,
        "midterm": midterm_score,
        "final_exam": final_score,
        "final_score": final,
        "letter_grade": letter,
        "grade_point": point
    }
    
    return result


# ========================================
# PART 3: SYSTEM FUNCTION
# Grade MULTIPLE subjects for complete student report
# ========================================

def process_student_report(student_name, student_id, subjects_data):
    """
    Process complete student grading with MULTIPLE subjects
    
    This is the MAIN SYSTEM function that does everything:
    1. Grade each subject individually
    2. Calculate overall GPA
    3. Determine overall status
    4. Create complete report
    
    subjects_data format:
    [
        {"subject": "Math", "assignment": 85, "midterm": 90, "final": 88},
        {"subject": "Physics", "assignment": 75, "midterm": 80, "final": 78},
        ...
    ]
    """
    if not subjects_data:
        raise ValueError("Must have at least one subject")
    
    # Grade each subject
    graded_subjects = []
    grade_points = []
    
    for subject_data in subjects_data:
        subject_grade = grade_subject(
            subject_data["subject"],
            subject_data["assignment"],
            subject_data["midterm"],
            subject_data["final"]
        )
        graded_subjects.append(subject_grade)
        grade_points.append(subject_grade["grade_point"])
    
    # Calculate overall GPA
    gpa = calculate_average(grade_points)
    
    # Get average final score for status
    final_scores = [s["final_score"] for s in graded_subjects]
    average_score = calculate_average(final_scores)
    
    # Determine overall status
    status = determine_status(average_score)
    
    # Create complete report
    report = {
        "student_id": student_id,
        "name": student_name,
        "subjects": graded_subjects,
        "gpa": gpa,
        "average_score": average_score,
        "status": status
    }
    
    return report


def print_student_report(report):
    """Print complete student report nicely"""
    print("\n" + "=" * 60)
    print("STUDENT GRADE REPORT")
    print("=" * 60)
    print(f"Student ID: {report['student_id']}")
    print(f"Name: {report['name']}")
    print("=" * 60)
    
    print("\nSUBJECTS:")
    for subject in report['subjects']:
        print(f"\n  {subject['subject']}:")
        print(f"    Assignment (30%): {subject['assignment']}")
        print(f"    Midterm (30%): {subject['midterm']}")
        print(f"    Final Exam (40%): {subject['final_exam']}")
        print(f"    Final Score: {subject['final_score']:.2f}")
        print(f"    Grade: {subject['letter_grade']} (GP: {subject['grade_point']:.1f})")
    
    print("\n" + "-" * 60)
    print(f"Overall GPA: {report['gpa']:.2f}")
    print(f"Average Score: {report['average_score']:.2f}")
    print(f"Status: {report['status']}")
    print("=" * 60 + "\n")


def print_subject_report(subject_grade):
    """Print single subject grade nicely"""
    print("\n" + "=" * 50)
    print(f"SUBJECT: {subject_grade['subject']}")
    print("=" * 50)
    print(f"Assignment (30%): {subject_grade['assignment']}")
    print(f"Midterm (30%): {subject_grade['midterm']}")
    print(f"Final Exam (40%): {subject_grade['final_exam']}")
    print("-" * 50)
    print(f"Final Score: {subject_grade['final_score']:.2f}")
    print(f"Letter Grade: {subject_grade['letter_grade']}")
    print(f"Grade Point: {subject_grade['grade_point']:.1f}")
    print("=" * 50 + "\n")


# ========================================
# DEMO - How to use the app
# ========================================

def main():
    """Demo of the grading system"""
    print("=== STUDENT GRADING SYSTEM DEMO ===\n")
    
    # ============================================
    # INTEGRATION TEST DEMO: Grade single subject
    # ============================================
    print("=" * 60)
    print("INTEGRATION TEST: Single Subject Grading")
    print("=" * 60)
    
    print("\n--- Subject 1: Mathematics ---")
    math_grade = grade_subject("Mathematics", 85, 90, 88)
    print_subject_report(math_grade)
    
    print("--- Subject 2: Physics ---")
    physics_grade = grade_subject("Physics", 75, 80, 78)
    print_subject_report(physics_grade)
    
    print("--- Subject 3: English ---")
    english_grade = grade_subject("English", 92, 88, 95)
    print_subject_report(english_grade)
    
    # ============================================
    # SYSTEM TEST DEMO: Complete student report with multiple subjects
    # ============================================
    print("\n" + "=" * 60)
    print("SYSTEM TEST: Multiple Subjects - Complete Student Report")
    print("=" * 60)
    
    # Student 1 - Excellent student (3 subjects)
    print("\n--- STUDENT 1: Budi Santoso (Excellent) ---")
    student1_subjects = [
        {"subject": "Mathematics", "assignment": 95, "midterm": 92, "final": 98},
        {"subject": "Physics", "assignment": 90, "midterm": 88, "final": 92},
        {"subject": "English", "assignment": 92, "midterm": 95, "final": 90}
    ]
    report1 = process_student_report("Budi Santoso", "S001", student1_subjects)
    print_student_report(report1)
    
    # Student 2 - Average student (4 subjects)
    print("--- STUDENT 2: Siti Nurhaliza (Average) ---")
    student2_subjects = [
        {"subject": "Mathematics", "assignment": 75, "midterm": 78, "final": 72},
        {"subject": "Physics", "assignment": 80, "midterm": 75, "final": 78},
        {"subject": "Chemistry", "assignment": 70, "midterm": 72, "final": 75},
        {"subject": "Biology", "assignment": 78, "midterm": 80, "final": 76}
    ]
    report2 = process_student_report("Siti Nurhaliza", "S002", student2_subjects)
    print_student_report(report2)
    
    # Student 3 - Struggling student (2 subjects)
    print("--- STUDENT 3: Ahmad Wijaya (Struggling) ---")
    student3_subjects = [
        {"subject": "Mathematics", "assignment": 55, "midterm": 48, "final": 52},
        {"subject": "Physics", "assignment": 60, "midterm": 58, "final": 55}
    ]
    report3 = process_student_report("Ahmad Wijaya", "S003", student3_subjects)
    print_student_report(report3)


if __name__ == "__main__":
    main()
