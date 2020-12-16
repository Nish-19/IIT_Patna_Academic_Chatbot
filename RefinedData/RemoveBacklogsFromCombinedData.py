import pandas as pd
import numpy as np

df = pd.read_csv('ori_combined_stud_and_grades_data.csv')
for i in df.index:
    if (df['sem1_spi'][i] == 0 or df['sem2_spi'][i] == 0 or df['sem3_spi'][i] == 0 or df['sem4_spi'][i] == 0 or df['sem5_spi'][i] == 0 or df['sem6_spi'][i] == 0 or df['sem7_spi'][i] == 0 or df['sem8_spi'][i] == 0 ):
        df.drop(i, axis = 0, inplace=True)

export_csv = df.to_csv(
    r'/home/ubuntu/Desktop/Academic Chatbot data/modified_combined_stud_and_grades_data.csv', index=None, header=True)
