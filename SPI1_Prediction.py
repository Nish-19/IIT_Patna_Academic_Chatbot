#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This is a basic token,where we have considered the marks of all 1st sem students
#With knowledge of marks of only few subjects,we are trying to predict the full SPI.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df2=pd.read_csv("sem1.csv")
temp1=pd.read_csv("Sem1numwt.csv")
temp1.drop(temp1.iloc[:, 20:], inplace = True, axis = 1) 
temp1.head()


# In[3]:


#for i in range(temp1['rollno'].count()) :
#temp['CPI']=temp['credCH101'][0]*temp['CH101'][0]+temp['credCH110'][0]*temp['CH110']
List =[]
temp1['SPI1']=0.0
List = ['CH101', 'CH110','EE101','HS101','MA101','ME110','ME111','PH101'] 
tot=0
for i in range(len(List)) :
    tot=tot+temp1['cred'+List[i]][0]
temp1


# In[4]:


for i in range(temp1['rollno'].count()) :
    for j in range(len(List)) :
        temp1['SPI1'][i]=temp1['SPI1'][i]+temp1[List[j]][i]*temp1['cred'+List[j]][0]
temp1['SPI1'] = temp1['SPI1'].div(tot)
temp2=temp1[['rollno','Branch','SPI1']]
temp1 = temp1.loc[temp1['SPI1'] > 5]
temp1.head()
temp2.head()                                                   
                                                    
                                                    


# In[5]:


#temp2.to_csv (r'C:\Users\Souhardya\OneDrive\Desktop\Mine\Semester1cst.csv', index = None, header=True)


# In[6]:


Input=temp1[['CH101','EE101','HS101','MA101','PH101']]
Input.head(5)


# In[7]:


Output=temp1['SPI1']
Output.head(5)


# In[8]:


from sklearn.model_selection import train_test_split


# In[9]:


X_train,X_test,Y_train,Y_test=train_test_split(Input,Output,test_size=0.2)
len(X_train)


# In[10]:


from sklearn import linear_model
model=linear_model.LinearRegression()


# In[11]:


model.fit(X_train,Y_train)


# In[12]:


model.score(X_train,Y_train)


# In[13]:


model.score(X_test,Y_test)


# In[ ]:




