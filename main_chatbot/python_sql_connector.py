import mysql.connector as mysql
from sentence_similarity import *

def initialise_database_connection():
	db = mysql.connect(#establishing connection with mysql
    	host = "LAPTOP-P9CM599B",
    	user = "check",
    	database = 'innov_lab',
    	password = '0123',
    	auth_plugin='caching_sha2_password'
    	#it is good practice to include the passwd as well.
	)#update queries will work only if we provide the password while connecting.
	print ("prompt from the mySQL connector : ",db)
	return db


def generate_output(utter, sql_query, db):
	cursor = db.cursor()
	cursor.execute("USE innov_lab;")#selecting the database to work work
	try:
		cursor.execute(sql_query)#fire the query
		returnedData = cursor.fetchall()#fetch the result from the connector
		unique_set = set(returnedData)
		unique_list = list(unique_set)
		print(unique_list)
	except Exception:
		print('Sorry query not found. These are the most similar sounding queries')
		find_similarity(utter)