import numpy as np
import random
from random import randint
import collections
from copy import deepcopy
from Chromosome_copy import *
import math

#---------------------------------------------------------------#
TOTAL_POPULATION = 100
MAX_GENERATIONS = 1000
CROSS_PROBABILITY = 0.9
MUTATION_PROBABILITY = 0.05
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
    # print("Fitness Calc")
    ### Your Code Here ####
    global STUDENT_GROUPS_GLOBAL
    global TEACHERS_GLOBAL
    global COURSES_GLOBAL
    fitness_values = []

    # Value of fitness in terms of exams per day
    # relativity = [0.1, 0.1, 0.5, 0.75, 0.8, 1, 1, 1, 0.8, 0.5, 0.5]
    relativity = [0.07, 0.5, 0.5, 0.6, 0.6,
                  0.4, 0.3, 0.001, 0.001, 0.001, 0.001]

    # -> Overlapping Students, Overlapping Teachers, Consecutive Teachers, Duplicate Exams
    # -> 100                   10                    10                    100

    for i, chromo in enumerate(population):
        overlap_student = 0
        overlap_teacher = 0
        consecutive_Students = 0
        consecutive_Teachers = 0
        chromo.remove_Empty_Days()
        FITNESS_CONSTANT = 1000
        for day in chromo.days:
            for session in day.sessions:
                overlap = session.overlapping_Students1()
                if overlap == True:
                    # FITNESS_CONSTANT -= 10
                    overlap_student += 2

                overlap = session.overlapping_Teachers()
                if overlap > 0:
                    FITNESS_CONSTANT -= 5
                    # overlap_teacher += 5
            overlap = day.consecutive_Students()
            if overlap > 0:
                consecutive_Students += 2
            overlap = day.consecutive_Teachers()
            if overlap > 0:
                consecutive_Teachers += 5
        MGbeforeCS = chromo.MG_before_CS()
        #print("MG before CS count students:",MGbeforeCS)        
        duplicate_Exams = chromo.duplicate_Exams()
        total_Exams = chromo.total_exams()
        total_Days = chromo.days_count
        remaining_Exams = len(COURSES_GLOBAL) - total_Exams

        if overlap_student > 0:
            FITNESS_CONSTANT -= overlap_student*20
        # if overlap_teacher > 0:
        #     FITNESS_CONSTANT -= 10
        if consecutive_Students > 0:
            FITNESS_CONSTANT -= 3
        # if consecutive_Teachers > 0:
            # FITNESS_CONSTANT -= 10
        if duplicate_Exams > 0:
            FITNESS_CONSTANT -= 40*duplicate_Exams
        if abs(remaining_Exams) > 0:
            FITNESS_CONSTANT -= 20*remaining_Exams
        if total_Days >= len(COURSES_GLOBAL)/2:
            FITNESS_CONSTANT -= 20*total_Days

        # fitness_values.append(1/conflicts)
        population[i].fitness = FITNESS_CONSTANT
        # print("Chromo {} with fitness {}".format(i, FITNESS_CONSTANT))
    for i, chromo in enumerate(population):
        population[i].index = i
    return population


def roulette_wheel_selection(population):
    # print("Wheel Sel")
    # population_copy = deepcopy(population)
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

def cross_Over(population):
    # print("Crossover")
    crossed_population = []
    global STUDENT_GROUPS_GLOBAL
    global COURSES_GLOBAL
    # dimensions = ["Day", "Session", "Student Group", "Teacher"]
    while len(crossed_population) < len(population):
        # print("Selecting Random In")
        parent_b = roulette_wheel_selection(population)
        parent_a = roulette_wheel_selection(population)
        # print("Selecting Random Out")
        if random.random() <= CROSS_PROBABILITY:
            # for i in range(len(population)):
            #     population[i].index = i
            # parent_b = roulette_wheel_selection(population)
            # parent_a = roulette_wheel_selection(population)
            # while (random_b == parent_a.index):
            #     random_b = randint(0, len(population)-1)
            # print("rand b:", random_b)

            # parent_b = population[random_b]
            # parent_b = roulette_wheel_selection(population)
            # print("Out of wheel")
            # print("parent b:", parent_b.index)
            pointer = randint(1, min(len(parent_a.days), len(parent_b.days)))

            for shift in range(pointer):
                parent_a.days[shift], parent_b.days[shift] = parent_b.days[shift], parent_a.days[shift]
            # print("Total exams:", population[parent_a.index].total_exams())
            # print("global length:", len(COURSES_GLOBAL))

            # if population[parent_a.index].total_exams() == len(COURSES_GLOBAL):
            #     # print("Resolving Conflicts in Crossover A")
            #     population[parent_a.index].resolve_Duplicates(
            #         STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)
            # if population[parent_b.index].total_exams() == len(COURSES_GLOBAL):
            #     # print("Resolving Conflicts in Crossover B")
            #     population[parent_b.index].resolve_Duplicates(
            #         STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)
            if len(crossed_population) < len(population):
                crossed_population.append(parent_a)
            if len(crossed_population) < len(population):
                crossed_population.append(parent_b)
        else:
            if len(crossed_population) < len(population):
                crossed_population.append(parent_a)
            if len(crossed_population) < len(population):
                crossed_population.append(parent_b)
        # print("DEEE Random In")
    for i in range(len(crossed_population)):
        crossed_population[i].index = i
    #prev_parent = parent_a
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
            #random_chromo = best_Schedule(population)
            #random_day1 = randint(0, new_chromo.days_count-1)
            random_day1 = randint(0, new_chromo.days_count-1)
            random_day2 = randint(0, chromo.days_count-1)

            # random_day3 = randint(0, chromo.days_count-1)
            # while random_day2 == random_day3:
            #     random_day3 = randint(0, chromo.days_count-1)

            # print("day1:", random_day1)
            # print("day2:", random_day2)
            # print("mutation")
            # temp_chromo = population[chromo.index].days[random_day2]
            # population[chromo.index].days[random_day2] = population[chromo.index].days[random_day3]
            # population[chromo.index].days[random_day3] = temp_chromo
            population[chromo.index].days[random_day2] = new_chromo.days[random_day1]
            if population[chromo.index].total_exams == len(COURSES_GLOBAL):
                print("Resolving Conflicts in mutation")
                population[chromo.index].resolve_Duplicates(
                    STUDENT_GROUPS_GLOBAL, COURSES_GLOBAL)

    return population


def best_Schedule(population):
    # print("Best Schedule")
    best = 0
    index = 0
    min_overlap = math.inf
    min_overlap_chromo = math.inf
    chromos = Chromosome()
    for i, chromo in enumerate(population):
        if chromo.fitness >= best:
            best = chromo.fitness
            min_overlap_chromo = min_overlap
            index = i
            chromos = chromo
    return chromos


def GA(population):
    print("MAX GENERATIONS: ", MAX_GENERATIONS)
    best_Chromo = None
    best_Chromo_list = []
    same_count = 0
    for i in range(MAX_GENERATIONS):
        # print("1 in")
        population = deepcopy(calculate_fitness(population))
        # if i == 0:
        #     parent_a = roulette_wheel_selection(population)
        #     prev_parent = parent_a
        # print("1 out")
        # print("Cross in")
        population = deepcopy(cross_Over(population))
        # print("Cross Out")
        population = deepcopy(calculate_fitness(population))
        # print("Cross out")
        # print("Best in")
        temp_best1 = best_Schedule(population)
        # print("Best Out")
        # print("Mutate In")
        population = deepcopy(mutate(population))
        # print("Mutate Out")
        population = deepcopy(calculate_fitness(population))
        temp_best = best_Schedule(population)
        if best_Chromo == None:
            best_Chromo = temp_best
        if best_Chromo.fitness < temp_best.fitness:
            best_Chromo = temp_best
        if best_Chromo.fitness < temp_best1.fitness:
            best_Chromo = temp_best1
        best_Chromo_list.append(best_Chromo)
        if i % 50 == 0:
            print("{} iterations passed".format(i))
            print("BEST SOLUTION AFTER {} ITERATIONS: ".format(
                i), best_Chromo.fitness)
            best_courses_list = []
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
            if len(best_Chromo_list) >2:
                if best_Chromo_list[-1] == best_Chromo_list[-2]:
                    same_count+=1
            else:
                same_count=0
            # if same_count>=100:
            #      population = deepcopy(mutate(population))

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
