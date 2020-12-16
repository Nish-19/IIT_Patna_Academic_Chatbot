import spacy
import csv

def find_tags(doc, out_path):
	with open(out_path, 'w') as f:
		f.write("Text,Lemma,POS,Tag,Dep,Shape,is alpha,is stop\n")
		for token in doc:
			f.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(token.text, token.lemma_, token.pos_,
			token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))
			print(token.text, token.lemma_, token.pos_,
			token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

def find_dependency(sentence, out_path):
	with open(out_path, 'w') as f:
		f.write("Token.text,Token.Dep,Head Text,Head Pos,Children\n")
		for token in doc:
			f.write("%s,%s,%s,%s,%s\n"%(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children]))		

if __name__ == '__main__':
	pos_path = 'E:\\4thSem\\inno_lab\\POS_Results'
	dependency_path = 'E:\\4thSem\\inno_lab\\Dependency_Results'
	in_path = 'E:/4thSem/inno_lab/sample_question.txt'
	sentences = list()
	nlp = spacy.load("en_core_web_sm")
	with open(in_path) as f:
		sentences = f.read().split('\n')
	for i, sentence in enumerate(sentences):
		if sentence is not '':
			doc = nlp(sentence)
			print(sentence)
			pos_file_out_path = pos_path + '\\' + str(i) + '.csv'
			dependency_file_out_path = dependency_path + '\\' + str(i) + '.csv'
			find_tags(doc, pos_file_out_path)
			find_dependency(doc, dependency_file_out_path)
	#find_tags(sentence)
