import numpy as np
import random
from random import randint
import collections
from copy import deepcopy
from Chromosome import *

#---------------------------------------------------------------#
TOTAL_POPULATION = 10
MAX_GENERATIONS = 300
CROSS_PROBABILITY = round(random.uniform(0.6, 1.0), 1)
MUTATION_PROBABILITY = round(random.uniform(0.0, 0.5), 1)
STUDENT_GROUPS_GLOBAL = {}
TEACHERS_GLOBAL = []
COURSES_GLOBAL = []
CLASS_IDS_GLOBAL = []
#---------------------------------------------------------------#


def main():
    courses_code_list, student_groups, teachers_list, class_IDs = create_Datasets()
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    global CLASS_IDS_GLOBAL
    STUDENT_GROUPS_GLOBAL = student_groups
    TEACHERS_GLOBAL = deepcopy(teachers_list)
    COURSES_GLOBAL = deepcopy(courses_code_list)
    CLASS_IDS_GLOBAL = deepcopy(class_IDs)
    population = []
    for i in range(TOTAL_POPULATION):
        population.append(populate(courses_code_list,
                                   student_groups, teachers_list, class_IDs))
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
    GA(population)


def calculate_fitness(population):
    ### Your Code Here ####
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    fitness_values = []
    count_conflict = 0
    # print("---------------")
    # print(STUDENT_GROUPS_GLOBAL)
    # print(TEACHERS_GLOBAL)
    print("---------------")

    # Value of fitness in terms of exams per day
    #relativity = [0.1, 0.1, 0.5, 0.75, 0.8, 1, 1, 1, 0.8, 0.5, 0.5]
    relativity = [1, 3, 0.3, 0.6, 0.5, 0.8, 0.2, 0.1, 0.1, 0.1, 0.1]
    #relativity =  [1, 1, 0.4, 5, 5, 6, 6, 1, 1, 1, 1]

    # -> Overlapping Students, Overlapping Teachers, Consecutive Teachers, Duplicate Exams
    # -> 100                   10                    10                    100

    for i, chromo in enumerate(population):
        count_conflict = 0
        total_exams = 0
        for day in chromo.days:
            for session in day.sessions:

                if session.overlapping_Students() > 10:
                    count_conflict += session.overlapping_Students()*2000

                count_conflict += session.overlapping_Teachers()

            count_conflict += day.consecutive_Teachers()*100
            total_exams += day.total_exams
        # print(count_conflict)
        if chromo.duplicate_Exams() > 0:
            count_conflict += chromo.duplicate_Exams() * 1000
        if count_conflict == 0:
            fitness_values.append(10000.0)
        else:
            fitness_values.append(1/count_conflict)
        # num_exams = 0
        # num_exams += chromo.days[0].total_exams
        # fitness_values[-1] *= relativity[num_exams]
        for day in chromo.days:
            num_exams = day.total_exams
            fitness_values[-1] *= relativity[num_exams]

        if (total_exams != len(COURSES_GLOBAL)):
            fitness_values[-1] *= 0.0001
        else:
            fitness_values[-1] += 100
        population[i].fitness = fitness_values[-1]
        population[i].index = i
        print("Fitness of Chromosome {} = {}, Exams Per Day: {}".format(
            i, fitness_values[-1], num_exams))
    for i, chromo in enumerate(population):
        population[i].index = i
    return population


def roulette_wheel_selection(population):
    population_copy = deepcopy(population)
    # Sum of fitnesses of population
    population_fitness = sum(
        [chromosome.fitness for chromosome in population_copy])

    # Probability = Chromo / (sum of fitnesses)
    chromosome_probabilities = [chromosome.fitness /
                                population_fitness for chromosome in population_copy]

    # Selects one chromosome randomly given the probabilities
    chromosome = np.random.choice(population_copy, p=chromosome_probabilities)
    # chromosome = population[randint(0, len(population)-1)]
    # print("The Chromo Selected has fitness: ", chromosome.fitness)
    return chromosome


def cross_Over(population):
    crossed_population = []
    global STUDENT_GROUPS_GLOBAL
    global COURSES_GLOBAL
    # dimensions = ["Day", "Session", "Student Group", "Teacher"]
    while len(crossed_population) < len(population):

        if randint(0, 100) <= CROSS_PROBABILITY * 100:
            # for i in range(len(population)):
            #     population[i].index = i
            random_b = randint(0, len(population)-1)
            parent_a = roulette_wheel_selection(population)
            # while (random_b == parent_a.index):
            #     random_b = randint(0, len(population)-1)
            # print("rand b:", random_b)

            # parent_b = population[random_b]
            parent_b = roulette_wheel_selection(population)
            # print("parent b:", parent_b.index)
            pointer = randint(1, min(len(parent_a.days), len(parent_b.days)))
            for shift in range(pointer):
                population[parent_a.index].days[shift], population[parent_b.index].days[
                    shift] = population[parent_b.index].days[shift], population[parent_a.index].days[shift]
            # if population[parent_a.index].total_exams() == len(COURSES_GLOBAL):
            #     print("Resolving Conflicts in Crossover A")
            #     population[parent_a.index].resolve_Duplicates(
            #         STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)
            # if population[parent_b.index].total_exams() == len(COURSES_GLOBAL):
            #     print("Resolving Conflicts in Crossover B")
            #     population[parent_b.index].resolve_Duplicates(
            #         STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)
            population_copy = deepcopy(population)
            crossed_population.append(population_copy[parent_a.index])
            crossed_population.append(population_copy[parent_b.index])
        # else:
        #     crossed_population.append(roulette_wheel_selection(population))
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
        if randint(0, 100) <= MUTATION_PROBABILITY * 100:
            new_chromo = populate(
                COURSES_GLOBAL, STUDENT_GROUPS_GLOBAL, TEACHERS_GLOBAL, CLASS_IDS_GLOBAL)
            random_day1 = randint(0, new_chromo.days_count-1)
            random_day2 = randint(0, chromo.days_count-1)
            # print("day1:", random_day1)
            # print("day2:", random_day2)

            population[chromo.index].days[random_day2] = new_chromo.days[random_day1]
            if population[chromo.index].total_exams == len(COURSES_GLOBAL):
                print("Resolving Conflicts in mutation")
                population[chromo.index].resolve_Duplicates(
                    STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)
    return population


def best_Schedule(population):
    best = 0

    for chromo in population:
        if chromo.fitness > best:
            best = chromo.fitness

    for chromo in population:
        if chromo.fitness == best:
            return chromo


def GA(population):
    print("MAX GENERATIONS: ", MAX_GENERATIONS)
    best_Chromo = None
    for i in range(30):
        population = deepcopy(calculate_fitness(population))
        population = deepcopy(cross_Over(population))
        population = deepcopy(mutate(population))
        population = deepcopy(calculate_fitness(population))
        temp_best = best_Schedule(population)
        if best_Chromo == None:
            best_Chromo = temp_best
        elif best_Chromo.fitness < temp_best.fitness:
            best_Chromo = temp_best

    print("BEST SOLUTION FOUND WITH FITNESS: ", best_Chromo.fitness)
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
    print("Courses duplicate: ", set(COURSES_GLOBAL) - set(best_courses))
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
