#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import seaborn as Sns


# In[3]:


t1=pd.read_csv("student_data.csv")
t1.rename(columns={'Roll Number' : 'rollno' , 'Blood Group' : 'Blood_group', 
'Mother Tongue' : 'Mother_Tongue'},inplace=True )
t2=pd.read_csv("Sem2wtnum.csv")
t1.head()


# In[4]:


t2.head()


# In[5]:


t2['SPI2'] = t2[['PH102', 'CS101','ME101','CH102','CS110','EE102','MA102','PH110']].mean(axis=1)
t2.head(10)
t3=t2[['rollno','SPI2']]


# In[6]:


df=pd.concat([t1,t3],axis='columns')
df = df.loc[:,~df.columns.duplicated()]
df.head(50)


# In[7]:


d1=pd.get_dummies(df.Category)
d2=pd.get_dummies(df.Sex)
d3=pd.get_dummies(df.Department)
#d4=pd.get_dummies(df.Board)
#d5=pd.get_dummies(df.State)
#d6=pd.get_dummies(df.Mother_Tongue)
df=pd.concat([df,d1,d2,d3],axis='columns')
df = df.loc[:,~df.columns.duplicated()]
df = df.loc[df['SPI2'] > 5]
df=df.drop(['rollno', 'Name','Department','Sex','Category','Blood_group','Board','Mother_Tongue','State'], axis = 1)
y=df['SPI2']
df.head()


# In[8]:


df.corr()


# In[9]:


Sns.distplot(df.SPI2)


# In[10]:


#df=df.drop(['PD','F','CH'],axis=1)
df.head()
Sns.distplot(df.SPI2)
df.corr()


# In[11]:


df.head(5)
df.drop(['SPI2'],axis=1)


# In[12]:


from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(df,y,test_size=0.2)
from sklearn import linear_model
model=linear_model.LinearRegression()
model.fit(X_train,Y_train)


# In[13]:


model.score(X_train,Y_train)


# In[14]:


model.score(X_test,Y_test)


# In[ ]:




