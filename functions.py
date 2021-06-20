from textblob import TextBlob
import re

# a function to clean the tweets
def cleanTxt(text):
	text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
	text = re.sub('#', '', text) # Removing '#' hash tag
	text = re.sub('RT[\s]+', '', text) # Removing RT
	text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
	
	return text




# function to get subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# function to get the polarity
def getPolarity(text):
    return  TextBlob(text).sentiment.polarity


def getAnalysis(score):
    if score < 0:
        return 'Negative'

    elif score == 0:
        return 'Neutral'


    else:
        return 'Positive'
