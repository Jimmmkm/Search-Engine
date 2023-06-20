import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

import pickle
import json
from Tokenizer import Tokenizer
from CosineSimilarity import CosSimilarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class Search:

    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        self._tokenizer = Tokenizer()
        self._cosSimilarity = CosSimilarity()
        self._stopWords = set(stopwords.words('english'))

        with open("inverted_index.pkl", "rb") as file:
            self.inverted_index = pickle.load(file)

        with open("bookkeeping.json", "r") as file:
            self.url_data = json.load(file)

        with open("tag_index.pkl", "rb") as file:
            self.tag_index = pickle.load(file)


    def get_num_unique_words(self):
        return len(self.inverted_index)
    

    def get_num_unique_ids(self):
        count_set = set()
        for key, value in self.inverted_index.items():
            for docID, freq in value.items():
                count_set.add(docID)
            
        return len(count_set)

    def basic_search(self, term):
        """
        ***USED FOR DEBUG ONLY***
        Basic Search, could only handle one term query
        """
        lem_query = self._lemmatizer.lemmatize(term).lower()
        url_results = []

        results = self.inverted_index[lem_query]
        results = sorted(results.items(), key=lambda x: (-x[1], x[0]))[:20]

        url_results = []  # list of url results with format [(url, tf-idf), ]
        for key, tfidf in results:
            url_results.append((self.url_data[key], tfidf))

        return url_results
    

    def complex_search(self, query: list) -> dict:
        """
        Complex Search, could handle query with multiple terms

        params:
            - query: user query terms
        """
        
        ## count the number of documents
        count_set = set()
        for key, value in self.inverted_index.items():
            for docID, freq in value.items():
                count_set.add(docID)  
        num_docs = len(count_set)

        ## lemmetize query
        lem_query = []
        for term in query:
            lem_term = self._lemmatizer.lemmatize(term).lower()

            # add word if valid english words and not stop words
            if ((len(lem_term) > 1) and (not lem_term in self._stopWords)):
                lem_query.append(lem_term)

        ## cos similarity ranking
        print(len(self._cosSimilarity.cos_ranking(lem_query, self.inverted_index, self.tag_index, num_docs)))
        top_scores = self._cosSimilarity.cos_ranking(lem_query, self.inverted_index, self.tag_index, num_docs)[:20]

        url_results = []  # list of url results with format [(url, tf-idf), ]
        docList = []
        for key, tfidf in top_scores:
            docList.append(key)
            url_results.append((self.url_data[key], tfidf))

        return url_results, docList

    
    def run(self):
        query = input("Enter a Query: ")

        ## tokenize query
        query_list = self._tokenizer.tokenize(query)
        
        if len(query_list) >= 1:
            search_result = self.complex_search(query_list)[0]
        
        else:
            print("Invalid Query")

        rank = 1
        for url, tfidf in search_result:
            print("{rank}. {url}".format(rank=rank, url=url, tfidf=tfidf))
            rank += 1
    

if __name__ == "__main__":
    search = Search()
    while True:
        search.run()





