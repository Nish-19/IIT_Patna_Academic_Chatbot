import pandas as pd
orig_file = pd.read_csv('question_data.csv')
feedback_file = pd.read_csv('class_feedback.csv')
feedback_file.columns = ["question", "label"]
all_questions = orig_file['question'].tolist()
all_labels = orig_file["label"].tolist()
new_questions = feedback_file['question'].tolist()
new_labels = feedback_file['label'].tolist()
for i, question in enumerate(new_questions):
	if question not in all_questions:
		all_questions.append(question)
		all_labels.append(new_labels[i])

new_df = pd.DataFrame()
new_df['question'] = all_questions
new_df['label'] = all_labels
new_df.to_csv('question_data_up.csv', index = False)