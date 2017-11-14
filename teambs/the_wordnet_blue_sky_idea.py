
# coding: utf-8

# # Jeff's wordnet idea
# A wordnet is a data structure similar to a thesarus
# A wordnet is a collection of synsets.  Each synset is a collection of words with a similar meaning.
# 
# The structure of this page roughly follows the wordnet page in the NLTK documentation, http://www.nltk.org/howto/wordnet.html
# 
# 
# 

# In[ ]:


import sys
print ( sys.version, file=sys.stderr )


from nltk.corpus import wordnet as wn

import pandas as pd
import preprocessing
from typing import TypeVar
import nltk

def make_synset_from_word_list(component_words) -> nltk.corpus.reader.wordnet.Synset :
    """
    This subroutine returns a synset which is the union of the all of the synsets of
    all of the words in the component (which is either a 'body' or a 'title'.
    
    param: component_words    A list of words in the title or the body of this joke
    """
    
    component_synset = set({})
    for word in component_words:
        word_synset = wn.synset(word)
        assert isinstance(word_synset[0], nltk.corpus.reader.wordnet.Synset)
        component_synset |= word_synset
    return component_synset
        


# In[5]:


print("Reading the jokes JSON file", file=sys.stderr)
jokeData = pd.read_json("reddit_jokes.json")
print("Preprocessing", file=sys.stderr)
prep = preprocessing.preprocess()
print("Storing the jokeData dictionary", file=sys.stderr)
jokeData['body']: pd.core.series.Series = prep.cleanData(jokeData['body'])
jokeData['title']: pd.core.series.Series = prep.cleanData(jokeData['title'])
print("The type of the values of dictionary 'title' is ", type(jokeData['title']))
print("The type of the values of dictionary 'body' is ", type(jokeData['body']))

print("Tokenizing the words", file=sys.stderr)
# title_word_list is a list of all of the tokenized words in each title.  If there are 194394 jokes in the JSON
# file, then this list will be of length 194394
title_word_list = prep.tokenizeText(jokeData['title'])
body_word_list = prep.tokenizeText(jokeData['body'])


# print(type(words))
# 

# In[8]:


print(type(words))
print(len(words))
print(words[1])


# In[ ]:


for title_words, body_words in zip(title_word_list, body_word_list :
    body_synset = make_synset_from_word_list(body_words)
    title_synset = make_synset_from_word_list(title_words)
    similarity_list = list()
    for title_syn_elem in title_synset:
        for body_syn_elem in body_synset:
            distance = wn.path_similarity(title_syn_elem, body_syn_elem)
            similarity_list.append( ( distance, title_syn_elem, body_syn_elem))
    similarity_list.sort()

    


# In[13]:


from nltk.corpus import wordnet as wn
syns =wn.synsets('dog') 
assert isinstance(syns, wn.Synset),"Type of syns is %s" % type(syns)
print(type(syns[0]))
s:set =set()
print("There are %d items in set s (should be 0)" % len(s))
s.add("Q", "R")
print("Set s contains %s, should be Q, R " % str(s) )
s ^= {"W", "T", "R"}
print("Set s contains %s, should be Q, R, T, W" % str(s) )
s |= {"W", "p"}
print("Set s contains %s, should be Q R, T, W, p "% str(s) )

