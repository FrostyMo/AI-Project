import numpy
from random import randint
import collections
from copy import deepcopy
from Chromosome import *

#---------------------------------------------------------------#
TOTAL_POPULATION = 20
MAX_GENERATIONS = 300
CROSS_PROBABILITY = 0.0
MUTATION_PROBABILITY = 0.0
STUDENT_GROUPS_GLOBAL = {}
TEACHERS_GLOBAL = []
COURSES_GLOBAL = []
#---------------------------------------------------------------#

# Calculate Fitness of population

# Session -> Overlap
# Random Number -> student_groups -> random course -> replace
# ExamDuplication -> Remove Course


def main():
    courses_code_list, student_groups, teachers_list, class_IDs = create_Datasets()
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    STUDENT_GROUPS_GLOBAL = student_groups
    TEACHERS_GLOBAL = deepcopy(teachers_list)
    COURSES_GLOBAL = deepcopy(courses_code_list)
    population = []
    for i in range(TOTAL_POPULATION):
        population.append(populate(courses_code_list,
                                   student_groups, teachers_list, class_IDs))
    population[15].days[2].sessions[0].display_Session()
    population[15].days[2].sessions[1].display_Session()
    calculate_fitness(population)


def calculate_fitness(population):
    ### Your Code Here ####
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    fitness_value = 0.0
    print("---------------")
    # print(STUDENT_GROUPS_GLOBAL)
    # print(TEACHERS_GLOBAL)
    print("---------------")
    for i, chromo in enumerate(population):
        for j, days in enumerate(chromo.days):
            for k, session in enumerate(days.sessions):
                for l, student_group in enumerate(session.studentGroups):
                    # Remove student that is not enrolled in
                    # at least 3 courses
                    for student in student_group:
                        if not student.is_Valid:
                            population[i].days[j].sessions[k].studentGroups[l].remove(
                                student)
                            for key in STUDENT_GROUPS_GLOBAL:
                                STUDENT_GROUPS_GLOBAL[key].remove(student)

                # Replace exam that is overlapping with
                # student's courses
                for l, grp1 in enumerate(session.studentGroups):
                    for n, grp2 in enumerate(session.studentGroups):
                        if l is not n:
                            count = 0
                            while(Student("").groups_Overlap(grp1, grp2)):
                                random_course = COURSES_GLOBAL[randint(
                                    0, len(COURSES_GLOBAL)-1)]
                                random_group = STUDENT_GROUPS_GLOBAL[random_course]
                                if (count < 1000):
                                    population[i].days[j].sessions[k].studentGroups[n] = random_group
                                    population[i].days[j].sessions[k].courseIDs[n] = random_course
                                    grp2 = random_group
                                elif (count < 2000):
                                    population[i].days[j].sessions[k].studentGroups[l] = random_group
                                    population[i].days[j].sessions[k].courseIDs[l] = random_course
                                    grp1 = random_group
                                else:
                                    fitness_value -= 1
                                    break
                                # print(i, end=" ")
                                count += 1

                # Replace teachers who are duplicates in the session
                for l, teacher1 in enumerate(session.teachers):
                    for m, teacher2 in enumerate(session.teachers):
                        if l is not m:
                            while (teacher1 == teacher2):
                                random_teacher = TEACHERS_GLOBAL[randint(
                                    0, len(TEACHERS_GLOBAL))]
                                population[i].days[j].sessions[k].teachers[m] = random_teacher
                                teacher2 = random_teacher

            for k, session1 in enumerate(days.sessions):
                for l, session2 in enumerate(days.sessions):
                    if k is not l:
                        while (set(session1.teachers) & set(session2.teachers)):
                            random_teacher = TEACHERS_GLOBAL[randint(
                                0, len(TEACHERS_GLOBAL))]
                            random_int = randint(0, len(session2.teachers))
                            population[i].days[j].sessions[l].teachers[random_int] = random_teacher
                            session2.teachers[random_int] = random_teacher

    return population


def tester():
    student1 = Student("Shahnoor")
    courses1 = ["Math", "Science", "History"]
    student1.add_Courses(courses1)
    # student1.initialize_Courses(courses1)
    student1.display_Student()

    student2 = Student("Momin")
    courses2 = ["Islamiat", "CS", "PF"]
    student2.add_Courses(courses2)
    # student2.initialize_Courses(courses2)
    student2.display_Student()

    student3 = Student("Hello")
    courses3 = ["Yolo", "CS", "History"]
    student3.add_Courses(courses3)
    # student3.initialize_Courses(courses3)
    student3.display_Student()

    print(student1.overlaps(student2))
    print(student1.overlaps(student3))

    student_Group1 = [student1, student2, student3]
    student_Group2 = [student1, student2, student3]
    session1 = Session()
    session2 = Session()
    session3 = Session()
    session4 = Session()
    session1.add_to_Session("AR", "M11", student_Group1, "C01", 3)
    session1.add_to_Session("POOP", "H10", student_Group1, "C02", 3)
    session1.display_Session()

    session2.add_to_Session("AR1", "M12", student_Group1, "C01", 3)
    session2.add_to_Session("POOP", "H11", student_Group1, "C02", 3)
    session2.display_Session()

    session3.add_to_Session("AR", "M13", student_Group1, "C01", 3)
    session3.add_to_Session("POOP", "H12", student_Group1, "C02", 3)
    session3.display_Session()

    session4.add_to_Session("AR1", "M16", student_Group1, "C01", 3)
    session4.add_to_Session("POOP", "H19", student_Group1, "C02", 3)
    session4.display_Session()

    day1 = Day()
    day2 = Day()
    day1.add_Session(session1)
    day1.add_Session(session2)
    day2.add_Session(session3)
    day2.add_Session(session4)

    chromo = Chromosome()
    chromo.add_Day(day1)
    chromo.add_Day(day2)
    print("Grp overlap: ", Student("").groups_Overlap(
        student_Group1, student_Group2))
    print("Students overlap: ", session1.overlapping_Students())
    print("Teachers overlap: ", session1.overlapping_Teachers())

    print("Session Teachers Overlap: ", day1.consecutive_Teachers())
    print("Exam Duplication on days: ", chromo.duplicate_Exams())


# tester()
main()
