import pandas as pd 
import spacy
import numpy as np

nlp = spacy.load('en_core_web_lg')

question_data = pd.read_csv('question_data.csv')
print(question_data.head())

with nlp.disable_pipes():
	doc_vectors = np.array([nlp(text).vector for text in question_data.question])

print(doc_vectors.shape)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(doc_vectors, question_data.label,
                                                    test_size=0.25, random_state=1)

from sklearn.svm import LinearSVC

# Set dual=False to speed up training, and it's not needed
svc = LinearSVC(random_state=1, dual=False, max_iter=10000)
svc.fit(X_train, y_train)
print(f"Accuracy: {svc.score(X_test, y_test) * 100:.3f}%", )
result = svc.predict(X_test)
X_test_questions = list()
for vector in X_test:
	for i, vec in enumerate(doc_vectors):
		if np.array_equal(vector, vec):
			X_test_questions.append(question_data.question[i])

for i in range(len(result)):
	print(X_test_questions[i],'\t',result[i])

