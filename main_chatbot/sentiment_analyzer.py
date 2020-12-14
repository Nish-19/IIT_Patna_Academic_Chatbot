from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_polarity(text):
	analyser = SentimentIntensityAnalyzer()
	score = analyser.polarity_scores(text)
	sentiment = 0
	# if score['neg'] > score['pos'] and score['neg'] > score['neu']:
	# 	sentiment = -1
	# elif score['pos'] > score['neg'] and score['pos'] > score['neu']:
	# 	sentiment = 1
	# if score['neu'] > score['pos'] and score['neu'] > score['neg']:
	# 	sentiment = 0
	if score['compound'] > 0.05:
		sentiment = 1
	elif score['compound'] < -0.05:
		sentiment = -1
	else:
		sentiment = 0
	return sentiment

#print(get_polarity(input('Enter the text\n')))