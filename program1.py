import os
import re, math
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
import time

def createcollection():
	collection_time = time.time()
	count = 0
	for filename in os.listdir(corpus_root):
		with open(os.path.join(corpus_root, filename), 'r', encoding='utf-8') as file:
			doc = file.read()
			file.close()
			doc = doc.lower()
			tokens = tokenizer.tokenize(doc)

			tokens = [term for term in tokens if term not in stop_words]
			tokens = [stemmer.stem(term) for term in tokens]

			collection[filename] = tokens
			count = count+len(collection[filename])

			freqs = {}

			for word in tokens:
				freqs[word] = freqs.get(word, 0)

			for word in freqs:
				if word not in doccount:
					doccount[word] = 1
				else:
					doccount[word] = doccount[word] + 1

	print ("Finished creating collection")

	print ("%s words found" %count)

	for word in doccount:
		idf[word] = getidf(word)

	print ("Collection creation time %s" %(time.time() - collection_time))

###### Function to find the inverse document frequency of a word
def getidf(token):
	#total number of documents in which the token exists
	if token not in doccount:
		token = stemmer.stem(token)

	nt = doccount[token]
	if (nt > 0):
		ratio = float(N)/nt
	else:
		return 0

	idf = math.log10(ratio)

	return idf

###### Function to find out the total occurence of a word in all the documents
def getcount(token):
	count = 0
	token = stemmer.stem(token)
	for line in collection:
		for word in collection[line]:
			if (word == token):
				count = count+1
	return count

###### Function to find the normalized tfidf of words in a query
def getquerytf(text):
	text = text.lower()
	freqs = {}
	
	tokens = tokenizer.tokenize(text)
	
	tokens = [term for term in tokens if term not in stop_words]
    
	tokens = [stemmer.stem(term) for term in tokens]

	for word in tokens:
		freqs[word] = freqs.get(word, 0) + 1

	rootmeansquare = 0
	for word in freqs:
		if (freqs[word] > 0):
			freqs[word] = 1 + float(math.log10(freqs[word]))
			rootmeansquare = rootmeansquare + float(math.pow(freqs[word], 2))
		else:
			freqs[word] = 0

	for word in freqs:
		if (freqs[word] > 0):
			freqs[word] = freqs[word]/float(math.sqrt(rootmeansquare))

	return freqs

####### Function to find the normalized tfidf of all the words in a document
def getdoctfidf(filename):	
	counts = {}
	tfidf = {}
	normtfidf = {}

	for word in collection[filename]:
		counts[word] = counts.get(word, 0) + 1

	#print (counts)

	rootmeansquare = 0
	for word in counts:
		tfidf[word] = (1 + math.log10(float(counts[word]))) * idf[word]
		rootmeansquare = rootmeansquare + math.pow(tfidf[word], 2)
	
	for word in counts:
		normtfidf[word] = tfidf[word]/math.sqrt(rootmeansquare)

	return normtfidf

###### Function to find the cosine similarity between two documents
def docdocsim(filename1,filename2):
	doctfidf1 = getdoctfidf(filename1)
	doctfidf2 = getdoctfidf(filename2)

	tfidffinal = 0.0

	for word in doctfidf1:
		if word in doctfidf2:
			tfidffinal= tfidffinal + (doctfidf1[word] * doctfidf2[word])
		else:
			continue

	return tfidffinal

####### Function to find the cosine similarity between a query and a document
def querydocsim(qstring,filename):
	query = qstring.lower()

	querytfidf = getquerytf(query)

	doctfidf = getdoctfidf(filename)

	tfidffinal = 0.0

	tokens = tokenizer.tokenize(qstring)

	tokens = [term for term in tokens if term not in stop_words]
    
	tokens = [stemmer.stem(term) for term in tokens]

	for word in tokens:
		if word in doctfidf:
			tfidffinal= tfidffinal + (float(doctfidf[word]) * float(querytfidf[word]))
		else:
			continue
	
	return tfidffinal

####### Function to find the document with highest similarity score with a query
def query(qstring):
	query = qstring.lower()

	querytfidf = getquerytf(query)

	tokens = tokenizer.tokenize(qstring)

	tokens = [term for term in tokens if term not in stop_words]
    
	tokens = [stemmer.stem(term) for term in tokens]

	comp = {}
	for filename in collection:
		tfidffinal = 0.0
		doctfidf = getdoctfidf(filename)
		for word in tokens:
			if word in doctfidf:
				tfidffinal= tfidffinal + (float(doctfidf[word]) * float(querytfidf[word]))
				comp[filename] = tfidffinal
			else:
				continue

	best = 0
	for filename in comp:
		if (comp[filename] > best):
			best = comp[filename]

	for filename in comp:
		if (comp[filename] == best):
			print (filename)
			break
	return 0

########################################################
######################### MAIN #########################
########################################################

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
stemmer = PorterStemmer()

stop_words = stopwords.words('english')

corpus_root = './presidential_debates'

WORD = re.compile(r'\w+')

collection = {}
idf = {}
doccount = {}

N = len(os.listdir(corpus_root))

createcollection()