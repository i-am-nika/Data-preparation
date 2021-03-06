#!/bin/env python3

""" 
Pre-process Text Data. The program takes one command-line argument - a text file for pre-processing. 
If you run the program without a command-line argument, 
you'll be asked to type an url of the website you want to pre-process.
"""

#preprocess.py
#usage:
#$ ./preprocess.py
 #__author__ = "Tetyana Chernenko"
#__copyright__ = "Copyright (c) 2017, 2018 Tetyana Chernenko"
#__credits__ = ["Tetyana Chernenko"]
#__license__ = "GNU General Public License v3.0"
#__version__ = "1.0.0"
#__maintrainer__ = "Tetyana Chernenko"
#__email__ = "tatjana.chernenko@gmail.com"
#__status__ = "Development"

import sys
import nltk
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt 
import seaborn as sns 
from urllib import request
        
def getData(filename):
    with open(filename,"r") as f:
        data = f.readlines() # returns a list
    return data

def readUrl(url):    
    data = request.urlopen(url).read().decode('utf8')    
    return data

def clean_html(data):        
    soup = BeautifulSoup(str(data), "lxml")
    text = soup.get_text()
    return text

def tokenize_remove_punct(text):
    tokens = re.findall(r"\w+", str(text)) # remove punctuation 
    words = [] 
    for word in tokens:
        if word == "n": 
            words.append(" ")
        else:
            words.append(word.lower())
    return words

def tokenize_keep_punct(text):
    tokens = re.findall(r"\w+(?:[-']\w+)*|'|[-.(]+|\s\w*", str(text)) # don't remove punctuation
    words = [] 
    for word in tokens:
        if word == "n": 
            words.append(" ")
        else: 
            words.append(word.lower())
    return words

def remove_capit(words):
    words_l = []
    for word in words:
        words_l.append(word.lower())
    return words_l

def del_stopwords(words):
    without_stopwords = []
    stop_words = nltk.corpus.stopwords.words("english")
    print("English stopwords: ", stop_words)
    for word in words:
       if word not in stop_words:
           without_stopwords.append(word)
    print(without_stopwords)
    return without_stopwords

def own_stopwords(words, own_list):
    without_stopwords = []
    stop_words = own_list.split(", ")
    print("Own stopwords: ", stop_words)
    for word in words:
       if word not in stop_words:
           without_stopwords.append(word)
    return without_stopwords

def stem(without_stopwords):
    porter = nltk.PorterStemmer() 
    without_stopwords = [porter.stem(t) for t in without_stopwords]
    return without_stopwords

def lemm(without_stopwords):
    wnl = nltk.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in without_stopwords]
    return lemmas 


if __name__ == "__main__":
    arg_list = sys.argv

    if len(arg_list) > 1:
        textfile_for_preprocessing = arg_list[1]
        data = getData(textfile_for_preprocessing)
    else:
            url = str(input(" Please type your url: "))
            data = readUrl(url)

    choice = input("Do you want to clean data from html tags? (yes / no) Your choice: ")
    if choice == "yes":
        text = clean_html(data)
        print(text)
    else:
        text = data
        print(text)

    choice = input("Do you want to tokenize your data? (yes / no) Your choice: ")
    if choice == "yes":
        choice = input("Do you want to remove punctuation? (yes / no) Your choice: ")
        if choice == "yes":
            words = tokenize_remove_punct(text)
        else:
            words = tokenize_keep_punct(text)
    else:
        words = text

    choice = input("Do you want to remove capitalisation? (yes / no) Your choice: ")
    if choice == "yes":
        words_low = remove_capit(words)
    else:
        words_low = words

    choice = input("Do you want to delete stopwords? (yes / no) Your choice: ")
    if choice == "yes":
        without_stopwords = del_stopwords(words_low)
    else:
        without_stopwords = words_low

    choice = input("Do you want to delete your own stopwords? (yes / no) Your choice: ")
    if choice == "yes":
        own_list = input("Please type your own stopwords separated by commas (for example: am, i, if ) Your choice: ")
        without_stopwords = own_stopwords(without_stopwords, own_list)
    else:
        pass

    choice = input("Do you want to make stemming? (yes / no) Your choice: ")
    if choice == "yes":
        without_stopwords = stem(without_stopwords)
    else:
        pass

    choice = input("Do you want to make lemmatization? (yes / no) Your choice: ")
    if choice == "yes":
        lemmas = lemm(without_stopwords)
    else:
        lemmas = without_stopwords

    choice = input("Do you want to see Frequency Distribution of words? (yes / no) Your choice: ")
    if choice == "yes":
        lemmas_without_empty_lines = []
        for lemma in lemmas:
            if lemma.split():
                lemmas_without_empty_lines.append(lemma)
        sns.set() 
        freqdist1 = nltk.FreqDist(lemmas_without_empty_lines) 
        freqdist1.plot(25)

    choice = input("Do you want to write output to a file? (yes / no) Your choice: ")
    if choice == "yes":
        choice = input("Please type the filename with the path (for example: /myfiles/output.txt or output.txt (if you want to create an output file in the current directory). Your output file: ")
        try:
            output_file = open(choice, 'w')
            choice = input("Do you want to remove duplicates of words? (yes / no) Your choice: ")
            if choice == "yes":
                words = set(lemmas) # remove duplicates
            else:
                words = lemmas            
            print("Writing output to a file...")
            choice = input("Do you want to sort your tokens alphabetically (and remove empty lines between sentences)? (yes / no) Your choice: ")
            if choice == "yes":
                for word in sorted(words): 
                    if word.split():
                        print(word, file = output_file)
                print("Done.")
            else:
                for word in words: 
                    print(word, file = output_file)
                print("Done.")
        except:
            print("Incorrect filename or path.")
    
