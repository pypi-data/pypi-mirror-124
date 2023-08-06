import tensorflow as tf
import string
import re
import nltk

def clean_up(text):
    nltk.download('wordnet')
    stopWords = nltk.corpus.stopwords.words('english') 
    wn = nltk.WordNetLemmatizer()
    noPunctText = "".join([c for c in str(text) if c not in string.punctuation]) #remove punctuation
    tokens = re.split('\W+', str(noPunctText)) #Use the punctuation-free text to split into separate words
    noStopWords = [word for word in tokens if word not in stopWords] #remove stop words e.g 'and'
    text_nsw = [each_string.lower() for each_string in noStopWords] #make all the words lowercase
    lem_text = [wn.lemmatize(word) for word in text_nsw] #lemmatize the words (i.e bring the words back to their roots)
    return lem_text