import os
from bs4 import BeautifulSoup
from Tokenizer import Tokenizer
from tfidfCalc import TFIDF_Calc
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
import nltk
import pickle
import json
import os, sys
nltk.download(['stopwords', 'words', 'wordnet'])


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
os.chdir(SCRIPT_DIR)


"""
This module will create the inverted index for corpus
"""

class InvertedIndex:
    def __init__(self):
        self.inverted_index = dict()
        self.numWords_docs_map = dict()
        self.tokenizer = Tokenizer()
        self.tfidf_calc = TFIDF_Calc()

        self._stopWords = set(stopwords.words('english'))
        self._englishWords = set(words.words())
        self._lemmatizer = WordNetLemmatizer()

        self.tag_index = dict()  # similar to inverted index but with tag weights

        # html tag heuristic
        self.tag_rank = {
            'title': 1.5,
            'h1': 1.4,
            'h2': 1.3,
            'h3': 1.2,
            'b': 1.2,
            'strong': 1.2,
            'em': 1,
            'a': 1,
            'p': 1,
            'img': 1,
            'ul': 1,
            'ol': 1,
            '': 1
        }

        # import bookkeeping
        with open('bookkeeping.json') as json_file:
            self.bookkeeping = json.load(json_file)



    def _append_inverted_index(self, word, docID):
        """
        Format: {term: {docID: count, }, }
        """

        if word not in self.inverted_index:
            self.inverted_index[word] = dict()
            self.inverted_index[word][docID] = 1
        else:
            if docID not in self.inverted_index[word]:
                self.inverted_index[word][docID] = 1
            else:
                self.inverted_index[word][docID] += 1
    
    def _append_tag_index(self, word, docID, tag):
        """
        Format: {term, {docID: tag_weights, }, }
        """

        if word not in self.tag_index:
            self.tag_index[word] = dict()
            self.tag_index[word][docID] = self.tag_rank[tag]
        else:
            if docID not in self.tag_index[word]:
                self.tag_index[word][docID] = self.tag_rank[tag]
            else:
                # compare tag weights
                # replace previous one if larger
                if self.tag_rank[tag] > self.tag_index[word][docID]:
                    self.tag_index[word][docID] = self.tag_rank[tag]
        



    def run(self):
        current = os.getcwd()
        # print(current)
        pt=os.path.join(current, 'WEBPAGES_RAW')

        COUNTER = 0
        for folder in os.listdir(pt):
            if (os.path.isfile(os.path.join(pt, folder)) == False):
                folder_path = os.path.join(pt, folder)
                for page in os.listdir(folder_path):
                    with open(os.path.join(folder_path, page), 'r', encoding='utf-8') as file:
                        soup = BeautifulSoup(file.read(), 'html.parser')
                        texts = soup.find_all(text=True) # extract html plain text segments/list
                        clean_text = ''.join(t.text for t in texts) # combine text segments
                        
                        tokenize_list = []
                        for text in texts:
                            parent_tag = text.parent.name
                            for token in self.tokenizer.tokenize(text.text):
                                tokenize_list.append((token, parent_tag))


                        # get key
                        key = str(folder) + "/" + str(page)  # key to access url in bookkeeping.json

                        ## append words to inverted index
                        word_count = 0
                        for token, parent_tag in tokenize_list:
                            # lemmitize token
                            lem_token = self._lemmatizer.lemmatize(token)

                            # add word if valid english words and not stop words
                            if ((len(lem_token) > 1) and (not lem_token in self._stopWords)):
                                self._append_inverted_index(lem_token, key)

                                parent_tag = '' if parent_tag not in self.tag_rank else parent_tag
                                self._append_tag_index(lem_token, key, parent_tag)
                            
                            word_count += 1
                        
                        self.numWords_docs_map[key] = word_count

                    print(key)
                    COUNTER += 1

        # modify inverted index to store tf-idfs
        self.inverted_index = self.tfidf_calc.calc_tf_idf(self.inverted_index, self.numWords_docs_map)
              
        #save dictionary
        with open("inverted_index.pkl", "wb") as file:
            pickle.dump(self.inverted_index, file, protocol=pickle.HIGHEST_PROTOCOL)

        with open("inverted_index.json", "w") as file:
            json.dump(self.inverted_index, file)

        with open("tag_index.pkl", "wb") as file:
            pickle.dump(self.tag_index, file, protocol=pickle.HIGHEST_PROTOCOL)
        
        with open("tag_index.json", "w") as file:
            json.dump(self.tag_index, file)

        
if __name__ == "__main__":
    inverted_index = InvertedIndex()
    inverted_index.run()