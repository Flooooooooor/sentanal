
# coding: utf-8

# In[80]:


# Adapted from code by Shravan I.V. 
# https://opensourceforu.com/2016/12/analysing-sentiments-nltk/
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from random import shuffle
import math
import numpy as np

# Step 0 - All data
allData = [
    ("Great place to be when you are in Bangalore.", "pos"),
    ("The place was being renovated when I visited so the seating was limited.", "neg"),
    ("Loved the ambience, loved the food", "pos"),
    ("The food is delicious but not over the top.", "neg"),
    ("Service - Little slow, probably because too many people.", "neg"),
    ("The place is not easy to locate", "neg"),
    ("If I could give this place zero stars I would!", "neg"),
    ("I had the carne asada burrito and it was amazing", "pos"),
    ("I had a really bad experience here about a year ago", "neg"),
    ("Trust me, you have to be pretty damn good to get this high honor", "pos"),
    ("Hopefully in the near future, the owner will open up another store to alleviate the congestion of his current spot", "neg"),
    ("Super crowded and not a whole lot of seating", "neg"),
    ("This place holds a special place in my heart.", "pos"),
    (" Unfortunately, they still put sour cream in my husband's burrito when I specifically requested his burrito without it.", "neg"),
    ("The menu seems pretty simple.", "neg"),
    ("The flavors were great.", "pos"),
    (" La Taqueria is a true orginal of the Misison and has been around for decades.", "pos"),
    ("Nothing flashy, just plain old delicious carne asada, tortilla, cilantro, onions and salsa.", "pos"),
    ("What a disappointment.", "neg"),
    ("Unfortunately, everything about the experience was mediocre, starting with the food and moving to the customer service.", "neg"),
    ("Half a burrito was the perfect amount, and you get the benefit of still being able to eat delicious food!", "pos"),
    ("This was the first place I wanted to try on my trip to San Fran, and it was well worth it.", "pos")
]
    
trainSize = math.floor(len(allData) * 0.9) 

shuffle(allData)

# Step 1 – Training data
train = allData[:trainSize]
test = allData[trainSize:]

#print("TRAIN" + str(train))
#print("\n\n\nTEST" + str(test))


# In[81]:


# Step 2
dictionary = set(word.lower() for passage in train for word in word_tokenize(passage[0]))

#print(dictionary)


# In[82]:


# Step 3
t = [({word: (word in word_tokenize(x[0])) for word in dictionary}, x[1]) for x in train]

#print(t)


# In[83]:


# Step 4 – the classifier is trained with sample data
classifier = nltk.NaiveBayesClassifier.train(t)


# In[84]:


def getConfusion(dataset):

    confusion = np.matrix([[0,0],[0,0]])

    for case in dataset:
        sentence, answer = case[0], case[1]
        test_data_features = {word.lower(): (word in word_tokenize(sentence.lower())) for word in dictionary}
        guess = (classifier.classify(test_data_features))

        if (answer == "pos"):
            if (guess == "pos"):
                confusion[1,1] += 1
            else:
                confusion[1,0] += 1
        else:
            if (guess == "pos"):
                confusion[0,1] += 1
            else:
                confusion[0,0] += 1
                
    return confusion


# In[85]:


def printResults(name, confusion):
    
    total = np.sum(confusion)
    correct = confusion[0,0] + confusion[1,1]
    
    accuracy = correct / total
    
    print("----------------")
    print(name)
    print(confusion)
    print("accuracy: " + "{:.0%}".format(accuracy))


# In[86]:


train_confusion = getConfusion(train)
test_confusion = getConfusion(test)

printResults("Training:", train_confusion)
printResults("Testing:", test_confusion)

