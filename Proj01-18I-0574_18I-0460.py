import numpy
import pandas as pd
from random import randint
import collections
from copy import deepcopy
#-------------------------Classes-------------------------#


class Student:
    def __init__(self, name, courses1=None):
        self.name = name
        if courses1 is None:
            self.courses = []
        else:
            self.courses = courses1

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
        for student1 in grp1:
            for student2 in grp2:
                if student1.overlaps(student2):
                    return True
        return False

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

    def display_Student(self):
        print(self.name)
        print(self.courses)


class Session:
    def __init__(self):
        self.teachers = []
        self.courseIDs = []
        self.studentGroups = []
        self.duration = 3
        self.classRoomIDs = []
        self.num_exams = 0

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
        tester = Student("Tester")
        for i, grp1 in enumerate(self.studentGroups):
            for j, grp2 in enumerate(self.studentGroups):
                if i is not j:
                    if tester.groups_Overlap(grp1, grp2):
                        return True
        return False

    # Check whether a session has teachers that
    # have overlapping exams
    def overlapping_Teachers(self):
        if (len(set(self.teachers)) == len(self.teachers)):
            return False
        return True

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

    # Add only if 2 sessions not added already
    def add_Session(self, session):
        if (len(self.sessions) < self.max_ses):
            self.sessions.append(session)
            return True
        return False

    # Returns True if same teacher in 2 session on the same day
    def consecutive_Teachers(self):
        set1 = set(self.sessions[0].teachers)
        set2 = set(self.sessions[1].teachers)
        if (set1 & set2):
            return True
        return False


class Chromosome:
    max_days = 10

    def __init__(self, days=[]):
        self.days = days

    def add_Day(self, day):
        if (len(self.days) < 10):
            self.days.append(day)
            return True
        return False

    def duplicate_Exams(self):
        list_exam = []
        for day in self.days:
            for session in day.sessions:
                for exam in session.courseIDs:
                    list_exam.append(exam)
        if (len(set(list_exam)) == len(list_exam)):
            return False
        return True


#-------------------------Classes-------------------------#

# Remove duplicates except first instance row, using all columns
def remove_Dups(df, df_name):
    print("~~~~~~~~~")

    # Check if duplicated array empty
    if df[df.duplicated()].empty:
        print("No duplicates found for {}".format(df_name))

    # Else drop duplicates
    else:
        print("Duplicates found for {}. Removing them!".format(df_name))
        print(df[df.duplicated()])
        df.drop_duplicates(inplace=True)
    print(df)
    print("~~~~~~~~~\n\n")
    return df


def main():
    # No headers in csv files
    teachers = pd.read_csv('./teachers.csv', header=None, names=["Name"])
    courses = pd.read_csv('./courses.csv', header=None,
                          names=["Code", "Title"])
    studentNames = pd.read_csv(
        './studentNames.csv', header=None, names=["Name"])

    # Has a header, so including it
    studentCourse = pd.read_csv('./studentCourse.csv')
    # Rename the unnamed column
    studentCourse.rename(columns={'Unnamed: 0': 'Sr#'}, inplace=True)

    # Remove duplicates for all the pandas dataframes
    teachers = remove_Dups(teachers, "Teachers")
    courses = remove_Dups(courses, "Courses")
    studentNames = remove_Dups(studentNames, "Student Names")
    studentCourse = remove_Dups(studentCourse, "Student Course")

    print(studentCourse.drop_duplicates(['Course Code']))


#---------------------------------------------------------------#
TOTAL_POPULATION = 100
MAX_GENERATIONS = 300
CROSS_PROBABILITY = 0.0
MUTATION_PROBABILITY = 0.0
#---------------------------------------------------------------#


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


tester()
