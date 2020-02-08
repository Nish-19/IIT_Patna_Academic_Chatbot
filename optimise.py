def dfs(vertex,past,summary):
	
	if summary[vertex.text]['Dep']=='nsubj' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex
	elif summary[vertex.text]['Dep']=='attr' and vertex.text!='what' and vertex.text!='who':
		sql['Select']=vertex
	elif summary[vertex.text]['Dep']!='pobj' and summary[vertex.text]['Dep']!='det' and summary[past.text]['Dep']=='pobj':
		sql['Condition_val']=past
		sql['Condition_val_type'] = past.shape_
		sql['additional']=vertex
	elif summary[vertex.text]['Dep']=='pobj' and len(summary[vertex.text]['Children'])==0 and len(sql['Select'].text)!=0:
		sql['Condition_val']=vertex
		sql['Condition_val_type']=past.shape_
	for child in summary[vertex.text]['Children']:
		dfs(child,vertex,summary)