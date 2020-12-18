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
    plt.show()
    
#2. A function to show what subjects are available for a given branch in a given sem with their credits  
def SubjectWeightage ( semno, branch ):
    tsem = allsem[semno]
    tsem = tsem.loc[tsem[branch] == 1]
    tsub = tsem.iloc[:,0].values
    colour = []
    for i in range(len(tsub)):
        colour.append ((np.random.rand(),np.random.rand(), np.random.rand()))
    y_pos = np.arange(start =0,stop= 3*len(tsub),step = 3)
    wt = tsem.iloc[:,2].values
    for i in range(len(y_pos)):
        plt.barh(y_pos[i], wt[i], height = 1.5, align='center', alpha=0.5, color = colour[i])
    plt.yticks(y_pos, tsub, color = 'purple')
    plt.xlabel('Credits')
    plt.ylabel('Course')
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
    colour = []
    for i in range(len(grade)):
        colour.append ((np.random.rand(),np.random.rand(), np.random.rand()))
    heights = height.values
    
    for i in range(len(y_pos)):
        plt.bar(y_pos[i], heights[i], width = 2, align='center', alpha=0.5, color = colour[i])
        
    for i, v in enumerate(height):
        plt.text((3*i)-0.3, v + 0.1 , v, color='black', fontweight='bold')
    plt.xticks(y_pos, grade, color = 'purple')
    plt.xlabel('Course')
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
    colour = []
    for i in range(len(y_pos)):
        colour.append ((np.random.rand(),np.random.rand(), np.random.rand()))
    
    for i in range(len(y_pos)):    
        plt.bar(y_pos[i], height[i], width = 2, align='center', alpha=0.5, color = colour[i])
        
    for i, v in enumerate(height):
        plt.text((3*i)-0.9, v + 0.1 , "{:.2f}".format(v), color='black', fontweight='bold')
    plt.xticks(y_pos, smno, color = 'red')
    plt.xlabel('Semester Number')
    plt.ylabel('SPI')
    plt.title('Result ({})'.format(rollno))
    plt.show()

#5. A function to visually compare performance of two courses of students enrolled in both of them. 
def ComparePerformance(subcode1, subcode2):
    gradeDict = {}
    gradeDictFin = {}
    points = {"AA": 10, "AB": 9, "BB": 8, "BC" : 7, "CC" : 6, "CD" : 5, "DD": 4, "F": 0}
    for i in df.index:
        if subcode1 == df['subno'][i]: 
            gradeDict[df['rollno'][i]] = []
            gradeDict[df['rollno'][i]].append(points[df['grade'][i]])

    for i in df.index:
        if subcode2 == df['subno'][i]:
            if df['rollno'][i] in gradeDict.keys():
                gradeDictFin[df['rollno'][i]] = gradeDict[df['rollno'][i]]
                gradeDictFin[df['rollno'][i]].append(points[df['grade'][i]])

    gradeX = []
    gradeY = []
    for k in gradeDictFin.keys():
        gradeX.append(gradeDictFin[k][0])
        gradeY.append(gradeDictFin[k][1])
    
    plt.scatter(gradeX, gradeY)
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
GradeDistribution(subcode)

semno = 4
branch = "EE"
SubjectWeightage(semno, branch)

rollno = "1401CS20"
semno = 4
SemResult( rollno, semno )

rollno = "1401CS20"
AllSemsSpi(rollno)

subcode1 = "MA101"
subcode2 = "MA102"
ComparePerformance( subcode1, subcode2)

