from wh_nlp_sql import *
from nltk_chat import *
from cgb import *
if __name__ == '__main__':
	print('Hello! My name is academic chatbot. I am here at your service')
	utter = ''
	utter_ip = ''
	print("Please enter D if you want to ask a database question else just enter the question. Type quit to end the conversation\n")
	db = initialise_database_connection()
	nlp = spacy.load("en_core_web_sm")
	utter = input('> ')
	while utter != 'quit':
		if utter == 'D' or utter == 'd':
			print('Please enter the database related question')
			utter_ip = input('> ')
			if utter_ip =="predict_cpi":
				cat=input("Enter the category:")
				sex=input("Enter Gender:")
				brh=input("Enter branch:")
				print("Predicted CPI is:",cgb(cat,sex,brh))
			else:
				doc=nlp(utter_ip)
				sql_query=create_dictionary(utter_ip,doc)
				generate_output(sql_query,db)
		# elif utter == 'quit':
		# 	print("It was great talking to you! Thank You!")
		# 	break
		else:
			chatty(utter)
		utter = input('> ')
	print("It was nice talking to you! Thank You")
