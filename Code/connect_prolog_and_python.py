import pyswip
from pyswip import Prolog


# Load the Prolog file
prolog = pyswip.Prolog()

def consult_prolog():
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




   
'''
sem1Credit=[3,3,4,4,3,2,1]
sem1Grade =[75,50,70,55,40,65,85]
sem2Credit=[]
sem2Grade =[]
consult_prolog()
result=process_student_grades(sem1Credit,sem1Grade,sem2Credit,sem2Grade)
print(result)


consult_prolog()
print("default : " + str(get_default_gpa()))
update_default_gpa(3.0)
print("default : " + str(get_default_gpa()))

'''