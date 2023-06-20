import pickle

with open("utils\\inverted_index.pkl", "rb") as file:
    inverted_index = pickle.load(file)

doc = set()

for term in inverted_index:
    for docID in inverted_index[term]:
        doc.add(docID)

print(len(doc))
print(len(inverted_index["informatics"]))