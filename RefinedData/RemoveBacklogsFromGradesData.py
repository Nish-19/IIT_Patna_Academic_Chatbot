import pandas as pd
import numpy as np


df = pd.read_csv('ori_combined_stud_and_grades_data.csv')
df1 = pd.read_csv('ori_grades_data.csv')
backlog_rolls = {}
for i in df.index:
    if (df['sem1_spi'][i] == 0 or df['sem2_spi'][i] == 0 or df['sem3_spi'][i] == 0 or df['sem4_spi'][i] == 0 or df['sem5_spi'][i] == 0 or df['sem6_spi'][i] == 0 or df['sem7_spi'][i] == 0 or df['sem8_spi'][i] == 0 ):
        backlog_rolls[df['rollno'][i]] = 1

for i in df1.index:
    if df['rollno'][i] in backlog_rolls:
        df1.drop(i, axis = 0, inplace = True)

export_csv = df1.to_csv(
    r'/home/ubuntu/Desktop/Academic Chatbot data/modified_grades_data.csv', index=None, header=True)