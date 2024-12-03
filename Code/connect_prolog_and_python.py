# Dwyane Gibbs
import pyswip
from pyswip import Prolog


# Load the Prolog file
prolog = pyswip.Prolog()

# Python flag to track if the file has been consulted
file_consulted = False  # Initially set the flag to False, indicating the file hasn't been consulted yet.

def consult_prolog():
    global file_consulted  # Declare that we are using the global variable 'file_consulted'
    
    if not file_consulted:  # Check if the flag is False (file has not been consulted yet)
        prolog.consult("prolog_knowledge_base.pl")  # Consult the Prolog knowledge base (load it into memory)
        file_consulted = True  # After consulting, set the flag to True (indicating the file has been consulted)
        print("Prolog file consulted.")  # Print a message indicating the file has been consulted
    else:
        print("Prolog file has already been consulted.")  # If the flag is True, print this message (file already consulted)


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


def update_default_gpa(new_gpa):
    """Update the default GPA threshold."""
    try:
        list(prolog.query(f"update_default_gpa({float(new_gpa)})"))
        return True
    except Exception as e:
        print(f"Error updating default GPA: {e}")
        return False


# Function to get the current default GPA
def get_default_gpa():
    for result in prolog.query("default_gpa(GPA)"):
        return result["GPA"]
    return None  # In case there's no default GPA set


#get the cumulative gpa
def process_student_grades(sem1Credit, sem1Grade, sem2Credit, sem2Grade):

    # Prepare Prolog query for cumulative GPA
    query = f"calculate_cumulative_gpa({sem1Credit}, {sem1Grade},{sem2Credit},{sem2Grade}, CGPA)"
        
    # Query Prolog and extract results for cumulative GPA
    cumulativeGPA = list(prolog.query(query))

    # Prepare Prolog query for  semester 1 GPA
    query2 = f"calculate_semester_gpa({sem1Credit}, {sem1Grade}, SEM1GPA)"
    sem1GPA = list(prolog.query(query2))


    # Prepare Prolog query for semester 2 GPA
    query3 = f"calculate_semester_gpa({sem2Credit}, {sem2Grade}, SEM2GPA)"
    sem2GPA = list(prolog.query(query3))

    if cumulativeGPA==[]:
        cumulativeGPA=[{"CGPA": "N/A"}] # Default to "N/A" if key doesn't exist

    if sem1GPA==[]:
        sem1GPA=[{"SEM1GPA": "N/A"}] # Default to "N/A" if key doesn't exist

    if sem2GPA==[]:
        sem2GPA=[{"SEM2GPA": "N/A"}] # Default to "N/A" if key doesn't exist

    
    result =  f"{sem1GPA[0]["SEM1GPA"]},{sem2GPA[0]["SEM2GPA"]},{cumulativeGPA[0]["CGPA"]}"
    return result




   
