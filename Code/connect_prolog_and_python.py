# Dwyane Gibbs
import pyswip
from pyswip import Prolog

# Load the Prolog file
prolog = pyswip.Prolog()
prolog.consult("prolog_knowledge_base.pl")


# Define a function to get the letter grade and grade point for a given score
def get_grade_info(score):
    for result in prolog.query(f"score_to_grade({score}, LetterGrade, GradePoint)"):
        return result["LetterGrade"], result["GradePoint"]
    return None, None


# Define a function to add two numbers
def add_numbers(num1, num2):
    for result in prolog.query(f"add_numbers({num1}, {num2}, Total)"):
        return result["Total"]
    return None


# Define a function to divide two numbers
def divide_numbers(num1, num2):
    for result in prolog.query(f"divide_numbers({num1}, {num2}, Total)"):
        return result["Total"]
    return None


# Define a function to update the default GPA
def update_default_gpa(new_gpa):
    prolog.assertz(f"update_default_gpa({new_gpa})")
