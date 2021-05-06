import numpy as np
import random
from random import randint
import collections
from copy import deepcopy, copy
from Chromosome import *
import math

# ********************* UNI'S DATASET ********************* #

#---------------------------------------------------------------#
TOTAL_POPULATION = 100
MAX_GENERATIONS = 1000
CROSS_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.05
STUDENT_GROUPS_GLOBAL = {}
TEACHERS_GLOBAL = []
COURSES_GLOBAL = []
CLASS_IDS_GLOBAL = []
STUDENT_LIST_GLOBAL = []
#---------------------------------------------------------------#


def main():
    file_name = './studentCourse.csv'
    courses_code_list, student_groups, teachers_list, class_IDs, student_names_list = create_Datasets(
        file_name)
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    global CLASS_IDS_GLOBAL
    global STUDENT_LIST_GLOBAL
    STUDENT_GROUPS_GLOBAL = student_groups
    TEACHERS_GLOBAL = deepcopy(teachers_list)
    COURSES_GLOBAL = deepcopy(courses_code_list)
    CLASS_IDS_GLOBAL = deepcopy(class_IDs)
    STUDENT_LIST_GLOBAL = deepcopy(student_names_list)
    population = []
    for i in range(TOTAL_POPULATION):
        population.append(populate(courses_code_list,
                                   student_groups, teachers_list, class_IDs))
        population[i].index = i
        population[i].chromo_To_Bits(TOTAL_POPULATION)
        print("CHROMO {} = {}\n\n".format(i, population[i].chromoBits))
        if i == 99:
            print("Teachers Size: ", len(
                population[i].days[0].sessions[0].teachers) + len(population[i].days[0].sessions[1].teachers))
    # population[15].days[2].sessions[0].display_Session()
    # population[15].days[2].sessions[1].display_Session()
    # for i in range(10):
        # population = calculate_fitness(population)
        # # roulette_wheel_selection(population)
        # population = deepcopy(cross_Over(population))
        # # for chromo in population:
        # #     for day in chromo.days:
        # #         print(day.sessions[0].teachers)
        # #         print(day.sessions[1].teachers)
        # #population = calculate_fitness(population)

        # mutate(population)
        # population = calculate_fitness(population)
    # print(HARD_CONSTRAINTS)
    # print(SOFT_CONSTRAINTS)
    GA(population)


def calculate_fitness(population):
    # print("Fitness Calc")
    ### Your Code Here ####
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    global STUDENT_LIST_GLOBAL
    # fitness_values = []

    # Value of fitness in terms of exams per day
    relativity = [0.1, 0.1, 0.5, 0.75, 0.8, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01]
    # relativity = [0.07, 0.5, 0.5, 0.6, 0.6,
    #               0.4, 0.3, 0.001, 0.001, 0.001, 0.001]

    # -> Overlapping Students, Overlapping Teachers, Consecutive Teachers, Duplicate Exams
    # -> 100                   10                    10                    100

    for i, chromo in enumerate(population):
        overlap_student = 0
        overlap_teacher = 0
        consecutive_Students = False
        consecutive_Teachers = 0
        weekend_days = 0
        population[i].remove_Empty_Days()
        chromo.remove_Empty_Days()
        FITNESS_CONSTANT = 100000.0
        csBeforemg = 0
        # total_Conflicts = 0
        for j, day in enumerate(chromo.days):
            for session in day.sessions:

                overlap = session.overlapping_Students1()
                # print("Students overlap:", overlap)
                if overlap == True:
                    overlap_student += 2

                overlap = session.overlapping_Teachers()
                if overlap > 0:
                    # print("T")
                    overlap_teacher += overlap

                if (j+1) % 8 == 0 or (j+1) % 9 == 0:
                    if session.courseIDs is not None:
                        weekend_days += 2
            overlap = day.consecutive_Students()
            if overlap > 0:
                consecutive_Students += 2

            overlap = day.consecutive_Teachers()
            if overlap > 0:
                consecutive_Teachers += 5

        duplicate_Exams = chromo.duplicate_Exams()
        total_Exams = chromo.total_exams()
        total_Days = chromo.days_count
        remaining_Exams = len(COURSES_GLOBAL) - total_Exams + duplicate_Exams

        # print("Rems: ", remaining_Exams)
        if chromo.CS_before_MG() == False:
            # print("CS before MG")
            population[i].soft["MG before CS"] = "Not Violated"

        else:
            FITNESS_CONSTANT -= 5
            population[i].soft["MG before CS"] = "Violated"
        if overlap_student > 0:
            population[i].hard["Students Overlap"] = "Violated"
        if overlap_student > 12:
            # print("OS")
            FITNESS_CONSTANT -= overlap_student*50
        else:
            population[i].hard["Students Overlap"] = "Not Violated"

        if overlap_teacher > 0:
            # print("ttt")
            population[i].hard["Teachers Overlap"] = "Violated"
            FITNESS_CONSTANT -= 10
        else:
            population[i].hard["Teachers Overlap"] = "Not Violated"

        if weekend_days > 0:
            population[i].hard["Weekend"] = "Violated"
            FITNESS_CONSTANT -= weekend_days*30
        else:
            population[i].hard["Weekend"] = "Not Violated"

        if consecutive_Students > 0:
            population[i].soft["Consecutive Exam"] = "Violated"
            FITNESS_CONSTANT -= consecutive_Students
        else:
            population[i].soft["Consecutive Exam"] = "Not Violated"

        if consecutive_Teachers > 0:
            # print(" c t")
            population[i].hard["Consecutive Teachers"] = "Violated"
            FITNESS_CONSTANT -= 10
        else:
            population[i].hard["Consecutive Teachers"] = "Not Violated"
        if duplicate_Exams > 0:
            # print("dup")
            population[i].hard["Duplicate Course"] = "Violated"
            FITNESS_CONSTANT -= 50*duplicate_Exams
        else:
            population[i].hard["Duplicate Course"] = "Not Violated"
        if remaining_Exams > 0:
            # print("r")
            population[i].hard["All Courses"] = "Violated"
            FITNESS_CONSTANT -= 50*remaining_Exams
        else:
            population[i].hard["All Courses"] = "Not Violated"
        # if total_Days >= len(COURSES_GLOBAL)/2:
        #     FITNESS_CONSTANT -= total_Days*5
        # for day in chromo.days:
        #     FITNESS_CONSTANT *= relativity[day.total_exams]
        population[i].fitness = FITNESS_CONSTANT
        # print("Chromo {} with fitness {}".format(i, FITNESS_CONSTANT))
    for i, chromo in enumerate(population):
        population[i].index = i
    return population


def roulette_wheel_selection(population):
    # print("Wheel Sel")

    # Sum of fitnesses of population
    population_fitness = sum(
        [chromosome.fitness for chromosome in population])
    # pick = random.uniform(0, population_fitness)
    # Probability = Chromo / (sum of fitnesses)
    chromosome_probabilities = [chromosome.fitness /
                                population_fitness for chromosome in population]

    # Selects one chromosome randomly given the probabilities
    chromosome = np.random.choice(population, p=chromosome_probabilities)

    # range_list = []
    # range_list.append(0.0)
    # for prob in chromosome_probabilities:
    #     range_list.append(float(range_list[-1]+prob))
    # rand_num = random.random()
    # for i, value in enumerate(range_list):

    #     if range_list[i-1] < rand_num and rand_num <= value:
    #         return population[i-1]

    # chromosome = population[3]
    # print("The Chromo Selected has fitness: ", chromosome.fitness)
    return chromosome


def cross_Over(population, list_best):
    # print("Crossover")
    crossed_population = []
    global STUDENT_GROUPS_GLOBAL
    global COURSES_GLOBAL

    for i, chromo in enumerate(list_best):
        if i < 4:
            crossed_population.append(chromo)
    # dimensions = ["Day", "Session", "Student Group", "Teacher"]
    while len(crossed_population) < len(population):
        random_b = randint(0, len(population)-1)
        parent_b = population[random_b]
        parent_a = roulette_wheel_selection(population)

        if random.random() <= CROSS_PROBABILITY:
            pointer = randint(1, min(len(parent_a.days), len(parent_b.days)))

            for shift in range(pointer):
                parent_a.days[shift], parent_b.days[shift] = parent_b.days[shift], parent_a.days[shift]

            if len(crossed_population) < len(population):
                crossed_population.append(parent_a)
            if len(crossed_population) < len(population):
                crossed_population.append(parent_b)
        else:
            if len(list_best) > 0:
                if len(crossed_population) < len(population):
                    crossed_population.append(
                        list_best[randint(0, len(list_best)-1)])
            elif len(crossed_population) < len(population):
                crossed_population.append(parent_a)
        # print("DEEE Random In")
    for i in range(len(crossed_population)):
        crossed_population[i].index = i

    return crossed_population


def mutate(population):

    # mutate_population = []
    global COURSES_GLOBAL
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global CLASS_IDS_GLOBAL

    for chromo in population:
        if random.random() <= MUTATION_PROBABILITY:
            new_chromo = populate(
                COURSES_GLOBAL, STUDENT_GROUPS_GLOBAL, TEACHERS_GLOBAL, CLASS_IDS_GLOBAL)
            random_day1 = randint(0, new_chromo.days_count-1)
            random_day2 = randint(0, chromo.days_count-1)
            # print("day1:", random_day1)
            # print("day2:", random_day2)
            # print("mutation")
            population[chromo.index].days[random_day2] = new_chromo.days[random_day1]

    return population


def best_Schedule(population):
    # print("Best Schedule")
    best = 0
    chromos = []
    index = 0
    for i, chromo in enumerate(population):
        if chromo.fitness >= best:
            best = chromo.fitness
            index = i
    best_chromo = None
    for chromo in population:
        if chromo.fitness == best:
            chromos.append(chromo)
            if best_chromo == None:
                best_chromo = chromo

    return best_chromo, chromos


def GA(population):
    print("MAX GENERATIONS: ", MAX_GENERATIONS)
    best_Chromo = None
    list_best = []
    for i in range(MAX_GENERATIONS):

        # population = deepcopy(calculate_fitness(population))
        population = deepcopy(calculate_fitness(population))
        population = deepcopy(cross_Over(population, list_best))
        # population = cross_Over(population, list_best)

        population = deepcopy(mutate(population))
        # population = mutate(population)

        # population = deepcopy(calculate_fitness(population))
        population = deepcopy(calculate_fitness(population))
        temp_best, list_best_temp = best_Schedule(population)
        if best_Chromo == None:
            best_Chromo = temp_best
            list_best = list_best_temp
        if best_Chromo.fitness < temp_best.fitness:
            best_Chromo = temp_best
            list_best = list_best_temp
        # if best_Chromo.fitness < temp_best1.fitness:
        #     best_Chromo = temp_best1
        if i % 50 == 0:
            print("{} iterations passed".format(i))
            print("BEST SOLUTION AFTER {} ITERATIONS: ".format(
                i), best_Chromo.fitness)
            best_courses_list = []
            remaining_Exams = len(
                COURSES_GLOBAL) - best_Chromo.total_exams() + best_Chromo.duplicate_Exams()
            print("Remaining Exams: ", remaining_Exams)
            print("Total Days:", len(best_Chromo.days))
            print("HARD CONSTRAINTS\n", best_Chromo.hard)
            print("SOFT CONSTRAINTS\n", best_Chromo.soft)
            for j, day in enumerate(best_Chromo.days):
                print("Day {}...\nSession 1:".format(j+1))
                print(day.sessions[0].courseIDs)
                best_courses_list.append(day.sessions[0].courseIDs)
                best_courses_list.append(day.sessions[1].courseIDs)
                print(day.sessions[0].teachers)
                print("Student_Overlap: ",
                      day.sessions[0].overlapping_Students())

                print("Session 2:")
                print(day.sessions[1].courseIDs)
                print(day.sessions[1].teachers)
                print("Student_Overlap: ",
                      day.sessions[1].overlapping_Students())

            best_courses = []
            for list_exam in best_courses_list:
                for exam in list_exam:
                    best_courses.append(exam)
            print("Courses Remaining: ", set(
                COURSES_GLOBAL) - set(best_courses))
            print("Best Courses: ", sorted(best_courses))
            print("Total: ", best_Chromo.total_exams())

    print("BEST SOLUTION FOUND WITH FITNESS: ", best_Chromo.fitness)
    print("And duplicate exams: ", best_Chromo.duplicate_Exams())
    print("Total Days:", len(best_Chromo.days))
    best_courses_list = []
    for i, day in enumerate(best_Chromo.days):
        print("Day {}...\nSession 1:".format(i+1))
        print(day.sessions[0].courseIDs)
        best_courses_list.append(day.sessions[0].courseIDs)
        best_courses_list.append(day.sessions[1].courseIDs)
        print(day.sessions[0].teachers)
        print("Student_Overlap: ", day.sessions[0].overlapping_Students())
        print("Session 2:")
        print(day.sessions[1].courseIDs)
        print(day.sessions[1].teachers)
        print("Student_Overlap: ", day.sessions[1].overlapping_Students())

    best_courses = []
    for list_exam in best_courses_list:
        for exam in list_exam:
            best_courses.append(exam)
    print("Courses Remaining: ", set(COURSES_GLOBAL) - set(best_courses))
    print("Best Courses: ", sorted(best_courses))
    return best_Chromo


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


# Day 1...
# Session 1:
# ['CS218', 'DS3011']
# ['Sajid Khan', 'Zainab Abaid']
# Student_Overlap:  6
# Session 2:
# ['CS302']
# ['Farah Jabeen Awan']
# Student_Overlap:  0
# Day 2...
# Session 1:
# ['AI2011', 'SS113']
# ['Usman Ashraf', 'Asif Naeem']
# Student_Overlap:  6
# Session 2:
# ['EE227']
# ['Sehrish Hassan']
# Student_Overlap:  0
# Day 3...
# Session 1:
# ['SE110', 'SS118']
# ['Aqeel Shahzad', 'Hassan Mustafa']
# Student_Overlap:  5
# Session 2:
# ['CS328']
# ['Subhan Ullah']
# Student_Overlap:  0
# Day 4...
# Session 1:
# ['SS111', 'CS118']
# ['Sanaa Ilyas', 'Shehreyar Rashid']
# Student_Overlap:  4
# Session 2:
# ['CS220']
# ['Sidra Khalid']
# Student_Overlap:  0
# Day 5...
# Session 1:
# ['CY2012', 'SS152']
# ['Muhammad Usman', 'Nagina Safdar']
# Student_Overlap:  1
# Session 2:
# ['CS307']
# ['Muhammad Usman']
# Student_Overlap:  0
# Day 6...
# Session 1:
# ['MT205', 'MG220']
# ['Farwa Batool', 'Aqeel Shahzad']
# Student_Overlap:  7
# Session 2:
# ['CS219']
# ['Gul e Aisha']
# Student_Overlap:  0
# Day 7...
# Session 1:
# ['CS217', 'EE229']
# ['Shafaq Riaz', 'Maimoona Rassol']
# Student_Overlap:  3
# Session 2:
# ['CS211']
# ['Kifayat Ullah']
# Student_Overlap:  0
# Day 8...
# Session 1:
# ['MT224']
# ['Sidra Khalid']
# Student_Overlap:  0
# Session 2:
# ['MG223']
# ['Adnan Tariq']
# Student_Overlap:  0
