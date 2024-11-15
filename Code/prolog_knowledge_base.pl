% Academic Probation Alert Python and Prolog Project. 
% Authors Dwayne Gibbs, Kemar Christie, Roberto James, Tyoni Davis.

/*
Function that accepts a list for the credits that each module has and the corresponding scre a student got and outputs back the
letter grade, gpa and grade point. grade point is credit x corresponding GPA.

Input : Credit [3,4,3,4 ] and [90,40,80,30] - score
Output: Letter Grade[A+,D-,A-,F] and GPA [4.00,1.8,3.67,1.5] and Grade Point Earned [12,7.2,11.01,6]

Function that adds all integers in a list
Sum of List [3,4,3,4]
Output = 14
*/

% Grade scale facts
grade_scale('A+', 4.3, 90.0, 100.0).
grade_scale('A', 4.0, 80.0, 89.99).
grade_scale('A-', 3.67, 75.0, 79.99).
grade_scale('B+', 3.33, 70.0, 74.99).
grade_scale('B', 3.0, 65.0, 69.99).
grade_scale('B-', 2.67, 60.0, 64.99).
grade_scale('C+', 2.33, 55.0, 59.99).
grade_scale('C', 2.0, 50.0, 54.99).
grade_scale('D+', 1.67, 45.0, 49.99).
grade_scale('D', 1.3, 40.0, 44.99).
grade_scale('U', 0.0, 0.0, 39.99).

% Detertime Letter Grade and Grade Point
score_to_grade(Score, LetterGrade, GradePoint) :-
    % Validate score is within possible range
    Score >= 0,
    Score =< 100,
    % Find matching grade scale
    grade_scale(LetterGrade, GradePoint, MinScore, MaxScore),
    Score >= MinScore,
    Score =< MaxScore.

% Add two numbers
add_numbers(Num1, Num2, Total) :-
    number(Num1),    % Verify first number
    number(Num2),    % Verify second number
    Total is Num1 + Num2.

% Divide two numbers
divide_numbers(Num1, Num2, Total) :-
    number(Num1),    % Verify first number
    number(Num2),    % Verify second number
    Num2 =\= 0,      % Check for division by zero
    Total is Num1 / Num2.


% Initial default GPA
default_gpa(2.0).

% Rule to update the default GPA
update_default_gpa(NewGPA) :-
    retract(default_gpa(_)),      % Remove the current default GPA
    assert(default_gpa(NewGPA)).  % Set the new default GPA

