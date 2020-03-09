import mysql.connector as mysql

def initialise_database_connection():
	db = mysql.connect(#establishing connection with mysql
    	host = "hostname",
    	user = "username",
    	database = 'databasename',
    	password = 'password',
    	auth_plugin='caching_sha2_password'
	)#update queries will work only if we provide the password while connecting.
	print ("prompt from the mySQL connector : ",db)
	return db


def generate_output(sql_query, db):
	cursor = db.cursor()
	cursor.execute("USE innov_lab;")#selecting the database to work work
	cursor.execute(sql_query)#fire the query
	returnedData = cursor.fetchall()#fetch the result from the connector
	print(returnedData)
