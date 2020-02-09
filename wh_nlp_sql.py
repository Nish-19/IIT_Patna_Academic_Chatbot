import spacy
roll_number = '1801cs01'

def create_sql(sql):
	if sql['Condition_val_type'] == 'XXddd':
		sql_query = 'SELECT ' + sql['Condition_val'].text + ' FROM table_name ' + 'WHERE Roll_number = ' + roll_number + ';'
	else:
		roll_number1 = roll_number
		if sql['Condition_val_type'] == 'ddddxxdd':
			roll_number1 = sql['Condition_val'].text
		sql_query = 'SELECT ' + sql['Select'].text + ' FROM table_name ' + 'WHERE Roll_number = ' + roll_number1 + ';'
		if len(sql['additional']) > 0:
			sql['Select'] = sql['additional'][0].text + '_' + sql['Condition_val'].text + '_' + sql['Select'].text
			sql_query = 'SELECT ' + sql['Select'] + ' FROM table_name ' + 'WHERE Roll_number = ' + roll_number1 + ';'
	print(sql_query)



def dfs(vertex,past,summary, sql):
	
	if summary[vertex.text]['Dep']=='nsubj' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex
	elif summary[vertex.text]['Dep']=='attr' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex
	elif summary[vertex.text]['Dep']!='pobj' and summary[vertex.text]['Dep']!='det' and summary[past.text]['Dep']=='pobj':
		sql['Condition_val']=past
		sql['Condition_val_type'] = vertex.shape_
		sql['additional'].append(vertex)
	elif summary[vertex.text]['Dep']=='pobj' and len(summary[vertex.text]['Children'])==0 and len(sql['Select'].text)!=0:
		sql['Condition_val']=vertex
		sql['Condition_val_type']=vertex.shape_
	for child in summary[vertex.text]['Children']:
		dfs(child,vertex,summary, sql)



def create_dictionary(doc):
	summary = dict()
	root = ''
	#sql = dict()
	for token in doc:
		lst = [child for child in token.children]
		print(lst)
		if token.dep_ == 'ROOT':
			#root = token.text
			root = token
		summary[token.text] = {'Children' : lst, 'Dep' : token.dep_}

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
	dfs(root, root, summary, sql)
	print(sql)
	print(summary)
	create_sql(sql)

if __name__ == '__main__':
	in_path = 'E:/4thSem/inno_lab/wh_questions.txt'
	nlp = spacy.load("en_core_web_sm")
	with open(in_path) as f:
		sentences = f.read().split('\n')
	for i, sentence in enumerate(sentences):
		if sentence is not '':
			doc = nlp(sentence)
			#if i != 2:
			create_dictionary(doc)
