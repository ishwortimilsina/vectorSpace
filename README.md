* In this assignment, I implemented a toy "search engine". 

* More specifically, this code will read a corpus and produce TF-IDF vectors for documents in the corpus. 

* Then, given a query string, this code will compute the cosine similarity between the query vector and 
the document vectors and return the document that gets the highest similarity score.

* The code is written in python.

* The text files to work on are in ./presedential_debates directory

* I have used nltk library for text processing

- createcollection() function will create a collection of idfs of all the unique words in the corpus
- getidf() function is used to calculate idf of a word when the particular word and total number of words and total number of documents is given
- getcount() function is to find out the total occurences of a word in all the documents
- getquerytf() function is used to find the normalized tfidf of words in a query
- getdoctfidf() function is used to find the normalized tfidf of all the words in a document
- docdocsim() function finds the cosine similarity between two documents
- querydocsim() function finds the cosine similarity between a query and a document
- query() function is for finding the document with highest similarity score with a query
