import numpy
import pandas as pd


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
