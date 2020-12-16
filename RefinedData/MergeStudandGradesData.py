import pandas as pd
import numpy as np
spi = {}


def AllSemsSpi(rollno):
    spi.clear()
    locroll = df1.loc[df1['rollno'] == rollno]
    points = {"AA": 10, "AB": 9, "BB": 8, "BC": 7,
              "CC": 6, "CD": 5, "DD": 4, "F": 0}

    for i in range(1, 9):
        rslt = locroll.loc[locroll['semno'] == i]
        rslt = rslt[['subno', 'crd', 'grade']]
        rslt['points'] = 1
        sm = 0
        tot = 0
        for j in rslt.index:
            rslt['points'][j] = points[rslt['grade'][j]]
            sm = sm + rslt['crd'][j]
            tot = tot + rslt['points'][j]*rslt['crd'][j]
        if sm == 0:
            spi[i] = "NaN"
        else:
            spi[i] = tot/sm
            spi[i] = float("{:.2f}".format(spi[i]))


df1 = pd.read_csv('ori_grades_data.csv')
df2 = pd.read_csv('ori_stud_data.csv')
df2['sem1_spi'] = 0.00
df2['sem2_spi'] = 0.00
df2['sem3_spi'] = 0.00
df2['sem4_spi'] = 0.00
df2['sem5_spi'] = 0.00
df2['sem6_spi'] = 0.00
df2['sem7_spi'] = 0.00
df2['sem8_spi'] = 0.00
for i in df2.index:
    AllSemsSpi(df2['Roll Number'][i])
    df2['sem1_spi'][i] = spi[1]
    df2['sem2_spi'][i] = spi[2]
    df2['sem3_spi'][i] = spi[3]
    df2['sem4_spi'][i] = spi[4]
    df2['sem5_spi'][i] = spi[5]
    df2['sem6_spi'][i] = spi[6]
    df2['sem7_spi'][i] = spi[7]
    df2['sem8_spi'][i] = spi[8]


allcol = list(df2.columns)

for col in allcol:
    df1[col] = "NaN"

for col in allcol:
    for i in df2.index:
        roll = df2['Roll Number'][i]
        df1.loc[df1.rollno == roll, col] = df2[col][i]
df1 = df1.drop(['Roll Number'], axis=1)

export_csv = df1.to_csv(
    r'/home/ubuntu/Desktop/Academic Chatbot data/ori_combined_stud_and_grades_data.csv', index=None, header=True)
