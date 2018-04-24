
# coding: utf-8

# In[45]:


import os
import json

metadata_directory = "metadata"
file_directory = "json_samples"
choices = ['1','2','3']


# In[46]:


def document_test(data):
    text = data["text"]
    sents = [(e+'.').strip() for e in text.replace('\n','').split('.')][:-1]   
    
    scores = []
    n_sents = len(sents)
    choices_string = "(" + "/".join(choices) + ")"
    
    for j, sent in enumerate(sents):
        sent_label = "Sentence {arg1} of {arg2}:".format(arg1=j+1, arg2=n_sents)
        x = input("\n" + sent_label + "\n" + sent + "\n\nScore? " + choices_string + " ")
        while x not in choices:
            x = input("Score? " + choices_string + " ")
        scores.append((sent,int(x)))
    
    return scores


# In[47]:


def thru_documents(i, scores_dict):
    print("\nPlease read and score each sentence. The possible scores are:\n\t1: sad\n\t2: neutral\n\t3: happy")

    while True:

        filename = str(i) + ".txt"
        filepath = os.path.join(file_directory, filename)

        try:
            with open(filepath, 'r') as file:
                x = input("\nProceed to Document{arg}? (y/n) ".format(arg=i))
                while (x != "y"):
                    if (x == "n"):
                        print("Please enjoy your break.")
                        return (i, scores_dict) 
                    else:
                        x = input("Input (y/n) ")
                data = json.load(file)
                scores_dict[filename] = document_test(data)
                i += 1
        except Exception:
            i = 0
            break

    
    return (i, scores_dict)


# In[48]:


def main():
    
    # beginning the trials
    if not os.path.exists(metadata_directory):
        os.mkdir(metadata_directory)
        print("Welcome to the questionnaire.")
        i, now_dict = thru_documents(1, {})
    # resume trials
    else:
        with open(os.path.join(metadata_directory, "m.txt"), 'r') as file:
            obj = json.load(file)
            now_dict = obj['dict']
            i = obj['i']
            if i == 0:
                print("You have already completed the documents.")
            else:
                print("Welcome back.")
                i, now_dict = thru_documents(i, now_dict)
    
    # create json object for metadata
    obj = {}
    obj['i'] = i
    obj['dict'] = now_dict
        
    with open(os.path.join(metadata_directory, "m.txt"), 'w') as outfile:
        json.dump(obj, outfile, indent=4)
        
    if i == 0:
        print("You have completed all of the documents. Thank you!")


# In[53]:


if __name__ == "__main__":
    main()

