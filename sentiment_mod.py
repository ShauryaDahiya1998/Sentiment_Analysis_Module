import nltk
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

class VoteClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers = classifiers

    def classify(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self,features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf



#This makes a list of different words in the different categories of movies. A neat way to make a list
#This is the data set which we use to compare against
#From this we create the traning and testing sets
short_pos = open("positive.txt","r").read()
short_neg = open("negative.txt","r").read()

documents = []


all_words = []
short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

#  j is adjective, r is adverb, and v is verb
# allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in short_pos.split('\n'):
    documents.append((p, "pos"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

for p in short_neg.split('\n'):
    documents.append((p, "neg"))
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
all_words = nltk.FreqDist(all_words)

#to check how many time a perticcular word comes up
#print(all_words['bad'])

word_features = list(all_words.keys())[:2500]


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]
random.shuffle(featuresets)

training_set = featuresets[:2500]
testing_set =  featuresets[2500:5000]
# posterior = prior occurences x liklihood / evidence = aive bayes algo
#the naive bayes algo
classifier = nltk.NaiveBayesClassifier.train(training_set)

#reading the pickled classifier
#classifier_f = open("naivebayes.pickle","rb")
#classifier = pickle.load(classifier_f)
#classifier_f.close()


#pickling the classifier
'''save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()'''

#MNB_Classifier
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)

#bernoulli
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier .train(training_set)

#SVC_classifier = SklearnClassifier(SVC())
#SVC_classifier.train(training_set)
#print("SVC_classifier Algo accuracy: ", (nltk.classify.accuracy(SVC_classifier,testing_set))*100)

#NuSVC_classifier = SklearnClassifier(NuSVC())
#NuSVC_classifier.train(training_set)
#print("NuSVC_classifier Algo accuracy: ", (nltk.classify.accuracy(NuSVC_classifier,testing_set))*100)

voted_classifier = VoteClassifier(classifier,MNB_classifier,BernoulliNB_classifier,LogisticRegression_classifier,SGDClassifier_classifier)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
