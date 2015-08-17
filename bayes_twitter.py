import nltk

#so we want to auto classify a tweet as positive or negative

#positive tweets
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]
#negative tweets
neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]
#take both lists and create single list of tuples
#each containing 2 elements
#first element is an array containing the workds
#second element is the type of setiment
#get rid of words smaller than 2 characters and we use
#lowecase for everything
tweets = []
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3] 
    tweets.append((words_filtered, sentiment))
#list of tweets
tweets = [
    (['love', 'this', 'car'], 'positive'),
    (['this', 'view', 'amazing'], 'positive'),
    (['feel', 'great', 'this', 'morning'], 'positive'),
    (['excited', 'about', 'the', 'concert'], 'positive'),
    (['best', 'friend'], 'positive'),
    (['not', 'like', 'this', 'car'], 'negative'),
    (['this', 'view', 'horrible'], 'negative'),
    (['feel', 'tired', 'this', 'morning'], 'negative'),
    (['not', 'looking', 'forward', 'the', 'concert'], 'negative'),
    (['enemy'], 'negative')]
#test tweets
test_tweets = [
    (['feel', 'happy', 'this', 'morning'], 'positive'),
    (['larry', 'friend'], 'positive'),
    (['not', 'like', 'that', 'man'], 'negative'),
    (['house', 'not', 'great'], 'negative'),
    (['your', 'song', 'annoying'], 'negative')]

#CLASSIFIER

#list of words features need to be extracted from the tweets
#list with every ditinct words ordered by frequency of appearance
#will use the following function to get the list + helper functions

word_features = get_word_features(get_words_in_tweets(tweets))

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
 #<FreqDist:
   # 'this': 6,
    #'car': 2,
    #'concert': 2,
    #'feel': 2,
    #'morning': 2,
    #'not': 2,
    #'the': 2,
    #'view': 2,
    #'about': 1,
    #'amazing': 1,
    #...
	#>
word_features = [
    'this',
    'car',
    'concert',
    'feel',
    'morning',
   	'not',
    'the',
    'view',
    'about',
    'amazing',
	]

#to create a classifier, need to decide what features most relevant
#to do
	#1st: need a feature extractor
	#here the input is the tweet
	#will use the word features list
	#defined above along with the input to create the dictionary 
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
#can apply the features to our classifier usering the method
#apply_features
training_set = nltk.classify.apply_features(extract_features, tweets)

#have our training set, can train our classifier
classifier = nltk.NaiveBayesClassifier.train(training_set)

def train(labeled_featuresets, estimator=ELEProbDist):
    ...
    # Create the P(label) distribution
    label_probdist = estimator(label_freqdist)
    ...
    # Create the P(fval|label, fname) distribution
    feature_probdist = {}
    ...
    return NaiveBayesClassifier(label_probdist, feature_probdist)
 def classify(self, featureset):
    # Discard any feature names that we've never seen before.
    # Find the log probability of each label, given the features.
    # Then add in the log probability of features given labels.
    # Generate a probability distribution dictionary using the dict logprod
    # Return the sample with the greatest probability from the probability
    # distribution dictionary
