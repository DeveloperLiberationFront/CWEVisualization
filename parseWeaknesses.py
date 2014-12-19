from __future__ import division, print_function

__author__ = 'Brooke'
import string
import tfidf
import nltk
import numpy as np

from nltk import *
from collections import Counter
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('cwec_v2.8.xml'), 'xml')

from nltk.stem import WordNetLemmatizer
st = WordNetLemmatizer()
stemmer = SnowballStemmer("english")
print('*'*50)
i = 0
z = 0
stopwords = nltk.corpus.stopwords.words('english')

g = open('Data2/words.txt', 'w+')
g.close()

for x in soup.Weakness_Catalog.Weaknesses.find_all('Weakness'):
    table = tfidf.tfidf()
    name = x.attrs['Name']
    #Get description summary and format text.
    s = x.Description.Description_Summary.get_text()
    s = s.lower()
    s = "".join(c for c in s if c not in string.punctuation)
    a = s.split()
    a = [w for w in a if w.lower() not in stopwords]
    a = [stemmer.stem(w) for w in a]
    c = Counter(a)
    #See if there is an extended description before grabbing it.
    if hasattr(x.Description, 'Extended_Description'):
        if x.Description.Extended_Description is None:
            z += 1
            p = ""
        else:
            p = x.Description.Extended_Description.get_text()
    else:
        p = ""
    #Format extended description, if any.
    p = p.lower()
    p = "".join(c for c in p if c not in string.punctuation)
    b = p.split()
    b = [w for w in b if w.lower() not in stopwords]
    b = [stemmer.stem(w) for w in b]
    d = Counter(b)
    #Add documents into table.
    table.addDocument("Description", a)
    table.addDocument("Extended Description", b)
    #Format weakness name for file name.
    n = "".join(c for c in name if c not in string.punctuation)
    n = string.capwords(n)
    n = n.replace(' ', '')
    f = open('Data/' + str(i) + "_" + n + '.txt', 'w')
    f.write(name + "\n")
    #Write TF-IDF data to file, if a word (k) appears in both description and extended description
    #then add to the file.
    for k, v in sorted(c.items(), key=lambda y: y[1], reverse=True):
        if table.similarities([k])[0][1] > 0 and table.similarities([k])[1][1] > 0:
            f.write(k + ", " + str(table.similarities([k])[0][1]) + ", " + str(table.similarities([k])[1][1]) + "\n")
            #if word (k) is not already included in the file of key terms, then add it.
            if open('Data/words.txt').read().find(k) == -1:
                open('Data/words.txt', 'a').write(k + "\n")
    ##f.write("\n")
    ##for k, v in sorted(d.items(), key=lambda y: y[1], reverse=True):
        ##f.write(k + ", " + str(table.similarities([k])[0][1]) + ", " + str(table.similarities([k])[1][1]) + "\n")
    f.close()
    i += 1
    #if i > 10: #for only running on certain numbers of weaknesses. Mainly test purposes.
    #    break

print("How many don't have extended description: " + str(z))
print("How many weaknesses in document: " + str(i))
