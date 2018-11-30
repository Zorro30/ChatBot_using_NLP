# coding: utf-8

# # Meet Robo: your friend

import nltk
import numpy as np
import random
import string # to process standard python strings
import pyttsx3
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f=open('chatbot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()# converts to lowercase
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

sent_tokens[:2]

word_tokens[:5]

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


# Checking for greetings
def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



# Generating response
def response(user_response):
    robo_response=''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

r = sr.Recognizer()
engine = pyttsx3.init()
flag=True
my_text = "My name is BroBot. Please give me some command, or just say exit to leave!"
engine.say(my_text)
engine.runAndWait()

enine = pyttsx3.init()
my_text = 'Ask or give a Command!'
print('Ask or give a Command!')
engine.say(my_text)
engine.runAndWait()


while(flag==True):
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            user_response = r.recognize_google(audio)
            print("You said: {}".format(user_response))
        # user_response = input()
        # user_response=user_response.lower()
            if user_response!='exit':
                if user_response=='thanks' or user_response=='thank you':
                    flag=False
                    engine = pyttsx3.init()
                    my_text = 'You are welcome..'
                    print("ROBO: You are welcome..")
                    engine.say(my_text)
                    engine.runAndWait()

                else:
                    if greeting(user_response)!=None:
                        engine = pyttsx3.init()
                        my_text = '{}'.format(greeting(user_response))
                        print("ROBO: "+greeting(user_response))
                        engine.say(my_text)
                        engine.runAndWait()
                    else:
                        sent_tokens.append(user_response)
                        word_tokens=word_tokens+nltk.word_tokenize(user_response)
                        final_words=list(set(word_tokens))
                        print("ROBO: ",end="")
                        engine = pyttsx3.init()
                        my_text = '{}'.format(response(user_response))
                        print(response(user_response))
                        engine.say(my_text)
                        engine.runAndWait()
                        sent_tokens.remove(user_response)
            else:
                flag=False
                engine = pyttsx3.init()
                my_text = 'Bye! take care..'
                print("ROBO: Bye! take care..")
                engine.say(my_text)
                engine.runAndWait()

        except:
            engine = pyttsx3.init()
            my_text = 'sorry could not here you. Please try again!'
            print('sorry could not here you. Please try again!')
            engine.say(my_text)
            engine.runAndWait()
            