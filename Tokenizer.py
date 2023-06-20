import sys
from nltk.stem import WordNetLemmatizer

class Tokenizer:
    def __init__(self):
        self.token_dict = dict()
        self._token_size = 0
        self._token_list = []

    def tokenize(self, content):
        """tokenize the content and return a list containing tokens"""
        sub_str = ""
        tokens_list = []
        for char in content:
            # if alphanumeric, continue adding substr
            # else the substr becomes one token and append to list
            if (char.isalnum() and char.isascii()):
                sub_str += char.lower()
            
            else:
                if (sub_str != ""):
                    tokens_list.append(sub_str)
                
                sub_str = ""
        
        # add the last token
        if (sub_str != ""):
            tokens_list.append(sub_str)
        
        self._token_size = len(tokens_list)
        self._token_list = tokens_list

        return tokens_list


    def computeWordFrequencies(self, content):
        """counts the number of occurrences of each 
        token in the token list."""
        tokens_list = self.tokenize(content)


        for token in tokens_list:
            # if map does not contain the token, initilize token
            # else increment the frequency
            if (token not in self.token_dict):
                self.token_dict[token] = 1
            else:
                self.token_dict[token] += 1
        

    def get_tokens_list(self):
        return self._token_list

    def get_tokens_size(self):
        return self._token_size 

    def get_freqMap(self):
        return self.token_dict

