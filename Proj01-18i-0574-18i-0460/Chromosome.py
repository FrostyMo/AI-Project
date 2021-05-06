import numpy as np
import pandas as pd
from random import randint
import collections
from copy import deepcopy
#-------------------------GLOBALS-------------------------#
COURSES_BITS_GLOBAL = {}
STUDENTS_BITS_GLOBAL = {}
TEACHERS_BITS_GLOBAL = {}
CLASS_BITS_GLOBAL = {}
HARD_CONSTRAINTS = ["Students Overlap", "Teachers Overlap",
                    "Consecutive Teachers", "Duplicate Course", "Weekend", "All Courses"]
SOFT_CONSTRAINTS = ["Break on Friday",
                    "Consecutive Exam", "MG before CS", "Faculty Meeting"]
#---------------------------------------------------------#

#-------------------------Classes-------------------------#


class Student:
    def __init__(self, name, courses1=None):
        self.name = name
        if courses1 is None:
            self.courses = []
        else:
            self.courses = courses1
        self.studentID = None
        self.check_MGCS = []

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    # Add a course for the student
    def add_Course(self, course):
        self.courses.append(course)

    # Add a course for the student
    def add_Courses(self, courses1):
        for course in courses1:
            self.courses.append(course)

    # Add new courses together
    def initialize_Courses(self, courses1):
        self.courses = courses1

    # Compare names since unique
    def __eq__(self, student):
        return self.name == student.name

    # Return true if any course same for two students
    def overlaps(self, student):
        set1 = set(self.courses)
        set2 = set(student.courses)
        if (set1 & set2):
            return True
        return False

    # Check with 2 groups as @param
    def groups_Overlap(self, grp1, grp2):
        count_conflict = 0
        # for student1 in grp1:
        #     for student2 in grp2:
        #         if student1.name == student2.name:
        #             count_conflict += 1
        #             break
        student_list1 = []
        student_list2 = []
        for student1 in grp1:
            student_list1.append(student1.name)
        for student2 in grp2:
            student_list2.append(student2.name)

        count_conflict = len(
            set(student_list1).intersection(set(student_list2)))
        return count_conflict

    # Check if at least 3 courses assigned
    def is_Valid(self):
        if (len(self.courses) >= 3):
            return True
        return False

    # Check if at least 3 courses assigned to @param
    def is_Student_Valid(self, student):
        if (len(student.courses) >= 3):
            return True
        return False

    def student_To_Bits(self, bits):
        self.studentID = bits

    def display_Student(self):
        print(self.name, self.studentID)
        print(self.courses)


class Session:
    def __init__(self):
        self.teachers = []
        self.courseIDs = []
        self.studentGroups = []
        self.duration = 3
        self.classRoomIDs = []
        self.num_exams = 0
        self.sessionID = ""
        self.sessionBits = ""

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def session_To_Bits(self):
        for i, teacher in enumerate(self.teachers):
            self.sessionID += TEACHERS_BITS_GLOBAL[teacher]
            self.sessionBits += TEACHERS_BITS_GLOBAL[teacher]
            if i != len(self.teachers) - 1:
                self.sessionID += '_'
        self.sessionID += "-"
        for i, course in enumerate(self.courseIDs):
            self.sessionID += COURSES_BITS_GLOBAL[course]
            self.sessionBits += COURSES_BITS_GLOBAL[course]
            if i != len(self.courseIDs) - 1:
                self.sessionID += '_'
        self.sessionID += "-"
        for i, classs in enumerate(self.classRoomIDs):
            self.sessionID += CLASS_BITS_GLOBAL[classs]
            self.sessionBits += CLASS_BITS_GLOBAL[classs]
            if i != len(self.classRoomIDs) - 1:
                self.sessionID += '_'

    def add_to_Session(self, teacher, courseID, studentGroup, classRoomID, duration=3):
        self.teachers.append(teacher)
        self.courseIDs.append(courseID)
        self.studentGroups.append(studentGroup)
        self.duration = duration
        self.classRoomIDs.append(classRoomID)
        self.num_exams += 1

    # Check whether a session has student groups that
    # have overlapping exams
    def overlapping_Students(self):
        count_conflict = 0
        for i, grp1 in enumerate(self.studentGroups):
            for j, grp2 in enumerate(self.studentGroups):
                if j > i:
                    # print("grp overlap", tester.groups_Overlap(grp1, grp2))
                    count_conflict += Student("").groups_Overlap(grp1, grp2)

        return count_conflict

    def overlapping_Students1(self):
        count_conflict = 0
        grp1_names = []
        for grp1 in self.studentGroups:
            for grp in grp1:
                grp1_names.append(grp.name)

        if len(grp1_names) - len(set(grp1_names)) > 0:
            return True
        return False

    # Check whether a session has teachers that
    # have overlapping exams

    def overlapping_Teachers(self):
        return len(self.teachers) - len(set(self.teachers))

    def display_Session(self):
        print("+++++++++++++++++++++++++++++++")
        print("Teachers: ", self.teachers)
        print("Courses: ", self.courseIDs)
        for i, group in enumerate(self.studentGroups):
            print("Group {}:".format(i+1), end=" [ ")
            for student in group:
                print(student.name, end=" ")
            print("]", end=" ")
        print("")
        print("Class Rooms: ", self.classRoomIDs)
        print("Session Duration: {} Hours".format(self.duration))
        print("Total Exams: ", self.num_exams)
        print("+++++++++++++++++++++++++++++++")


# Day contains 2 sessions max
# Each session contains further schedule
class Day:
    max_ses = 2

    def __init__(self):
        self.sessions = []
        self.total_exams = 0
        self.dayID = ""
        self.dayBits = ""
        self.exam_list = []

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def day_To_Bits(self):
        if self.sessions is not None:
            self.dayID += "0-"
            self.dayBits += "0"
            self.sessions[0].session_To_Bits()
            self.dayID += self.sessions[0].sessionID
            self.dayBits += self.sessions[0].sessionBits
            if len(self.sessions) == 2:
                self.dayID += "-1-"
                self.dayBits += "1"
                self.sessions[1].session_To_Bits()
                self.dayID += self.sessions[1].sessionID
                self.dayBits += self.sessions[1].sessionBits

    # Add only if 2 sessions not added already
    def add_Session(self, session):
        if (len(self.sessions) < self.max_ses):
            self.sessions.append(session)
            self.exam_list.append(session.courseIDs)
            self.total_exams += session.num_exams
            return True
        return False

    # Returns True if same teacher in 2 session on the same day
    # set1 [sn, mo, AR, Abd, maaz]
    # set2 [Ali, Muntahim, sn, maaz]
    def consecutive_Teachers(self):
        set1 = set(self.sessions[0].teachers)
        set2 = set(self.sessions[1].teachers)
        return len(set1.intersection(set2))

    def consecutive_Students(self):
        ses1_grp = []
        ses2_grp = []
        for exam_grps in self.sessions[0].studentGroups:
            for grp in exam_grps:
                # print("grp",grp.name)
                # for g in grp:
                ses1_grp.append(grp.name)
        for exam_grps in self.sessions[1].studentGroups:
            for grp in exam_grps:
                # print("grp",grp.name)
                # for i in range(len(grp)):
                ses2_grp.append(grp.name)
        set1 = set(ses1_grp)
        set2 = set(ses2_grp)
        return len(set1.intersection(set2))

    def MG_before_CS(self):
        # for exam_grps in self.sessions[0].studentGroups:
        # for grp in exam_grps:

        pass


class Chromosome:
    max_days = 13

    def __init__(self, days=None):
        if days == None:
            self.days = []
        else:
            self.days = days
        self.days_count = 0
        self.fitness = 0
        self.index = 'a'
        self.chromoID = ""
        self.chromoBits = ""
        self.hard = {}
        self.soft = {}

        for cons in HARD_CONSTRAINTS:
            self.hard[cons] = "Not Violated"
        for cons in SOFT_CONSTRAINTS:
            self.soft[cons] = "Not Violated"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def chromo_To_Bits(self, pop_size):
        len_bits_pop = len(np.binary_repr(pop_size))
        len_bits_day = len(np.binary_repr(len(self.days)))
        index_binary = np.binary_repr(self.index, len_bits_pop)

        self.chromoID += index_binary + "-"
        self.chromoBits += index_binary
        for i, day in enumerate(self.days):
            days_binary = np.binary_repr(i, len_bits_day)
            day.day_To_Bits()
            self.chromoID += days_binary + "-" + day.dayID + "+"
            self.chromoBits += days_binary + day.dayBits

    def add_Day(self, day):
        if (len(self.days) < self.max_days):
            self.days.append(day)
            self.days_count += 1
            return True
        return False

    def remove_Empty_Days(self):
        for i, day in enumerate(self.days):
            # if (i % 5 != 0 or i % 6 != 0):
            if day.sessions[0].courseIDs is None and day.sessions[1].courseIDs is None:
                self.days.remove(day)
                self.days_count -= 1

    def duplicate_Exams(self):
        list_exam = []
        for day in self.days:
            for session in day.sessions:
                for exam in session.courseIDs:
                    list_exam.append(exam)
        return len(list_exam) - len(set(list_exam))

    # Returns index of session and courseID in that session
    def find_exam(self, day_index, exam):
        for i, session in enumerate(self.days[day_index].sessions):
            for j, exam1 in enumerate(session.courseIDs):
                if exam == exam1:
                    return i, j
        return -1, -1

    def total_exams(self):
        exams = sum(day.total_exams for day in self.days)
        return exams

    def resolve_Duplicates(self, STUDENT_GROUPS_GLOBAL, courses_list):
        list_exam = []
        set_exam = []
        for day in self.days:
            list_exam_day = []
            for session in day.sessions:
                for exam in session.courseIDs:
                    list_exam_day.append(exam)
                    set_exam.append(exam)
            list_exam.append(list_exam_day)

        set_exam = set(set_exam)
        count = 0
        missing_exams = list(set(courses_list) - set_exam)
        # print("Missing exams:", missing_exams)
        if len(missing_exams) == 0:
            return
        for i, exams_day in enumerate(list_exam):
            for j, exams_day2 in enumerate(list_exam):
                if j <= i:
                    continue
                if j > i and set(exams_day).intersection(set(exams_day2)) is not None:
                    for exam1 in (exams_day):
                        for exam2 in (exams_day2):
                            if exam1 == exam2 and count < len(missing_exams):
                                session_index, course_index = self.find_exam(
                                    j, exam2)
                                # print("HI: ", missing_exams[count])
                                self.days[j].sessions[session_index].courseIDs[course_index] = missing_exams[count]
                                self.days[j].sessions[session_index].studentGroups[course_index] = STUDENT_GROUPS_GLOBAL[missing_exams[count]]
                                count += 1

    def CS_before_MG(self):

        cs_before = True
        day_exams = {}
        for i, day in enumerate(self.days):
            list_exam_day = []
            for string in day.exam_list[0]:
                if "CS" in string:
                    cs_before = True
                list_exam_day.append(string)
            for string in day.exam_list[1]:
                if "MG" in string and cs_before == True:
                    return True
                list_exam_day.append(string)
            day_exams[i] = list_exam_day

        index = -1
        for i, key in enumerate(day_exams):
            for string in day_exams[key]:
                if "CS" in string:
                    cs_before = True
                    index = i
                if "MG" in string and cs_before and i > index:
                    return True
        return False


#-------------------------Classes-------------------------#

# Remove duplicates except first instance row, using all columns


def remove_Dups(df, df_name, col_name=None):
    print("~~~~~~~~~")

    # Check if duplicated array empty
    if df[df.duplicated()].empty:
        print("No duplicates found for {}".format(df_name))

    # Else drop duplicates
    else:
        print("Duplicates found for {}. Removing them!".format(df_name))
        if col_name is None:
            print(df[df.duplicated()])
            df.drop_duplicates(inplace=True)
        else:
            print(df[df.duplicated([col_name])])
            df.drop_duplicates([col_name], inplace=True)
    print(df)
    print("~~~~~~~~~\n\n")
    return df


def create_Datasets(student_file):
    global COURSES_BITS_GLOBAL
    global TEACHERS_BITS_GLOBAL
    global STUDENTS_BITS_GLOBAL
    global CLASS_BITS_GLOBAL
    # No headers in csv files
    teachers = pd.read_csv('./teachers.csv', header=None, names=["Name"])
    courses = pd.read_csv('./courses.csv', header=None,
                          names=["Code", "Title"])
    studentNames = pd.read_csv(
        './studentNames.csv', header=None, names=["Name"])

    # Has a header, so including it
    studentCourse = pd.read_csv(student_file)
    # Rename the unnamed column
    # studentCourse.rename(columns={'Unnamed: 0': 'Sr#'}, inplace=True)

    # Remove duplicates for all the pandas dataframes
    teachers = remove_Dups(teachers, "Teachers")
    courses = remove_Dups(courses, "Courses", "Code")
    studentNames = remove_Dups(studentNames, "Student Names")
    # studentCourse = remove_Dups(studentCourse, "Student Course")

    # print(studentCourse.drop_duplicates(['Course Code']))

    class_IDs = ["C01", "C02", "C03", "C04",
                 "C05", "C06", "C07", "C08", "C09", "C10"]
    courses_code_list = list(set(studentCourse['Course Code'].tolist()))
    # courses_title_list = courses['Title'].tolist()
    student_names_list = studentNames['Name'].tolist()
    teachers_list = teachers['Name'].tolist()

    student_groups = {}
    course_Bits = {}  # Dictionary for binary format for courses
    teacher_Bits = {}  # Dictionary for binary format for teachers
    class_Bits = {}  # Dictionary for binary format for classes
    for course in courses_code_list:
        student_groups[course] = []
        course_Bits[course] = None

    courses_length = len(courses_code_list)
    students_length = len(student_names_list)
    teachers_length = len(teachers_list)
    classes_length = len(class_IDs)

    binary_len_courses = len(np.binary_repr(courses_length))
    binary_len_students = len(np.binary_repr(students_length))
    binary_len_teachers = len(np.binary_repr(teachers_length))
    binary_len_classes = len(np.binary_repr(classes_length))
    for i, course in enumerate(courses_code_list):
        course_Bits[course] = np.binary_repr(i, binary_len_courses)
    for i, teacher in enumerate(teachers_list):
        teacher_Bits[teacher] = np.binary_repr(i, binary_len_teachers)

    for i, classs in enumerate(class_IDs):
        class_Bits[classs] = np.binary_repr(i, binary_len_classes)
    print(course_Bits)
    print(teacher_Bits)
    print(class_Bits)

    # Create Student() list
    Student_List = []
    for student in student_names_list:
        stud = Student(
            student, studentCourse['Course Code'].loc[studentCourse['Student Name'] == student].tolist())
        stud.student_To_Bits(np.binary_repr(i, binary_len_students))
        Student_List.append(stud)

    for student in Student_List:
        student.display_Student()

    for course in courses_code_list:
        # print(course)
        for student in Student_List:
            if course in student.courses:
                student_groups[course].append(student)
    COURSES_BITS_GLOBAL = course_Bits
    TEACHERS_BITS_GLOBAL = teacher_Bits
    CLASS_BITS_GLOBAL = class_Bits
    # for key in student_groups:
    #     print("Key {}: ".format(key))
    #     print("[", end="")
    #     for value in student_groups[key]:
    #         print("'{}".format(value.name), end="' ")
    #     print("]")
    # print("[", end="")
    # for value in student_groups['CG']:
    #     print("'{}".format(value.name), end="' ")
    # print("]")
    # print(len(student_groups['CG']))
    # print(student_groups['OOP'])
    return courses_code_list, student_groups, teachers_list, class_IDs, student_names_list


def populate(courses_code_list, student_Groups, teachers, classIDs):
    # Span exams over 5 days
    # exams_per_day = int(len(courses_code_list)/5)
    N = len(courses_code_list)
    a = np.arange(0, N)
    b = np.random.choice(a, N, replace=False)
    # print(b)
    # print(len(b))
    courses_random_list = []
    for i in range(N):
        courses_random_list.append(courses_code_list[b[i]])

    # print(courses_random_list)

    exams_per_day = randint(1, 4)
    # print('{}---------------------'.format(exams_per_day))
    i = 0
    count = 0
    days = []
    while (i < len(courses_random_list)):
        # print(courses_random_list[i:i+exams_per_day])
        my_list = courses_random_list[i:i+exams_per_day]
        my_list_copy = deepcopy(my_list)
        session1 = Session()
        session2 = Session()
        for j in range(int(exams_per_day/2)):
            my_list_size = len(my_list_copy)
            adder = 0
            if j < my_list_size:  # 0  4, 1   5, 2   6, 3   7,
                session1.add_to_Session(teachers[randint(
                    0, len(teachers)-1)], my_list_copy[j], student_Groups[my_list_copy[j]], classIDs[count], 3)
            if j+int(exams_per_day/2) < my_list_size:
                adder = j+int(exams_per_day/2)
                session2.add_to_Session(teachers[randint(
                    0, len(teachers)-1)], my_list_copy[adder], student_Groups[my_list_copy[adder]], classIDs[count], 3)
            count += 1
            if exams_per_day % 2 != 0 and j == int(exams_per_day/2)-1 and j+int(exams_per_day/2)+1 < my_list_size:
                session1.add_to_Session(teachers[randint(
                    0, len(teachers)-1)], my_list_copy[j+int(exams_per_day/2)+1], student_Groups[my_list_copy[j+int(exams_per_day/2)+1]], classIDs[count], 3)

        day = Day()
        day.add_Session(session1)
        day.add_Session(session2)
        days.append(day)
        i += exams_per_day
        count = 0
    chromo = Chromosome()
    for i, day in enumerate(days):
        chromo.add_Day(day)
        # print("Day# {}:".format(i))
        # print("Session 1:")
        # day.sessions[0].display_Session()
        # print("\nSession 2:")
        # day.sessions[1].display_Session()
    return chromo
