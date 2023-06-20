import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
nltk.download('averaged_perceptron_tagger')

class Lemmatizer:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, word):
        return self.lem(word)

    def lem(self, word):
        pos = pos_tag(word_tokenize(word))[0][1]
        if pos[0] == 'J':
            return self.lemmatizer.lemmatize(word, 'a')
        elif pos[0] == 'N':
            return self.lemmatizer.lemmatize(word, 'n')
        elif pos[0] == 'V':
            return self.lemmatizer.lemmatize(word, 'v')
        elif pos[0] == 'R':
            return self.lemmatizer.lemmatize(word, 'r')
        else:
            return word