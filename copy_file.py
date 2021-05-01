import numpy as np
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
    # population[15].days[2].sessions[0].display_Session()
    # population[15].days[2].sessions[1].display_Session()
    calculate_fitness(population)


def calculate_fitness(population):
    ### Your Code Here ####
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    fitness_values = []
    count_conflict = 0
    print("---------------")
    # print(STUDENT_GROUPS_GLOBAL)
    # print(TEACHERS_GLOBAL)
    print("---------------")

    for i, chromo in enumerate(population):
        count_conflict = 0
        for day in chromo.days:
            for session in day.sessions:
                print(session.overlapping_Students())
                count_conflict += session.overlapping_Students()
                count_conflict += session.overlapping_Teachers()
                session.display_Session()
            count_conflict += day.consecutive_Teachers()
        # print(count_conflict)
        if count_conflict == 0:
            fitness_values.append(1.0)
        else:
            fitness_values.append(1/count_conflict)
        print("Fitness of Chromosome {} = {}".format(i, fitness_values[-1]))


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
