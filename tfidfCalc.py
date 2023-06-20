import math

############################################
#        W(t,d)= tf x log(N/df(t))         #
############################################

class TFIDF_Calc:
    def _calc_idf(self, term, num_docs, inverted_index):
        """
        This function, by passing in the term and total number of documents
        will return the idf value for that term
        """
        num_docs_with_term = len(inverted_index[term])
        return math.log(num_docs/num_docs_with_term)
    
    
    def query_tf_idf(self, term: str, query: list, num_docs: int, inverted_index: dict) -> float:
        """
        This function considers query as a document and calculate its tf-idf value
        """
        tf_val = 1 + math.log(query.count(term)) # logarithmically scaled freq
        #tf_val = query.count(term) / len(query)

        num_docs_with_term = len(inverted_index[term])# increment num of doc as counting query as doc
        idf_val = math.log(num_docs/num_docs_with_term)

        return tf_val * idf_val
    

    def calc_tf_idf(self, inverted_index, numWords_docs_map):
        """
        This function, by passing in the inverted index, will calculate
        the tf-idf values for all terms and return the frequency map
        """
        ## count the number of documents
        count_set = set()
        for key, value in inverted_index.items():
            for docID, freq in value.items():
                count_set.add(docID)
            
        
        num_docs = len(count_set)
        
        ## calculate idfs for terms
        idfs = dict()
        for term, docIDs in inverted_index.items():
            idfs[term] = self._calc_idf(term, num_docs, inverted_index)
            
        ## calculate tf_idfs
        tfidfs = dict()
        for term in inverted_index:
            for docID in inverted_index[term]:
                ## calculate tfs for terms
                tf = inverted_index[term][docID]  # number of times term t appers in the doc
                #tf_val = tf / numWords_docs_map[docID]  # / total number of terms in the doc
                tf_val = 1 + math.log(tf)  # logarithmically scaled freq
                
                idf_val = idfs[term]
                
                if term not in tfidfs:
                    tfidfs[term] = dict()
                
                tfidfs[term][docID] = tf_val * idf_val
                    
        return tfidfs 

if __name__ == "__main__":
    tfidf_calc = TFIDF_Calc()

    corpus = ["This this", "This This this This", "this, wrong", "this, I don't know", "this wrong or right", "thiswrong ", "love is love", "no love ok love love run away"]

    numWords_docs_map = dict()  # count the number of words in doc d {docID: #, }
    inverted_index = dict()

    num_docs = 0
    docID = 1
    for text in corpus:
        
        word_count = 0
        for word in text.split():
            if word not in inverted_index:
                inverted_index[word] = dict()
                inverted_index[word][docID] = 1
            else:
                if docID not in inverted_index[word]:
                    inverted_index[word][docID] = 1
                else:
                    inverted_index[word][docID] += 1
                    
            word_count += 1
            
        numWords_docs_map[docID] = word_count
        
        docID += 1

    print("map: " + str(tfidf_calc.calc_tf_idf(inverted_index, numWords_docs_map)))

