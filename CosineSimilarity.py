"""
This module weight query (terms) against documents with cosine similarity
"""

import math
from tfidfCalc import TFIDF_Calc

class CosSimilarity:
    def __init__(self):
        self.tfidfcalc = TFIDF_Calc()

    def cos_ranking(self, query: list, inverted_index: dict, tag_index: dict, num_docs: int) -> dict:
        """
        Params:
            - query: list of terms
            - inverted index: {term: {docID: tfidf, }, }
            - tag_index: {term: {docID: tag_weight,}, }
            - num_docs: number of documents in corpus
        """


        # calculate weight for each term
        query_vec = dict()  # query vector
        query_len = 0

        doc_vec = dict()  # doc vector
        doc_len = 0
        
        for term in query:
            if term in inverted_index:
                query_vec[term] = self.tfidfcalc.query_tf_idf(term, query, num_docs, inverted_index)
                query_len += math.pow(query_vec[term], 2)

                for docID, tfidf in inverted_index[term].items():
                    if not term in doc_vec:
                        doc_vec[term] = dict()

                    if not docID in doc_vec[term]:
                        doc_vec[term][docID] = tfidf

                    else:
                        doc_vec[term][docID] += tfidf

                    doc_len += math.pow(tfidf, 2)

        Scores = dict()
        for term in query_vec:
            for docID in doc_vec[term]:
                if not docID in Scores:
                    Scores[docID] = (query_vec[term] / math.sqrt(query_len)) * (doc_vec[term][docID]/math.sqrt(doc_len))
                else:
                    Scores[docID] += (query_vec[term] / math.sqrt(query_len)) * (doc_vec[term][docID]/math.sqrt(doc_len))
                
                Scores[docID] += (tag_index[term][docID] / 3)

        # increase scores for pages that have both terms
        """
        for term in query_vec:
            for docID in list(Scores):
                if docID in doc_vec[term]:
                    Scores[docID] = Scores[docID] * math.sqrt(len(query))
                else:
                    Scores[docID] = Scores[docID] / (math.sqrt(len(query)) * 3)
        """

        top_scores = sorted(Scores.items(), key=lambda x: x[1], reverse=True)

        return top_scores


        
                    
                

