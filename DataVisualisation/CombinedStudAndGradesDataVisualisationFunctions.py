import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('ori_combined_stud_and_grades_data.csv')

# percentage of males and females on a given grade in a particular subject
def MFPertOnAGrade(subcode, grade):
    TotF = 0
    PartF = 0
    TotM = 0
    PartM = 0
    for i in df.index:
        if (df['subno'][i] == subcode and df['Sex'][i] == 'F'):
            TotF = TotF + 1
            if (df['grade'][i] == grade):
                PartF = PartF + 1
        
        if (df['subno'][i] == subcode and df['Sex'][i] == 'M'):
            TotM = TotM + 1
            if (df['grade'][i] == grade):
                PartM = PartM + 1

    print(str(PartF) + " females out of " + str(TotF) + " enrolled got " + grade + " grade in " + subcode)
    print(str(PartM) + " males out of " + str(TotM) + " enrolled got " + grade + " grade in " + subcode)
    
    height = []
    height.append((PartF/TotF)*100)
    height.append((PartM/TotM)*100)
    bars = ("Male", "Female")
    y_pos = np.arange(len(bars))

    #Set descriptions:
    plt.title("Percentage of Male and Female who got " + grade + " grade in subject " + subcode + "\n")
    plt.ylabel('Percentage')
    plt.xlabel('Gender')
    
    #Set tick colors:
    ax = plt.gca()
    ax.tick_params(axis='x', colors='red')
    ax.tick_params(axis='y', colors='red')
        
    plt.bar(y_pos, height, color=['dodgerblue', 'orange'])
    plt.xticks(y_pos, bars)
    for i, v in enumerate(height):
        plt.text(i-0.1, v + 0.1 , "{:.2f}".format(v) + "%", color='black', fontweight='bold')
    
    plt.show()
    
def CategoryPertOnAGrade(subcode, grade):
    Tot = {"OB" : 0, "SC" : 0, "ST" : 0, "GE" : 0, "PD": 0}
    Part = {"OB" : 0, "SC" : 0, "ST" : 0, "GE" : 0, "PD": 0}
    for i in df.index:
        if (df['subno'][i] == subcode):
            Tot[df['Category'][i]] += 1
            if (df['grade'][i] == grade):
               Part[df['Category'][i]] += 1
    height = []
    bars = []
    for k in Tot.keys():
        print(str(Part[k]) + k + " out of " + str(Tot[k]) + " enrolled got " + grade + " grade in " + subcode)
        height.append((Part[k]/Tot[k])*100)
        bars.append(k)
    
    y_pos = np.arange(len(bars))

    #Set descriptions:
    plt.title("Percentage of each category who got " + grade + " grade in subject " + subcode + "\n")
    plt.ylabel('Percentage')
    plt.xlabel('Category')
    
    #Set tick colors:
    ax = plt.gca()
    ax.tick_params(axis='x', colors='red')
    ax.tick_params(axis='y', colors='red')
        
    plt.bar(y_pos, height, color=['dodgerblue', 'orange', "green", "red", "purple"])
    plt.xticks(y_pos, bars)
    for i, v in enumerate(height):
        plt.text(i-0.3, v + 0.1 , "{:.2f}".format(v) + "%", color='black', fontweight='bold')
    
    plt.show()

subcode =  "MA101"
grade = "AA"
MFPertOnAGrade(subcode, grade)

subcode =  "MA101"
grade = "AA"
CategoryPertOnAGrade(subcode, grade)