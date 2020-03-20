#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[39]:


df=pd.read_csv("sem_grades.csv")
df['Branch']=df['rollno'].str[4:6]
df


# In[40]:


sem = df.loc[(df['semno'] == 2) ]
#sem = sem.drop_duplicates('rollno')
#sem.sort_values(by=['rollno'])
#sem = sem.reset_index()
#sem = sem.drop(['index'],axis=1)
sem


# In[41]:


sem=sem.drop(['year', 'crd','date_of_entry','sub_type'], axis = 1) 
sem.head()


# In[35]:


df2=pd.read_csv("Sem2.csv")
df2


# In[43]:


List = []   
for i in range(df2['subno'].count()) :
   if df2['CS'][i]==1 & df2['EE'][i]==1 & df2['ME'][i]==1 & df2['CH'][i]==1 & df2['CE'][i]==1:
    List.append(df2['subno'][i])
    
print(List)


# In[44]:


sem1 = sem.loc[sem['subno']==List[0]]
sem1 = sem1.reset_index()
sem1 = sem1.drop(['index'],axis=1)
sem1.rename(columns={'grade' : sem1['subno'][0]},inplace=True)
for i in range(1,len(List)):
   sem2 = sem.loc[sem['subno']==List[i]]
   sem2 = sem2.reset_index()
   sem2 = sem2.drop(['index'],axis=1)
   sem2.rename(columns={'grade' : sem2['subno'][0]},inplace=True)
   sem1=pd.concat([sem1,sem2],axis='columns')
   sem1 = sem1.loc[:,~sem1.columns.duplicated()]   
sem1


# In[46]:


sem1 = sem1.drop(['subno'],axis=1)
sem1.sort_values(["rollno"], axis=0, 
                 ascending=True, inplace=True) 
sem1 = sem1.reset_index()
sem1 = sem1.drop(['index'],axis=1) 
#sem1 = sem1[['rollno','semno','Branch','semno','CS203','CS221','EE220','MA201']]
sem1


# In[47]:


sem1.to_csv (r'C:\Users\Souhardya\OneDrive\Desktop\Mine\Semester2wts.csv', index = None, header=True) 


# In[ ]:




