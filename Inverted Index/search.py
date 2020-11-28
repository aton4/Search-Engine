import sys
import os
import pickle
from nltk.stem import PorterStemmer
import time
import json


def runSearchEngine():

    merged_ind = open("finalmergedind.txt", "r")
    idByteOffset = json.load(merged_ind)
    merged_txt = open("finalmerge.txt","r")
    portStem = PorterStemmer()
    urls = open("urls.txt","r")
    urls_map = json.load(urls)
    while(True):
        userInput = input("Input Search: ").strip()
        search_words = userInput.split(" ")
        list_search = []
        for word in search_words:
            wordStem = portStem.stem(word)
            offset = idByteOffset[wordStem]
            merged_txt.seek(offset)
            postingList = json.loads(merged_txt.readline()) 
            list_search.append(postingList)
            
        print(searchProcess(list_search, urls_map))

def searchProcess(inputPostingList, urls_map):
    wordPostings = inputPostingList
    foundIds = []

    if (len(wordPostings) == 1):
        for element in wordPostings[0]:
            foundIds.append(element[0])
        
        urls = foundIds[:5]
        url_links = ""
        for i in range(0,len(urls)):
            line = urls_map[str(urls[i])]
            url_links += line + "\n"
        return url_links

    wordPostings = sorted(wordPostings, key = lambda x : len(x))
    
    answers = []
    index1 = 0
    index2 = 0
    while ( (index1 < len(wordPostings[0])) and (index2 < len(wordPostings[1])) ):

        if (wordPostings[0][index1][0] == wordPostings[1][index2][0]):
            answers.append(wordPostings[0][index1][0])
            index1 = index1 + 1
            index2 = index2 + 1
        else:
            if (wordPostings[0][index1][0] < wordPostings[1][index2][0]):
                index1 = index1 + 1
            else:
                index2 = index2 + 1
    if(len(inputPostingList)==2):
        urls = answers[:5]
        url_links = ""
        for i in range(0,len(urls)):
            line = urls_map[str(urls[i])]
            url_links += line + "\n"
        return url_links
        
    for postings in range(2,len(wordPostings)):    
        list_process = wordPostings[postings]
        new_list = []
        ind1 = 0
        ind2 = 0
        while((ind1 < len(answers)) and (ind2 < len(list_process) )):
            if(answers[ind1] == list_process[ind2][0]):
                new_list.append(answers[ind1])
                ind1 = ind1 + 1
                ind2 = ind2 + 1
            else:
                if(answers[ind1] < list_process[ind2][0]):
                    ind1 = ind1 + 1
                else:
                    ind2 = ind2 + 1
        if(len(new_list)==0):
            return
        else:
            answers = new_list

    urls = []        
    if(len(answers)>=5):
        urls = answers[:5]
    else:
        urls = answers
    url_links = ""

    for i in range(0,len(urls)):
        # print(urls[i])
        line = urls_map[str(urls[i])]
        url_links += line + "\n"

    return url_links

if __name__ == '__main__':

    runSearchEngine()
