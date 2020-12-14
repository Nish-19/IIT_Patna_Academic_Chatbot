import spacy
import numpy as np
import pandas as pd

nlp = spacy.load('en_core_web_lg')
question_data = pd.read_csv('question_data.csv')

#Computing the word vector representations for all sentences

with nlp.disable_pipes():
	vectors = np.array([nlp(text).vector for text in question_data.question])

def cosine_similarity(a, b):
	return a.dot(b)/np.sqrt(a.dot(a)*b.dot(b))

def find_similarity(input_query):
	#input_query = input('Enter the query\n')
	input_vector = nlp(input_query).vector
	similarity = list()

	mean_vec = vectors.mean(axis = 0)
	centered = vectors - mean_vec

	similarity = [cosine_similarity(vector, (input_vector - mean_vec)) for vector in centered]

	print(similarity)
	print('The maximum similarity is with:')
	question_order = [question_data.question[similarity.index(element)] for element in sorted(similarity, reverse = True)]
	print(question_order[:3])
	print(sorted(similarity, reverse = True)[:3])
	#print(question_data.question[similarity.index(max(similarity))])