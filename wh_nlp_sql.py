import spacy
from python_sql_connector import *
roll_number = '1401cs01'

cols = ['rollno', 'semno', 'year', 'subno', 'crd', 'grade', 'date_of_entry', 'sub_type']

def create_sql(sql, flag):
	sql_query = 'SELECT ' + sql['Select'] + ' FROM sem_grades '
	sql_condition = 'WHERE '
	sql_condition_dict = {}
	for i, condition in enumerate(sql['Condition_val_type']):
		if condition == 'XXddd' or condition == 'xxddd':
			sql_condition_dict['subno'] = '\'' + sql['Condition_val'][i] + '\''
		elif condition == 'ddddxxdd' or condition == 'ddddXXdd':
			sql_condition_dict['rollno'] = '\'' + sql['Condition_val'][i] + '\''
	for condition_pair in sql['additional']:
		for key, value in condition_pair.items():
			sql_condition_dict[key] = '\'' + value + '\''
	# if 'rollno' not in sql_condition_dict.keys() and flag == 0:
	# 	sql_condition_dict['rollno'] = '\'' + roll_number + '\''
	for i, condition in enumerate(sql_condition_dict):
		if i == 0:
			sql_condition = sql_condition + condition + ' = ' + sql_condition_dict[condition]
		else:
			sql_condition = sql_condition + ' AND ' + condition + ' = ' + sql_condition_dict[condition]
	sql_condition = sql_condition + ';'
	sql_query = sql_query + sql_condition

	# if sql['Condition_val_type'] == 'XXddd':
	# 	sql_query = 'SELECT ' + sql['Select'].text + ' FROM table_name ' + 'WHERE rollno = ' + roll_number + ' AND ' + 'subno = ' + sql['Condition_val'].text + ';'
	# else:
	# 	roll_number1 = roll_number
	# 	if sql['Condition_val_type'] == 'ddddxxdd':
	# 		roll_number1 = sql['Condition_val'].text
	# 	sql_query = 'SELECT ' + sql['Select'].text + ' FROM table_name ' + 'WHERE Roll_number = ' + roll_number1 + ';'
	# 	if len(sql['additional']) > 0:
	# 		sql['Select'] = sql['additional'][0].text + '_' + sql['Condition_val'].text + '_' + sql['Select'].text
	# 		sql_query = 'SELECT ' + sql['Select'] + ' FROM table_name ' + 'WHERE Roll_number = ' + roll_number1 + ';'
	print(sql_query)
	generate_output(sql_query, db)



def dfs_what(vertex,past,summary, sql):
	
	if summary[vertex.text]['Dep']=='nsubj' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex.text
	elif summary[vertex.text]['Dep']=='attr' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex.text
	elif summary[vertex.text]['Dep']!='pobj' and summary[vertex.text]['Dep']!='det' and summary[past.text]['Dep']=='pobj':
		sql['Condition_val']=past.text
		sql['Condition_val_type'] = vertex.shape_
		sql['additional'].append(vertex)
	elif summary[vertex.text]['Dep']=='pobj' and len(summary[vertex.text]['Children'])==0 and len(sql['Select'])!=0:
		sql['Condition_val'].append(vertex.text)
		sql['Condition_val_type'].append(vertex.shape_)
	for child in summary[vertex.text]['Children']:
		dfs_what(child,vertex,summary, sql)

def list_sql_extract(summary, sql):
	for token, value in summary.items():
		if value['Dep'] == 'dobj' and value['is_stop'] == False:
			sql['Select'] = token
		if value['Dep'] == 'pobj' and len(value['Children']) == 0:
			sql['Condition_val'].append(token)
			sql['Condition_val_type'].append(value['Shape'])
		if value['Dep'] == 'pobj' and len(value['Children']) != 0:
			if summary[value['Children'][0].text]['Dep'] != 'acl': 
				sql['additional'].append({token : value['Children'][0].text})

def which_sql_extract(summary, sentence, sql):
	imax = 99999
	elements = sentence.split()
	for i, element in enumerate(elements):
		if element in cols and i < imax:
			sql['Select'] = element
			imax = i
		elif element in cols:
			sql['additional'].append({element : elements[i+1]})
		elif element == 'my':
			sql['additional'].append({'rollno' : roll_number})
	for token, value in summary.items():
		if value['Shape'] == 'XXddd' or value['Shape'] == 'xxddd' or value['Shape'] == 'ddddxxdd' or value['Shape'] == 'ddddXXdd':
			sql['Condition_val'].append(token)
			sql['Condition_val_type'].append(value['Shape']) 


def create_dictionary(sentence, doc):
	summary = dict()
	root = ''
	#sql = dict()
	for token in doc:
		lst = [child for child in token.children]
		print(lst)
		if token.dep_ == 'ROOT':
			#root = token.text
			root = token
		summary[token.text] = {'Children' : lst, 'Dep' : token.dep_, 'Shape' : token.shape_, 'is_stop' : token.is_stop}

	# for child in summary[root]['Children']:
	# 	print(type(child))
	# 	if summary[child.text]['Dep'] == 'nsubj':
	# 		sql['Select'] = child
	# 		for child1 in summary[str(child)]['Children']:
	# 			if summary[str(child1)]['Dep'] == 'prep':
	# 				for child2 in summary[str(child1)]['Children']:
	# 					sql['Condition_val'] = child2
	# 					sql['Condition_val_type'] = child2.shape_
	# 					sql['additional'] = []
	# 					for child3 in summary[str(child2)]['Children']:
	# 						if child3.dep_ != 'det':
	# 							sql['additional'].append(child3)
	sql = dict()
	sql['additional'] = []
	sql['Condition_val'] = []
	sql['Condition_val_type'] = []
	if root.text == 'List':
		list_sql_extract(summary, sql)
		flag = 1
	elif 'which' in sentence or 'Which' in sentence:
		which_sql_extract(summary, sentence, sql)
		flag = 3
	else:
		dfs_what(root, root, summary, sql)
		if 'my' in sentence:
			sql['additional'].append({'rollno' : roll_number})
		flag = 0
	print(sql)
	print(summary)
	create_sql(sql, flag)

if __name__ == '__main__':
	#in_path = 'E:/4thSem/inno_lab/wh_questions.txt'
	in_path = 'E:/4thSem/inno_lab/which_questions.txt'
	db = initialise_database_connection()	#Used for connecting with database.
	nlp = spacy.load("en_core_web_sm")
	with open(in_path) as f:
		sentences = f.read().split('\n')
	for i, sentence in enumerate(sentences):
		if sentence is not '':
			doc = nlp(sentence)
			create_dictionary(sentence, doc)
