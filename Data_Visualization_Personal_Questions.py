#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[4]:


df=pd.read_csv("student_data.csv")
df.rename(columns={"Blood Group": "Blood", "Mother Tongue": "Mother"},inplace = True)
df.head(4)


# In[5]:


List =['CS','EE','ME','CE','CH']


# In[6]:


#q(2,1)What is the number of SC/ST/Gen/PD students in whole batch
def stdcatno() :
    gen=0
    sc=0
    st=0
    pd=0
    obc=0
    for i in range(200) :
        if df['Category'][i]=='OB' :
            obc=obc+1
        if df['Category'][i]=='SC' :
             sc=sc+1
        if df['Category'][i]=='GE' :
             gen=gen+1
        if df['Category'][i]=='ST' :
             st=st+1
        if df['Category'][i]=='OB' :
             pd=pd+1
    print("General :",gen)
    print("OBC:",obc)
    print("SC",sc)
    print("ST",st)
    print("PD",pd)
    
    plt.hist(df.Category,color='green')
    plt.title('Whole Batch')
    


# In[7]:


#stdcatno()


# In[8]:


#Q(2,last)Branchwise category count
def branchcatno(Dept) :
    for i in range(len(List)) : 
        obc=0
        sc=0
        gen=0
        st=0
        pd=0
        #CS = df.loc[df['Department'] == 'CS']
        print("For ",List[i],":")
        for j in range(200) :
            if df['Department'][j]==List[i] :
                if df['Category'][j]=='OB' :
                    obc=obc+1
                if df['Category'][j]=='SC' :
                    sc=sc+1
                if df['Category'][j]=='GE' :
                    gen=gen+1
                if df['Category'][j]=='ST' :
                    st=st+1
                if df['Category'][j]=='OB' :
                    pd=pd+1
    
        print("General :",gen)
        print("OBC:",obc)
        print("SC",sc)
        print("ST",st)
        print("PD",pd)
        dep = df.loc[df['Department'] == List[i]]
        print(sns.countplot(dep['Category']))
        print(plt.title(List[i]))
        #print(plt.hist(dep.Category,color='green'))


# In[9]:


#branchcatno()


# In[10]:


#Q(2,3)SexRatio of Batch
def sexratio() :
    m=0
    f=0
    for i in range(200) :
        if df['Sex'][i]=='M' :
            m=m+1
        else :
            f=f+1
    print("Male:",m)
    print("Female:",f)
    print("Ratio:",m/f)
    print(sns.countplot(df['Sex']))


# In[11]:


#sexratio()


# In[14]:


#Blood Group Distribution of batch
def bloodgroup(df) :
    a_plus=0
    a_neg=0
    b_plus=0
    b_neg=0
    ab_plus=0
    ab_neg=0
    o_plus=0
    o_neg=0
    for i in range(200) :
        if df['Blood'][i]=='A+' :
            a_plus=a_plus+1
        if df['Blood'][i]=='A-' :
            a_neg=a_neg+1
        if df['Blood'][i]=='B+' :
            b_plus=b_plus+1
        if df['Blood'][i]=='B-' :
            b_neg=a_neg+1
        if df['Blood'][i]=='AB+' :
            ab_plus=ab_plus+1
        if df['Blood'][i]=='AB-' :
            ab_neg=ab_neg+1
        if df['Blood'][i]=='O+' :
            o_plus=o_plus+1
        if df['Blood'][i]=='O-' :
            o_neg=o_neg+1
    print("A plus:",a_plus,"Percentage : ",a_plus/0.5)
    print("A minus:",a_neg,"Percentage : ",a_neg/0.5)
    print("B plus:",a_plus,"Percentage : ",b_plus/0.5)
    print("B minus:",a_neg,"Percentage : ",b_neg/0.5)
    print("AB plus:",a_plus,"Percentage : ",ab_plus/0.5)
    print("AB minus:",a_neg,"Percentage : ",ab_neg/0.5)
    print("O plus:",a_plus,"Percentage : ",o_plus/0.5)
    print("O minus:",a_neg,"Percentage : ",o_neg/0.5)
   

    
    #plt.hist(df.Blood,color='green')
    sns.countplot(df['Blood'])
    plt.title('Whole Batch')


# In[15]:


#Number of students from UP
def state(stt) :
    tot=0
    for i in range(200) :
        if df['State'][i]==stt:
                tot=tot+1
    print("Number of students from",stt,":",tot)
    print("Whole Graph is as follows-")
    sns.countplot(df['State'])
    plt.title('Whole Batch')
    
    


# In[16]:


#state('UP')


# In[1]:


#Number of SC student from Bihar
def nopluscat(stt,cat) :
    tot=0
    for i in range(200) :
        if (df['State'][i]==stt) & (df['Category'][i]==cat) :
            tot=tot+1
    print("Number of",cat,"students from",stt,":",tot)
    
            


# In[17]:


#nopluscat("Bihar","SC")


# In[ ]:




