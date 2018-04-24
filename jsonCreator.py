
# coding: utf-8

# In[12]:


import os
import json
import random
import requests
from bs4 import BeautifulSoup

directory = "json_samples"

wikis = ['https://en.wikipedia.org/wiki/History_of_childhood', 
         'https://en.wikipedia.org/wiki/History_of_Japan',
         'https://en.wikipedia.org/wiki/History_of_Spain',
         'https://en.wikipedia.org/wiki/History_of_Africa',
         'https://en.wikipedia.org/wiki/Philosophy'
        ]


# In[13]:


def get_sentences(wiki):

    page = requests.get(wiki)
    soup = BeautifulSoup(page.text, 'html.parser')

    # remove parts of the html aren't body text sentences
    body = soup.find(class_='mw-parser-output')
    for h2 in soup('h2'):
        h2.decompose()
    for h3 in soup('h3'):
        h3.decompose()
    for sup in soup('sup'):
        sup.decompose()
    for table in soup('table'):
        table.decompose()
    for li in soup('li'):
        li.decompose()
    for blockquote in soup('blockquote'):
        blockquote.decompose()
    for toc in soup(class_='toc'):
        toc.decompose()
    for hatnote in soup(class_='hatnote navigation-not-searchable'):
        hatnote.decompose()
    for navbox in soup(class_='navbox'):
        navbox.decompose()

    text = body.get_text()

    # create a list of sentences
    sentences = [(e+'.').strip() for e in text.replace('\n','').split('.')]
    
    return sentences


# In[14]:


all_sents = []
for wiki in wikis:
    all_sents += get_sentences(wiki)


# In[15]:


def rand_join(sents):
    string = sents[0]
    
    for sent in sents[1:]:
        symbol = ' '
        r = random.uniform(0,10)
        if r>8:
            symbol = '\n\n'
            
        string += (symbol+sent)
        
    return string


# In[16]:


docs = []

while len(all_sents) > 20:
    n = random.randint(18,20)
    sents = all_sents[:n]
    all_sents = all_sents[n:]
    
    doc = rand_join(sents)
    docs.append(doc)   


# In[17]:


for i, doc in enumerate(docs):
    obj = {}
    obj['note_id'] = str(i)
    obj['text'] = doc
        
    filename = os.path.join(directory, str(i+1) + ".txt")
    with open(filename, 'w') as outfile:
        json.dump(obj, outfile, indent=4)

