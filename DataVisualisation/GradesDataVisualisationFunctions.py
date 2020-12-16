import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Functions

#1. A function to show how much percentage of students got a particular grade for the given subject 
def GradeDistribution ( subcode ):
    grades = df.loc[df['subno'] == subcode]
    grades = grades[{'grade'}]
    plt.figure(figsize = (5,5))
    labels = ["AA", "AB", "BB", "BC", "CC", "CD", "DD", "F"]
    value = grades.groupby('grade').size()
    plt.pie(value, labels = labels, autopct = "%.1f%%")
    
#2. A function to show what subjects are available for a given branch in a given sem with their credits  
def SubjectWeightage ( semno, branch ):
    tsem = allsem[semno]
    tsem = tsem.loc[tsem[branch] == 1]
    tsub = tsem.iloc[:,0].values
    y_pos = np.arange(start =0,stop= 3*len(tsub),step = 3)
    wt = tsem.iloc[:,2].values
    plt.barh(y_pos, wt, align='center', alpha=0.5)
    plt.yticks(y_pos, tsub)
    plt.xlabel('Credits')
    plt.title('Subject Weightage for Sem {} for Branch {}'.format(semno, branch))
    plt.show()

#3. A function to show the result of a given sem showing grades in all the subjects for the sem for a given rollno
def SemResult( rollno, semno ):
    result = df.loc[ df['rollno'] == rollno]
    result = result.loc[result['semno'] == semno] 
    points = {"AA": 10, "AB": 9, "BB": 8, "BC" : 7, "CC" : 6, "CD" : 5, "DD": 4, "F": 0}
    grade = result['subno']  
    y_pos = np.arange(start =0,stop= 3*len(grade),step = 3)
    result['point'] = 1
    for i in result.index:
        result['point'][i] = points[result['grade'][i]]
    height = result['point']
    plt.bar(y_pos, height, align='center', alpha=0.5)
    plt.xticks(y_pos, grade)
    plt.ylabel('GradePoint')
    plt.title('Result of Sem {} ({})'.format(semno, rollno))
    plt.show()

#4. A function to show the result of a given rollno in all sems showing SPIs of all sems 
def AllSemsSpi( rollno ):
    locroll = df.loc[ df['rollno'] == rollno]
    points = {"AA": 10, "AB": 9, "BB": 8, "BC" : 7, "CC" : 6, "CD" : 5, "DD": 4, "F": 0}
    
    spi = {}
    for i in range(1, 9):
        rslt = locroll.loc[locroll['semno'] == i] 
        rslt = rslt[['subno','crd','grade']] 
        rslt['points'] = 1
        sm = 0
        tot = 0
        for j in rslt.index:
            rslt['points'][j] = points[rslt['grade'][j]]
            sm = sm + rslt['crd'][j]
            tot = tot + rslt['points'][j]*rslt['crd'][j]
        spi[i] = tot/sm
 
    y_pos = np.arange(start = 0, stop = 24, step = 3)
    height = []
    smno = []
    for i in range(1, 9):
        height.append(spi[i])
        smno.append(i)
    plt.bar(y_pos, height, align='center', alpha=0.5)
    plt.xticks(y_pos, smno)
    plt.ylabel('SPI')
    plt.title('Result ({})'.format(rollno))
    plt.show()

# Dataframes to be used in functions
df = pd.read_csv('ori_grades_data.csv')

allsem = {}

for i in range(1,9):
    sem = df.loc[df['semno'] == i]
    sem['branch'] = sem.rollno.str.slice(start=4, stop=6, step=1)
    sem = sem.drop_duplicates(['subno','branch'])
    sem = sem[['subno','sub_type','crd','branch']]
    sem = pd.concat([sem,pd.get_dummies(sem['branch'])],axis=1)
    for col in sem.columns[4:]:
        sem[col].values[:] = 0 
    
    for ind in sem.index:
        sub = sem['subno'][ind]
        br = sem['branch'][ind]
        for jnd in sem.index:
            if sem['subno'][jnd] == sub:
                sem[br][jnd] = 1
                
    sem = sem.drop_duplicates('subno')
    sem = sem.reset_index()
    sem = sem.drop(['branch', 'index'],axis=1)

    #Created dictionary to store sem-wise subject info
    allsem[i] = sem 


# Function Calls
subcode = "MA101"
#GradeDistribution(subcode)

semno = 4
branch = "EE"
#SubjectWeightage(semno, branch)

rollno = "1401CS20"
semno = 4
#SemResult( rollno, semno )

rollno = "1401CS20"
#AllSemsSpi(rollno)


