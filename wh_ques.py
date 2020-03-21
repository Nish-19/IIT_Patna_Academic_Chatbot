import spacy
roll_number = '1401cs01'

def create_sql(sql, flag):
	sql_condition_dict = {}

	if flag==2:
		sql_query = 'SELECT name' + ' FROM table_name '
	elif flag==3:
		sql_query = 'SELECT COUNT(DISTINCT ' + sql['Select'] + ') FROM table_name '
	else:
		sql_query = 'SELECT ' + sql['Select'] + ' FROM table_name '
	sql_condition = 'WHERE '
	for i, condition in enumerate(sql['Condition_val_type']):
		if condition == 'XXddd':
			sql_condition_dict['subno'] = '\'' + sql['Condition_val'][i] + '\''
		elif condition == 'ddddxxdd' or condition == 'ddddXXdd':
			sql_condition_dict['rollno'] = '\'' + sql['Condition_val'][i] + '\''
		elif flag==2:
			sql_condition_dict['state'] = '\'' + sql['Condition_val'][i] + '\''

	if flag==3:
		for i,condition in enumerate(sql['additional']):
			if condition.shape_=='xx' or condition.shape_=='xxx':
				sql_condition_dict['branch'] = '\'' + sql['additional'][i].text + '\''
			elif condition.shape_=='xxddd':
				sql_condition_dict['subno'] = '\'' + sql['additional'][i].text + '\''
			elif condition.shape_=='dddd':
				sql_condition_dict['year'] = '\'' + sql['additional'][i].text + '\''
			else:
				sql_condition_dict['semester'] = '\'' + sql['additional'][i].text + '\''
 
	if flag==2:#hardcoded meanings of certain words as per field names in database, to be extended...
		if sql['Select']=='topper':#i have assumed that we have the max score of a subject already calculated.
			sql_condition_dict['grade']= '(SELECT MAX(grade) FROM table_name WHERE subno=' + sql_condition_dict['subno'] + ')'
		elif sql['Select']=='lowest':
			sql_condition_dict['grade']= '(SELECT MIN(grade) FROM table_name WHERE subno=' + sql_condition_dict['subno'] + ')'
		elif sql['Select']=='instructor':
			sql_condition_dict['status']= '\'' + sql['Select'] + '\''
	

	for condition_pair in sql['additional']:
		if flag==0:
			for key, value in condition_pair.items():
				sql_condition_dict[key] = '\'' + value + '\''
		# elif flag==2:
		# 	for vertex in sql['additional']:#optimise using pos , lemma
		# 		if vertex == 'lowest':
		# 			temp=sql['Select']
		# 			sql['Select']='MIN(' + temp + ')'
		# 		elif vertex == 'highest':
		# 			temp=sql['Select']
		# 			sql['Select']='MAX(' + temp + ')'



	if 'rollno' not in sql_condition_dict.keys() and flag == 0:
		sql_condition_dict['rollno'] = '\'' + roll_number + '\''
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

def dfsForHowMany(vertex,past,summary,sql):

	if vertex.shape_=='dddd' or summary[vertex.text]['Dep']=='nummod' or (summary[vertex.text]['Dep']=='amod' and summary[past.text]['Dep']=='pobj'):
		sql['additional'].append(vertex)
	elif vertex.shape_=='xx' and (summary[vertex.text]['Dep']=='pobj' or summary[vertex.text]['Dep']=='compound'):
		sql['additional'].append(vertex)
	for child in summary[vertex.text]['Children']:
		dfsForHowMany(child,vertex,summary,sql)

def dfs(vertex,past,summary, sql):
	
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
		dfs(child,vertex,summary, sql)

def dfsForWho(vertex,past,summary,sql):
	
	if summary[vertex.text]['Dep']=='attr' and vertex.text!='what' and vertex.text!='who' and len(sql['Select'])==0:
		sql['Select']=vertex.text
	elif (summary[vertex.text]['Dep']=='pobj' or (summary[vertex.text]['Dep']=='nummod' and summary[past.text]['Dep']=='attr') )  and len(summary[vertex.text]['Children'])==0:
		sql['Condition_val'].append(vertex.text)
		sql['Condition_val_type'].append(vertex.shape_)
	elif summary[vertex.text]['Dep']=='advmod' and len(sql['Select'])==0:
		sql['Select']=vertex.text
	for child in summary[vertex.text]['Children']:
		dfsForWho(child,vertex,summary,sql)

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

howMany=0
sql = dict()

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

	
	sql['additional'] = []
	sql['Condition_val'] = []
	sql['Condition_val_type'] = []
	whoFlag = 0
	flag = 0
	for child in summary[root.text]['Children']:
		if child.text == 'who':
			whoFlag = 1
	if root.text == 'List':
		list_sql_extract(summary, sql)
		flag = 1
	elif whoFlag==1:
		dfsForWho(root,root,summary,sql)
		flag = 2
	elif howMany==1:
		dfsForHowMany(root,root,summary,sql)
		flag=3
	else:
		dfs(root, root, summary, sql)
		flag = 0
	print(sql)
	print(summary)
	create_sql(sql, flag)

if __name__ == '__main__':
	#in_path = 'E:/4thSem/inno_lab/wh_questions.txt'
	in_path = '/home/vaibhavgakhreja/Desktop/machine learning/NLP/questions.txt'
	nlp = spacy.load("en_core_web_sm")
	with open(in_path) as f:
		sentences = f.read().split('\n')

	for i, sentence in enumerate(sentences):
		if sentence is not '':
			sentence=sentence.lower()
			doc = nlp(sentence)
			data = sentence.split()
			cnt=0
			for token in data:
				if cnt==2 and howMany==0:
					howMany=1
					sql['Select']=token
				if token=='how' or token=='many' :
					cnt=cnt+1
			create_dictionary(doc)
		howMany=0
