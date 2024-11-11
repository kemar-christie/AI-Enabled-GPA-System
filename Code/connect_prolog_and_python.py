# Dwyane Gibbs
import pyswip
import os

# Get the current directory an dprint out the files.
# NB prolog_knowledge_base.pl is showing in the list of files but still getting
# an error ERROR: source_sink `'prolog_knowledge_base.pl'' does not exist
current_dir = os.path.dirname(os.path.abspath(__file__))
# Create the full path to the Prolog file
prolog_file = os.path.join(current_dir, "prolog_knowledge_base.pl")
print("Files in directory:", os.listdir(current_dir))


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
