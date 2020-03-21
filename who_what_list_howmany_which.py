import spacy
roll_number = '1401cs01'

name_of_states = ['rajasthan','punjab','assam','bihar','karnataka','kerala']
cols = ['rollno', 'semno', 'year', 'subno', 'crd', 'grade', 'date_of_entry', 'sub_type']
replace = dict()
replace['subjects']='subno'
replace['subject']='subno'
replace['students']='rollno'
replace['student']='rollno'
replace['semester']='semno'
replace['one']='1'
replace['two']='2'
replace['three']='3'
replace['four']='4'
replace['first']='1'
replace['second']='2'
replace['third']='3'
replace['fourth']='4'
replace['five']='5'
replace['fifth']='5'

def create_sql(sql, flag):

	sql_condition_dict = {}
	if sql['Select'] in replace:
		sql['Select']=replace[sql['Select']]
	if flag==2:
		sql_query = 'SELECT name' + ' FROM table_name '
	elif flag==3:
		sql_query = 'SELECT COUNT(DISTINCT ' + sql['Select'] + ') FROM table_name '
	else:
		sql_query = 'SELECT ' + sql['Select'] + ' FROM table_name '
	
	sql_condition = 'WHERE '
	for i, condition in enumerate(sql['Condition_val_type']):
		if condition == 'xxddd':
			sql_condition_dict['subno'] = '\'' + sql['Condition_val'][i] + '\''
		elif condition == 'ddddxxdd':
			sql_condition_dict['rollno'] = '\'' + sql['Condition_val'][i] + '\''
		elif flag==2:
			sql_condition_dict['state'] = '\'' + sql['Condition_val'][i] + '\''

	if flag==3:
		for i,condition in enumerate(sql['additional']):
			if sql['additional'][i].text in replace:
				sql['additional'][i]=replace[sql['additional'][i].text]
			else:
				sql['additional'][i]=sql['additional'][i].text
			if condition.shape_=='xx' or condition.shape_=='xxx':
				sql_condition_dict['branch'] = '\'' + sql['additional'][i] + '\''
			elif condition.shape_=='xxddd':
				sql_condition_dict['subno'] = '\'' + sql['additional'][i] + '\''
			elif condition.shape_=='dddd':
				sql_condition_dict['year'] = '\'' + sql['additional'][i] + '\''
			elif condition.text in name_of_states:
				sql_condition_dict['state'] = '\'' + sql['additional'][i] + '\''
			else:
				sql_condition_dict['semno'] = '\'' + sql['additional'][i] + '\''

	if flag==2:
		if sql['Select']=='topper':
			sql_condition_dict['grade']= '(SELECT MAX(grade) FROM table_name WHERE subno=' + sql_condition_dict['subno'] + ')'
		elif sql['Select']=='lowest':
			sql_condition_dict['grade']= '(SELECT MIN(grade) FROM table_name WHERE subno=' + sql_condition_dict['subno'] + ')'
		elif sql['Select']=='instructor':
			sql_condition_dict['status']= '\'' + sql['Select'] + '\''

	if flag==0 or flag==1:
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
	print('Query : ',sql_query)

def dfsForHowMany(vertex,past,summary,sql):

	if vertex.shape_=='dddd' or summary[vertex.text]['Dep']=='nummod' or (summary[vertex.text]['Dep']=='amod' and summary[past.text]['Dep']=='pobj'):
		sql['additional'].append(vertex)
	elif vertex.shape_=='xx' and (summary[vertex.text]['Dep']=='pobj' or summary[vertex.text]['Dep']=='compound'):
		sql['additional'].append(vertex)
	elif vertex.shape_=='xxddd':
		sql['additional'].append(vertex)
	elif summary[vertex.text]['Dep']=='pobj':
		sql['additional'].append(vertex)
	for child in summary[vertex.text]['Children']:
		dfsForHowMany(child,vertex,summary,sql)

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
	elif vertex.text!='who' and ((summary[vertex.text]['Dep']=='pobj' or summary[vertex.text]['Dep']=='dobj' or (summary[vertex.text]['Dep']=='nummod' and summary[past.text]['Dep']=='attr') )  and len(summary[vertex.text]['Children'])==0):
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
listflag=0
whichFlag=0
sql = dict()

def create_dictionary(sentence,doc):
	summary = dict()
	root = ''
	for token in doc:
		lst = [child for child in token.children]
		# print(lst)
		if token.dep_ == 'ROOT':
			root = token
		summary[token.text] = {'Children' : lst, 'Dep' : token.dep_, 'Shape' : token.shape_, 'is_stop' : token.is_stop}
	if howMany==0:
		sql['Select']=''
	sql['additional'] = []
	sql['Condition_val'] = []
	sql['Condition_val_type'] = []
	whoFlag = 0
	flag = 0
	for child in summary[root.text]['Children']:
		if child.text == 'who':
			whoFlag = 1
	if listflag==1:
		list_sql_extract(summary, sql)
		flag = 1
	elif whoFlag==1:
		dfsForWho(root,root,summary,sql)
		flag = 2
	elif howMany==1:
		dfsForHowMany(root,root,summary,sql)
		flag=3
	elif whichFlag==1:
		which_sql_extract(summary,sentence,sql)
	else: 
		dfs(root, root, summary, sql)
		flag = 0

	if 'my' in sentence:
		sql['additional'].append({'rollno' : roll_number})
	# print(sql)
	# print(summary)
	create_sql(sql, flag)

if __name__ == '__main__':
	#in_path = 'E:/4thSem/inno_lab/wh_questions.txt'
	in_path = '/home/vaibhavgakhreja/Desktop/machine learning/NLP/questions.txt'
	nlp = spacy.load("en_core_web_sm")
	with open(in_path) as f:
		sentences = f.read().split('\n')

	for i, sentence in enumerate(sentences):
		if sentence is not '':
			print('Question : ',sentence)
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
				if token=='list':
					listflag=1
				if token=='which':
					whichFlag=1
			create_dictionary(sentence,doc)
		howMany=0
		listflag=0
		whichFlag=0