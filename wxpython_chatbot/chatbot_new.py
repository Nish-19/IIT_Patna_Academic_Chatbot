from wh_nlp_sql_new import *
from nltk_chat_new import *
from reorg_dbclass import *
from sentiment_analyzer import *
from collections import Counter
import os


def get_sentiment_report(sentiment_overall):
	count = Counter(sentiment_overall)
	total = 0
	for i in count.values():
		total+=i
	print('The sentimenet distribution of the user is:')
	print('Positive Sentiment:', (count[1]/total))
	print('Negative Sentiment:', (count[-1]/total))
	print('Neutral Sentiment:', (count[0]/total))

def initialize():
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
	MAX_LENGTH = 15
	x_train, y_train, x_test, y_test = import_dataset()
	embedding_matrix, tokenizer = get_embeddings(x_train, x_test)
	db = initialise_database_connection()
	nlp = spacy.load("en_core_web_sm")
	return embedding_matrix, tokenizer, MAX_LENGTH, db, nlp

def get_output(utter, embedding_matrix, tokenizer, MAX_LENGTH, db, nlp):
	if utter == 'quit' or utter == 'q':
		return "exit"
	choice = get_inference(utter, embedding_matrix, tokenizer, MAX_LENGTH)
	if choice == 0:
		output = chatty(utter)
	elif choice == 1:
		try:
			doc = nlp(utter)
			sql_query = create_dictionary(utter, doc)
			output = generate_output(utter, sql_query, db)
		except Exception:
			output = 'Sorry that didn\'t work.'
	
	return choice, output


if __name__ == '__main__':
	print('Hello! My name is academic chatbot. I am here at your service')
	print('Please wait! I am configuring myself')
	# Preparing sentence classifier
	os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
	MAX_LENGTH = 15
	x_train, y_train, x_test, y_test = import_dataset()
	embedding_matrix, tokenizer = get_embeddings(x_train, x_test)

	utter = ''
	utter_ip = ''
	#print("Please enter D if you want to ask a database question else just enter the question. Type quit to end the conversation\n")
	db = initialise_database_connection()

	print('I am ready! Let\'s Start!')

	nlp = spacy.load("en_core_web_sm")

	# Opening the feedback module
	feedback_file = open('feedback.csv', 'a+')

	# list to save all utterances
	history = []
	sentiment_overall = []
	# Getting the first utterance
	utter = input('> ')
	history.append(utter)
	# while utter != 'quit':
	# 	if utter == 'D' or utter == 'd':
	# 		print('Please enter the database related question')
	# 		utter_ip = input('> ')
	# 		doc = nlp(utter_ip)
	# 		sql_query = create_dictionary(utter_ip, doc)
	# 		generate_output(sql_query, db)
	# 	# elif utter == 'quit':
	# 	# 	print("It was great talking to you! Thank You!")
	# 	# 	break
	# 	else:
	# 		chatty(utter)
	# 	utter = input('> ')

	# Pass utter to a sentence classifier
	while utter != 'quit' or utter != 'q':
		choice = get_inference(utter, embedding_matrix, tokenizer, MAX_LENGTH)
		if choice == 0:
			chatty(feedback_file, utter)
		elif choice == 1:
			try:
				doc = nlp(utter)
				sql_query = create_dictionary(utter, doc)
				generate_output(utter, sql_query, db, feedback_file)
			except Exception:
				print('Sorry that didn\'t work.')
		utter = input('> ')
		if utter == 'quit':
			break
		history.append(utter)
		sentiment_overall.append(get_polarity(utter))

	get_sentiment_report(sentiment_overall)

	print("It was nice talking to you! Thank You")

