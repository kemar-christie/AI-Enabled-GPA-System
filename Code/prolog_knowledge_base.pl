% Academic Probation Alert Python and Prolog Project. 
% Authors Dwayne Gibbs, Kemar Christie, Roberto James, Tyoni Davis.

:- dynamic default_gpa/1.  % Declare the default_gpa as dynamic

% Accepts a list for the credits that each module has and the corresponding score a student got and outputs back the letter grade, gpa and grade point. grade point is credit x corresponding GPA.
process_grades([], [], [], [], []).
process_grades([Credit|Credits], [Score|Scores], [Letter|Letters], [GPA|GPAs], [Point|Points]) :-
    % Get letter grade and GPA for current score
    score_to_grade(Score, Letter, GPA),
    % Calculate grade point (credit × GPA)
    Point is Credit * GPA,
    % Process rest of the lists
    process_grades(Credits, Scores, Letters, GPAs, Points).

% Calculate cumulative GPA with result formatted to 2 decimal places
calculate_cumulative_gpa(Credits1, Scores1, Credits2, Scores2, FormattedGPA) :-
    % Calculate total points and credits for each semester
    process_grades(Credits1, Scores1, _, _, GradePoints1),
    process_grades(Credits2, Scores2, _, _, GradePoints2),
    sum_list(GradePoints1, TotalPoints1),
    sum_list(GradePoints2, TotalPoints2),
    sum_list(Credits1, TotalCredits1),
    sum_list(Credits2, TotalCredits2),
    % Calculate cumulative GPA
    TotalPoints is TotalPoints1 + TotalPoints2,
    TotalCredits is TotalCredits1 + TotalCredits2,
    TotalCredits > 0,
    % Calculate raw GPA
    RawGPA is TotalPoints / TotalCredits,
    % Format to 2 decimal places
    FormattedGPA is round(RawGPA * 100) / 100.

% Calculate semester GPA with result formatted to 2 decimal places
calculate_semester_gpa(Credits, Scores, FormattedGPA) :-
    % Process all grades
    process_grades(Credits, Scores, _, _, GradePoints),
    % Sum up total grade points and credits
    sum_list(GradePoints, TotalPoints),
    sum_list(Credits, TotalCredits),
    % Verify credits total is greater than zero
    TotalCredits > 0,
    % Calculate raw GPA
    RawGPA is TotalPoints / TotalCredits,
    % Format to 2 decimal places
    FormattedGPA is round(RawGPA * 100) / 100.

% Adds all integers in a list
% Base case: empty list has sum of 0
sum_list([], 0).
% Case for single element list: sum is just that element
sum_list([Single], Single).
% Recursive case for lists with more than one element
sum_list([Head|Tail], Sum) :-
    sum_list(Tail, TailSum),
    Sum is Head + TailSum.


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

% Check academic probation function maybe needed



/*
% Process grades for a semester:
?- process_grades([3,4,3,4], [90,40,80,30], Letters, GPAs, Points).

% Calculate semester GPA:
?- calculate_semester_gpa([3,4,3,4], [90,40,80,30], GPA).

% Calculate cumulative GPA:
?- calculate_cumulative_gpa([3,4], [90,80], [3,4], [70,60], CGPA).


test case 
calculate_cumulative_gpa([3,3,4,4,3,2,1],[75,50,70,55,40,65,85], [1,4,3,4,2], [90,75,65,70,80], CGPA).
calculate_cumulative_gpa([3,3,4,4,3,2,1],[75,50,70,55,40,65,85], [3,3,4,4,3,2,1],[75,50,70,55,40,65,85], CGPA).
calculate_cumulative_gpa([3,3,4,4,3,2,1],[75,50,70,55,40,65,85], [], [], CGPA).
*/