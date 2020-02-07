import sys#used to take input from command line
import time#used to find curr time.
import mysql.connector as mysql

db = mysql.connect(#establishing connection with mysql
    host = "localhost",
    user = "vaibhavgakhreja",
    #it is good practice to include the passwd as well.
)#update queries will work only if we provide the password while connecting.

print "prompt from the mySQL connector : ",db

cursor = db.cursor()

if len(sys.argv) > 1:#if there is a query
    question = " ".join(sys.argv[1:])#first element in argv is path of our file,then second argv onwards we concat every element(with spaces in between) to form a single string.

question = question.lower()#convert all to lowercase

x=question.split()#tokenise the string

print "tokenised input : ",x 

if x.count("select"):#type : select fieldName from tableName for rollnumber
    query = "SELECT " + x[1] +\
            "\nFROM " + x[3] +\
            "\nWHERE rollNumber=\"" + x[5] + "\";"
elif x.count("update"):#type : update fieldName from tableName for rollnumber to newVal
    query = "UPDATE " + x[3] +\
            "\nSET " + x[1] + "=\"" + x[7] + "\"" +\
            "\nWHERE rollNumber=\"" + x[5] + "\";"
elif x.count("delete"):#type : delete fieldName from tablename for rollnumber
    query = "DELETE " + x[1] +\
            "\nFROM " + x[3] +\
            "\nWHERE rollNumber=\"" + x[5] + "\";"
elif x.count("insert"):#type : insert space_seperated_data from tablename for rollnumber
    #query = "INSERT IN
else:
    query = "not identified as a valid command, try something else!"

print "query made : "
print query

cursor.execute("USE play;")#selecting the database to work work

cursor.execute(query)#fire the query

returnedData = cursor.fetchall()#fetch the result from the connector

for data in returnedData:#returned data is an array of tuples 
    print data[0]#first element of the tuple is our answer.
