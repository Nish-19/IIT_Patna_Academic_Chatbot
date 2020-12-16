
# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
df = pd.read_csv('ori_grades_data.csv')

# Organising the data
ma101 = df.loc[df['subno'] == 'MA101',['rollno','grade']]
ma102 = df.loc[df['subno'] == 'MA102',['rollno','grade']]

ma101 = ma101.rename(columns = {"grade": "grade_ma101"})
ma101 = ma101.reset_index()
ma101 = ma101.drop(['index'],axis=1)
ma102 = ma102.reset_index()
ma102 = ma102.drop(['index'],axis=1)
ma101['grade_ma102'] = "F"
i=0
j=0
while i < 200:
    if ma101['rollno'][i] == ma102['rollno'][j]:
        ma101['grade_ma102'][i] = ma102['grade'][j]
        i += 1
        j += 1
    else:
        ma101['grade_ma102'][i] = ma101['grade_ma101'][i]
        i += 1
dic = {'AA':10,'AB':9,'BB':8,'BC':7,'CC':6,'CD':5,'DD':4,'F':3}
for i in range(200):
    ma101['grade_ma101'][i] = dic[ma101['grade_ma101'][i]] 
    ma101['grade_ma102'][i] = dic[ma101['grade_ma102'][i]] 
    
ma101[['grade_ma101', 'grade_ma102']] = ma101[['grade_ma101', 'grade_ma102']].astype(float)

# Simple Linear Regression
X = ma101.iloc[:,1].values
y = ma101.iloc[:,2].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 0)

# Feature Scaling
"""from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)"""

# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
X_train=X_train.reshape(-1,1)
y_train=y_train.reshape(-1,1) 
regressor.fit(X_train, y_train)

#Predicting the Test set results
X_test=X_test.reshape(-1,1)
y_pred = regressor.predict(X_test)

# Visualising the Training set results
plt.scatter(X_train, y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.title('ma101 vs ma102 (Training set)')
plt.xlabel('ma101')
plt.ylabel('ma102')
plt.show()


# Visualising the Test set results
plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')
plt.title('ma101 vs ma102 (Test set)')
plt.xlabel('ma101')
plt.ylabel('ma102')
plt.show()




