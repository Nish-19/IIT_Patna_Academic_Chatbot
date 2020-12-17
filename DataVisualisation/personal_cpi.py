#!/usr/bin/env python
# coding: utf-8

# In[115]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors as mcolors
color = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
sdf=[]
for s,n in color.items():
    sdf.append(s)
    #print(s)


# In[116]:


df=pd.read_csv("student_data.csv")
df.rename(columns={"Blood Group": "Blood", "Mother Tongue": "Mother"},inplace = True)
df.head(4)


# In[117]:


List =['CS','EE','ME','CE','CH']


# In[118]:


# Creating autocpt arguments..Non call function
def func(pct, allvalues): 
    absolute = int(pct / 100.*np.sum(allvalues)) 
    return "{:.1f}%\n({:d} )".format(pct, absolute) 
#Customizing pie charts function
def plots(label=None,data=None,explode=None,colors=None,title=None):
    wp = { 'linewidth' : 1, 'edgecolor' : "green" } 
    # Creating plot 
    fig, ax = plt.subplots(figsize =(20, 20)) 
    wedges, texts, autotexts = ax.pie(data,  
                                      autopct = lambda pct: func(pct, data), 
                                      explode = explode,  
                                      labels = label, 
                                      shadow = True, 
                                      colors = colors, 
                                      startangle = 90, 
                                      wedgeprops = wp, 
                                      textprops = dict(color ="black"),
                                     ) 

    # Adding legend 
    ax.legend(wedges, label, 
              title =title, 
              loc ="center left", 
              bbox_to_anchor =(1, 0, 0.5, 1)) 
    plt.setp(autotexts, size = 8, weight ="bold") 
    ax.set_title("Customizing pie chart for "+ title) 

    # show plot 
    plt.show() 


# In[119]:


#What is the number of SC/ST/Gen/PD students in whole batch
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
    sns.countplot(df.Category)
    plt.title('Whole Batch')
    plt.show()
    label = ['Gen', 'OBC', 'SC', 'ST', 'PD',] 
    data = [gen,obc,sc,st,pd] 
    # Creating explode data 
    explode = (0.0, 0.0, 0.0, 0.0, 0.0) 
    # Creating color parameters 
    colors = ( "orange", "cyan", "brown", "lightgreen", "blue",) 
    # Wedge properties 
    wp = { 'linewidth' : 1, 'edgecolor' : "green" } 
    plots(label,data,explode,colors,"Whole Batch")
    


# In[120]:


stdcatno()


# In[121]:


#Branchwise category count.If no branch is given,call category count for batch
def branchcatno(brr=None) :
    if brr == None:
        stdcatno()
    else:
        temp=df[df['Department']== brr]
        sns.countplot(temp['Category'])
        plt.title(brr)
        label = ['Gen', 'OBC', 'SC', 'ST', 'PD']
        gen=(temp.Category == 'GE').sum()
        obc=(temp.Category == 'OB').sum()
        sc=(temp.Category == 'SC').sum()
        st=(temp.Category == 'ST').sum()
        pd=(temp.Category == 'PD').sum()
        print("For "+ brr +":")
        print("General: ",gen)
        print("OBC: ",obc)
        print("SC: ",sc)
        print("ST: ",st)
        print("PD: ",pd)
        data = [gen,obc,sc,st,pd] 
        # Creating explode data 
        explode = (0.0, 0.0, 0.0, 0.0, 0.0) 
        # Creating color parameters 
        colors = ( "orange", "cyan", "brown", "lightgreen", "blue") 
        # Wedge properties 
        wp = { 'linewidth' : 1, 'edgecolor' : "green" } 
        plots(label,data,explode,colors,brr)
    
#      for i in range(len(List)) : 
#         obc=0
#         sc=0
#         gen=0
#         st=0
#         pd=0
#         #CS = df.loc[df['Department'] == 'CS']
#         print("For ",List[i],":")
#         for j in range(200) :
#             if df['Department'][j]==List[i] :
#                 if df['Category'][j]=='OB' :
#                     obc=obc+1
#                 if df['Category'][j]=='SC' :
#                     sc=sc+1
#                 if df['Category'][j]=='GE' :
#                     gen=gen+1
#                 if df['Category'][j]=='ST' :
#                     st=st+1
#                 if df['Category'][j]=='OB' :
#                     pd=pd+1
    
#         print("General :",gen)
#         print("OBC:",obc)
#         print("SC",sc)
#         print("ST",st)
#         print("PD",pd)
#         dep = df.loc[df['Department'] == List[i]]
#         sns.countplot(df['Category'])
#         plt.title(List[i])
        #print(plt.hist(dep.Category,color='green'))


# In[122]:


branchcatno('CS')


# In[123]:


#Helper function in plotting 
def localplot(br,title):
    sns.countplot(br['Sex'])
    #plt.hist(df.Sex,color='green')
    plt.title(title)
    plt.show()
    
#Sex ratio of batch+ branchwise also 
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
    sns.countplot(df['Sex'])
    #plt.hist(df.Sex,color='green')
    plt.title('Whole Batch')
    plt.show()
    # Creating dataset 
    label = ['Male','Female'] 
    data = [m,f] 
    explode = (0.1, 0.0) 
    # Creating color parameters 
    colors = ( "orange","lightgreen",) 
    plots(label,data,explode,colors,"Whole Batch")
    CS = df.loc[df['Department'] == 'CS']
    CE = df.loc[df['Department'] == 'CE']
    CH = df.loc[df['Department'] == 'CH']
    EE = df.loc[df['Department'] == 'EE']
    ME=  df.loc[df['Department'] == 'ME']
    localplot(CS,"CS")
    localplot(EE,"EE")
    localplot(ME,"ME")
    localplot(CE,"CE")
    localplot(CH,"CH")


# In[124]:


sexratio()


# In[125]:


#Blood Group Distribution of batch
def bloodgroup() :
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
    label = ['A+','A-','B+','B-','AB+','AB-','O+','O-'] 
    data = [a_plus,a_neg,b_plus,b_neg,ab_plus,ab_neg,o_plus,o_neg] 
    explode = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0,0.0)  
    # Creating color parameters 
    colors = ( "orange","cyan","brown","lightgreen", "indigo", "beige",'yellow','red')
    plots(label,data,explode,colors,"Whole Batch")   


# In[126]:


bloodgroup()


# In[135]:


#Number of students from a particular state
#Kept Bihar as default
#Also outputs the all state distribution charts alawys
def state(stt="BH") :
    dicto={}
    label=[]
    data=[]
    explode=[]
    colo=[]
    tot=0
    for i in range(200) :
        keys=df['State'][i]
        if keys in dicto: 
            cp=dicto[keys]+1
            dicto[keys]=cp
        else:
            dicto.update({keys: 1})
    for state,number in dicto.items(): 
        label.append(state)
        data.append(number) 
    leng=len(dicto)
    print("Len is ",leng)
    for i in range(leng):
        explode.append(0.0)
    print("Number of students from",stt,":",dicto[stt])
    print("Whole Graph is as follows-")
    plt.figure(figsize =(10, 10)) 
    sns.countplot(df['State'])
    plt.title('Whole Batch') 
    i=0
    for i in range(len(sdf)):
        if i>8:
            colo.append(sdf[i])
        if i ==leng+8:
            break
        i+=1
    colors = tuple(colo)
    #print(datatype(colors))
    plots(label,data,explode,colors,"Whole Batch")   


# In[136]:


state('WB')


# In[153]:


def local2(temp,lab,cp=0):
    temp=temp[lab].value_counts().reset_index()
    #plt.pie(x=temp['State'],labels=temp['State'],)
    #Giving State.So,plotting Category composition of that particular state
    plt.figure(figsize =(20, 20)) 
    ax=plt.subplot(111)
    #plt.title('Whole Batch '+cat+ ' Composition')
    if cp == 1:
        plt.pie(temp[lab],labels = None,startangle=90) 
    else:
        plt.pie(temp[lab],labels = temp['index'],startangle=90) 
    # chartBox = ax.get_position()
    # ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
    ax.legend(loc='upper center',labels = temp['index'], bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
    plt.show()


#Number of Caste-State Distribution SC student from Bihar  Modified..
def nopluscat(stt=None,cat=None) :
    tot=0
    #Not giving input of state or category.SO plotting statewise students count 
    if (stt==None) & (cat==None):
        state() 
    #Giving Category.So,plotting category statewise
    elif stt==None:
        temp=df.loc[df['Category'] == cat]
        sns.countplot(temp['State'])
        plt.title('Whole Batch '+cat+' Composition')
        local2(temp,'State')
    elif cat==None:
        temp=df.loc[df['State'] == stt]
        sns.countplot(temp['Category'])
        plt.title('Whole Batch ' + stt + ' Composition')
        local2(temp,'Category')
    #Giving state and category both.So,outputting the count and plotting that category distribution for all states.
    else:   
        for i in range(200) :
            if (df['State'][i]==stt) & (df['Category'][i]==cat) :
                tot=tot+1
        print("Number of",cat,"students from",stt,":",tot)
        temp=df.loc[df['Category'] == cat]
        sns.countplot(temp['State'])
        plt.title('Whole Batch '+cat+ ' Composition') 
        plt.show() 
        local2(temp,'State')
    
            


# In[154]:


nopluscat('WB','SC')
#df.head()


# In[138]:


com=pd.read_csv("RefinedCombinedStudentandGradesData.csv")
com = com.drop_duplicates(subset='rollno', keep="first")

#Pass the spinumber or cpi as the parameter.If nothing is given,cpi will be taken bydefault.
#Plotting spi distribution
def cpi_gaussian_distribution(par='cpi'):
    sns.distplot(com[par])
#com.head()
cpi_gaussian_distribution('sem8_spi')
com


# In[141]:


# Plots of 1st year Result against overall cpi
def spi1_spi2_cpi():

    plt.scatter(com['sem1_spi'], com['cpi'], color='red')
    #plt.plot(X_train['sem1_spi'], model.predict(X_train), color='blue')
    plt.title('SPI_1 vs CPI')
    plt.xlabel('SPI_1stSem')
    plt.ylabel('CPI')
    plt.show()
    plt.scatter(com['sem2_spi'], com['cpi'], color='blue')
    #plt.plot(X_train['sem1_spi'], model.predict(X_train), color='blue')
    plt.title('SPI_2 vs CPI')
    plt.xlabel('SPI_2ndSem')
    plt.ylabel('CPI')
    plt.show()
    #     plt.figure(figsize =(220, 220)) 
    com['CPI_diff'] = -(com['sem1_spi']+com['sem2_spi'])/2.0 + com['cpi'] 
    #com.plot.bar(x='rollno', y='CPI_diff', rot=140, title="CPI difference with 1st Year SPI");
    #     plt.show(block=True);
    fig = plt.figure(figsize = (10, 10)) 
    # creating the bar plot 
    plt.bar(com['rollno'], com['CPI_diff'], color ='maroon',  
            width = 0.4) 
    plt.xlabel(" ") 
    plt.ylabel("CPI_diff_with_1stYear_SPI") 
    plt.title("1st Year Performance vs Total performance") 
    plt.legend("CPI")
    plt.show() 
spi1_spi2_cpi()




def boardcnt(bord =None):
    if bord != None:
        ds=com[com['Board']==bord]
        print("Number of students from "+bord +" is " + len(ds['rollno']))
    ax=plt.subplot(111)
    sns.countplot(com['Board'])
    temp=com['Board'].value_counts().reset_index()
    print(temp)
    ax.legend(loc='upper center',labels = temp['index'], bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)
    plt.title('Whole Batch Board Composition')
    plt.show()
    local2(com,'Board',1)

boardcnt()









