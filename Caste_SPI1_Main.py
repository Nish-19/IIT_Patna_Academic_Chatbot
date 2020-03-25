#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd
import seaborn as Sns


# In[36]:


t1=pd.read_csv("student_data.csv")
t1.rename(columns={'Roll Number' : 'rollno' , 'Blood Group' : 'Blood_group', 
'Mother Tongue' : 'Mother_Tongue'},inplace=True )
t2=pd.read_csv("Semester1cst.csv")
t1.sort_values("rollno", axis = 0, ascending = True, 
                 inplace = True, na_position ='last') 
t1 = t1.reset_index()
t1 = t1.drop(['index'],axis=1)
t2.sort_values("rollno", axis = 0, ascending = True, 
                 inplace = True, na_position ='last') 
t2 = t2.reset_index()
t2 = t2.drop(['index'],axis=1)
t1.head()


# In[37]:


t1 = t1.loc[t1['rollno'] != '1401CS18']
t1 = t1.reset_index()
t1 = t1.drop(['index'],axis=1)
t2.sort_values("rollno", axis = 0, ascending = True, 
                 inplace = True, na_position ='last') 
t2 = t2.reset_index()
t2 = t2.drop(['index'],axis=1)
t2.head()


# In[38]:


df=pd.concat([t1,t2],axis='columns')
df = df.loc[:,~df.columns.duplicated()]


# In[39]:


d1=pd.get_dummies(df.Category)
d2=pd.get_dummies(df.Sex)
d3=pd.get_dummies(df.Department)
#d4=pd.get_dummies(df.Board)
#d5=pd.get_dummies(df.State)
#d6=pd.get_dummies(df.Mother_Tongue)
df=pd.concat([df,d1,d2,d3],axis='columns')
df = df.loc[:,~df.columns.duplicated()]
df = df.loc[df['SPI1'] > 5]
df=df.drop(['rollno', 'Name','Department','Sex','Category','Blood_group','Board','Mother_Tongue','State','Branch'], axis = 1)
y=df['SPI1']
df
#df.corr()
#Trying to avoid the dummy variable trap


# In[40]:


Sns.distplot(df.SPI1)


# In[41]:


df=df.drop(['PD','F','CH'],axis=1)
df.head()
Sns.distplot(df.SPI1)
df.corr()


# In[42]:


df.head(5)
df.drop(['SPI1'],axis=1)


# In[43]:


from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(df,y,test_size=0.2)
from sklearn import linear_model
model=linear_model.LinearRegression()
model.fit(X_train,Y_train)


# In[44]:


model.score(X_train,Y_train)


# In[46]:


model.score(X_test,Y_test)


# In[47]:


#model.predict()


# In[ ]:




