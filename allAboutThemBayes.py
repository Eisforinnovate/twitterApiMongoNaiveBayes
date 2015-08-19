import nltk
import pandas as pd
import csv

# training data set , manually annotated 
# defining positive tweets list . This can be a database 
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

# defining negative tweets list . This can be a database
neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]

# merging the two list in one big training tuple and filtering two letters words 
tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))

# defining test tweets list
test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]

# getting word frequencies from the training data 

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


print get_words_in_tweets(tweets)
print get_word_features(get_words_in_tweets(tweets))
word_features = get_word_features(get_words_in_tweets(tweets))

# building a feature extractor
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

# building the training set
training_set = nltk.classify.apply_features(extract_features, tweets)

# training the classifier 
classifier = nltk.NaiveBayesClassifier.train(training_set)

def loadCsv(filename):
  lines = csv.reader(open(filename, "a"))
  dataset = list(lines)
  for i in range(len(dataset)):
    dataset[i] = [float(x) for x in dataset[i]]
  return dataset

#needed pandas to read csv
#ran into encoding problems here...probs how I exported as CSV
#next time i will just read over from pymongo  
dataset = pandas.read_csv("a.csv", lineterminator='\n',encoding='utf-16', header=None)
df = pd.read_csv("a.csv", lineterminator='\n',encoding='utf-16', header=None)
#df
tweet = dataset
print classifier.classify(extract_features(tweet.split()))