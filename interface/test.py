from wh_nlp_sql import *
from nltk_chat import *
from reorg_dbclass import *
from sentiment_analyzer import *
from collections import Counter
import os


def get_sentiment_report(sentiment_overall):
    count = Counter(sentiment_overall)
    print('The overall sentimenet is:', count)


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

    # list to save all utterances
    history = []
    sentiment_overall = []
    file1 = open("input.txt","r")
    utter = file1.readline()
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
            chatty(utter)
        elif choice == 1:
            doc = nlp(utter)
            sql_query = create_dictionary(utter, doc)
            generate_output(utter, sql_query, db)
        utter = input('> ')
        if utter == 'quit':
            break
        history.append(utter)
        sentiment_overall.append(get_polarity(utter))
        break

    get_sentiment_report(sentiment_overall)

    print("It was nice talking to you! Thank You")