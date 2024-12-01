# Dwyane Gibbs
from pyswip import Prolog
import os


# Load the Prolog file
prolog = Prolog
prolog.consult("prolog_knowledge_base.pl")


def get_grade_info(score):
    """Get letter grade and grade point for a given score."""
    try:
        query = f"score_to_grade({float(score)}, LetterGrade, GradePoint)"
        for result in prolog.query(query):
            return result["LetterGrade"].decode("utf-8"), float(result["GradePoint"])
        return None, None
    except Exception as e:
        print(f"Error getting grade info: {e}")
        return None, None


def process_semester_grades(credits, scores):
    """Process grades for a semester, returning letters, GPAs, and points."""
    try:
        credits_str = f"[{','.join(map(str, credits))}]"
        scores_str = f"[{','.join(map(str, scores))}]"

        query = f"process_grades({credits_str}, {scores_str}, Letters, GPAs, Points)"

        for result in prolog.query(query):
            return {
                "letters": [letter.decode("utf-8") for letter in result["Letters"]],
                "gpas": [float(gpa) for gpa in result["GPAs"]],
                "points": [float(point) for point in result["Points"]],
            }
        return None
    except Exception as e:
        print(f"Error processing semester grades: {e}")
        return None


def calculate_semester_gpa(credits, scores):
    """Calculate GPA for a single semester."""
    try:
        credits_str = f"[{','.join(map(str, credits))}]"
        scores_str = f"[{','.join(map(str, scores))}]"

        query = f"calculate_semester_gpa({credits_str}, {scores_str}, GPA)"

        for result in prolog.query(query):
            return float(result["GPA"])
        return None
    except Exception as e:
        print(f"Error calculating semester GPA: {e}")
        return None


def calculate_cumulative_gpa(credits1, scores1, credits2, scores2):
    """Calculate cumulative GPA across two semesters."""
    try:
        credits1_str = f"[{','.join(map(str, credits1))}]"
        scores1_str = f"[{','.join(map(str, scores1))}]"
        credits2_str = f"[{','.join(map(str, credits2))}]"
        scores2_str = f"[{','.join(map(str, scores2))}]"

        query = (
            f"calculate_cumulative_gpa({credits1_str}, {scores1_str}, "
            f"{credits2_str}, {scores2_str}, CGPA)"
        )

        for result in prolog.query(query):
            return float(result["CGPA"])
        return None
    except Exception as e:
        print(f"Error calculating cumulative GPA: {e}")
        return None


def update_default_gpa(new_gpa):
    """Update the default GPA threshold."""
    try:
        list(prolog.query(f"update_default_gpa({float(new_gpa)})"))
        return True
    except Exception as e:
        print(f"Error updating default GPA: {e}")
        return False
