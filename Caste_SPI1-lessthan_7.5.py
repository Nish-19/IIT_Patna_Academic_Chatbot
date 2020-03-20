#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


t1=pd.read_csv("student_data.csv")
t1.rename(columns={'Roll Number' : 'rollno' , 'Blood Group' : 'Blood_group', 
'Mother Tongue' : 'Mother_Tongue'},inplace=True )
t2=pd.read_csv("Semester1cst.csv")
t1


# In[3]:


df=pd.concat([t1,t2],axis='columns')
df = df.loc[:,~df.columns.duplicated()]
df['dec']=0.0
for i in range(200) :
    if df['SPI1'][i]>=7.5 :
        df['dec'][i]=1
df.head()


# In[4]:


d1=pd.get_dummies(df.Category)
d2=pd.get_dummies(df.Sex)
d3=pd.get_dummies(df.Department)
#d4=pd.get_dummies(df.Board)
#d5=pd.get_dummies(df.State)
#d6=pd.get_dummies(df.Mother_Tongue)
df=pd.concat([df,d1,d2,d3],axis='columns')
df = df.loc[:,~df.columns.duplicated()]
df = df.loc[df['SPI1'] > 4]
df=df.drop(['rollno', 'Name','Department','Sex','Category','Blood_group','Board','Mother_Tongue','State','Branch'], axis = 1)
y=df['dec']
df
#Trying to avoid the dummy variable trap


# In[5]:


df=df.drop(['SPI1','PD','F','CH'],axis=1)
df.head()


# In[6]:


from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(df,y,test_size=0.2)


# In[7]:


from sklearn import tree
model=tree.DecisionTreeClassifier()
model.fit(X_train,Y_train)


# In[8]:


model.score(X_train,Y_train)


# In[9]:


model.score(X_test,Y_test)


# In[ ]:




