import numpy
import pandas as pd
from random import randint
import collections


class Student:
    def __init__(self, name, courses=[]):
        self.name = name
        self.courses = courses

    # Add a course for the student
    def add_Course(self, course):
        courses.append(course)

    # Compare names since unique
    def __eq__(self, student):
        return self.name == student.name

    # Return true if any course same for two students
    def overlaps(self, student):
        set1 = set(self.courses)
        set2 = set(student.courses)
        return set1 and set2

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


class Session:
    def __init__(self, teachers=[], courseIDs=[], studentGroups=[],  classRoomIDs=[], duration=3):
        self.teachers = teachers
        self.courseIDs = courseIDs
        self.studentGroups = studentGroups
        self.duration = duration
        self.classRoomIDs = classRoomIDs
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
    def is_Valid(self):
        tester = Student("Tester")
        for grp1 in self.studentGroups:
            for grp2 in self.studentGroups:
                if grp1 is not grp2:
                    if tester.groups_Overlap(grp1, grp2):
                        return False
        return True


# Day contains 2 sessions max
# Each session contains further schedule
class Day:
    max = 2

    def __init__(self, sessions=[]):
        self.sessions = sessions

    # Add only if 2 sessions not added already
    def add_Session(self, session):
        if (len(self.sessions) < max):
            self.sessions.append(session)
            return True
        return False


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


# No headers in csv files
teachers = pd.read_csv('./teachers.csv', header=None, names=["Name"])
courses = pd.read_csv('./courses.csv', header=None, names=["Code", "Title"])
studentNames = pd.read_csv('./studentNames.csv', header=None, names=["Name"])

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
