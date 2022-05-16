# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:20:27 2021

@author: yuwen
"""



# importing the two .txt file's content
with open('input1.txt', 'r') as f1, open('input2.txt', 'r') as f2:
    content1 = f1.read()
    content2 = f2.read()
import nltk
import csv
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet, stopwords
from nltk.probability import FreqDist
from nltk.util import bigrams, trigrams

tokenizer = RegexpTokenizer(r'\w+') # use NOT alphanumeric as token separator
defaultStopwords = stopwords.words('english')

# -------------------------HELPER FUNCTIONS--------------------
def convertToWNTag(inputTag):
	# Wordnet only has 4 tags {verb,adjective,adverb,noun}, where the defualt is N for noun
	if inputTag[0] == 'N':
		returnTag = 1
	if inputTag[0] == 'V':
		returnTag = 2
	if inputTag[0] == 'J':
		returnTag = 3
	if inputTag[0] == 'R':
		returnTag = 4
	if inputTag[0] not in ( 'V', 'J', 'R', 'N'):
		returnTag = 1
	return (returnTag)

def convertToWNTag2(inputTag):
	# Wordnet only has 4 tags {verb,adjective,adverb,noun}, where the defualt is N for noun
	if inputTag[0] == 'N':
		returnTag = wordnet.NOUN
	if inputTag[0] == 'V':
		returnTag = wordnet.VERB
	if inputTag[0] == 'J':
		returnTag = wordnet.ADJ
	if inputTag[0] == 'R':
		returnTag = wordnet.ADV
	if inputTag[0] not in ( 'V', 'J', 'R', 'N'):
		returnTag = wordnet.NOUN
	return ( returnTag )

def bigramFreq(wordlist):
    listOfBigrams = list(bigrams(wordlist))
    bigramFreq = FreqDist()
    for pair in listOfBigrams:
        bigramFreq[pair]+=1
    return bigramFreq

def trigramFreq(wordlist):
    listOfTrigrams = list(trigrams(wordlist))
    trigramFreq = FreqDist()
    for t in listOfTrigrams:
        trigramFreq[t]+=1
    return trigramFreq

def wordFreq(wordlist):
    fdist = FreqDist()
    for w in wordlist:
        fdist[w] += 1
    return fdist

# Bigrams include a specific wordType (noun, verb, etc.)
def bigramTagFreq(wordlist, wordType):
    listOfBigrams = list(bigrams(wordlist))
    biTagFreq = FreqDist()
    for pair in listOfBigrams:
        tag = nltk.pos_tag(pair)
        if (convertToWNTag(tag[0][1]) == wordType) or (convertToWNTag(tag[1][1]) == wordType):
            biTagFreq[pair] +=1
    return biTagFreq

# Trigrams include a specific wordType (noun, verb, etc.)
def trigramTagFreq(wordlist, wordType):
    listOfTrigrams = list(trigrams(wordlist))
    triTagFreq = FreqDist()
    for t in listOfTrigrams:
        tag = nltk.pos_tag(t)
        if (convertToWNTag(tag[0][1]) == wordType) or (convertToWNTag(tag[1][1]) == wordType) or (convertToWNTag(tag[2][1]) == wordType):
            triTagFreq[t] +=1
    return triTagFreq
# -------------------------HELPER FUNCTIONS END----------------------

# using the tokenizer to remove the punctuationas
noPunct1 = tokenizer.tokenize(content1)
noPunct2 = tokenizer.tokenize(content2)

# Lemmatizing words
WNlemma = nltk.WordNetLemmatizer()
lemma_list1 = [WNlemma.lemmatize(w) for w in noPunct1]
lemma_list2 = [WNlemma.lemmatize(w) for w in noPunct2]

# Frequent words before lemma
fdist1 = wordFreq(noPunct1)
fdist2 = wordFreq(noPunct2)
# Frequent words after lemma
lfdist1 = wordFreq(lemma_list1)
lfdist2 = wordFreq(lemma_list2)
# =============================================================================
# print('Before Lemma: ')
# print(fdist1.most_common(30))
# print(fdist2.most_common(30))
# print()
# print('After Lemma: ')
# print(lfdist1.most_common(30))
# print(lfdist2.most_common(30))
# =============================================================================

# POS Taggings & convert to WNTag
# =============================================================================
# taggedTokens1 = nltk.pos_tag(lemma_list1)
# taggedTokens2 = nltk.pos_tag(lemma_list2)
# 
# # Create adj, verb, adv, and noun word lists
# # Remove stop words
# # Find most common adj, verb, adv, and nouns
# noun1 = FreqDist()
# noun2 = FreqDist()
# verb1 = FreqDist()
# verb2 = FreqDist()
# adj1 = FreqDist()
# adj2 = FreqDist()
# adv1 = FreqDist()
# adv2 = FreqDist()
# for w in taggedTokens1:
#     if w[0] not in defaultStopwords:
#         tg = convertToWNTag(w[1])
#         if tg == 1:
#             noun1[w[0]] += 1
#         if tg == 2:
#             verb1[w[0]] +=1
#         if tg == 3:
#             adj1[w[0]] +=1
#         if tg == 4:
#             adv1[w[0]] +=1
# for w in taggedTokens2:
#     if w[0] not in defaultStopwords:
#         tg = convertToWNTag(w[1])
#         if tg == 1:
#             noun2[w[0]] += 1
#         if tg == 2:
#             verb2[w[0]] +=1
#         if tg == 3:
#             adj2[w[0]] +=1
#         if tg == 4:
#             adv2[w[0]] +=1       
#
# print('\n',noun1.most_common(60))
# print('\n',noun2.most_common(60))        
# =============================================================================

# Bigrams & Trigrams (using lemmatized wordlist)
# bigramFreq1 = bigramFreq(lemma_list1)
# bigramFreq2 = bigramFreq(lemma_list2)
trigramFreq1 = trigramFreq(lemma_list1)
trigramFreq2 = trigramFreq(lemma_list2)
# print("\nbigramFreq1: 100 most common:")
# print(bigramFreq1.most_common(100))
# print("\nbigramFreq2: 100 most common:")
# print(bigramFreq2.most_common(100))

with open ('./Frequent_trigram1.csv', 'w', newline = '') as wFile1, open ('./Frequent_trigram2.csv', 'w', newline = '') as wFile2:
    headList = ['trigram', 'freq']
    writer1 = csv.DictWriter(wFile1, fieldnames = headList)
    writer2 = csv.DictWriter(wFile2, fieldnames = headList)
    writer1.writeheader()
    writer2.writeheader()
    for w in trigramFreq1.keys():
        writer1.writerow({headList[0]:w, headList[1]:trigramFreq1[w]})
    for w in trigramFreq2.keys():
        writer2.writerow({headList[0]:w, headList[1]:trigramFreq2[w]})
        
# Frequent Bigrams include some specific word type
# =============================================================================
# nounBigramFreq1 = bigramTagFreq(lemma_list1, 1)
# nounBigramFreq2 = bigramTagFreq(lemma_list2, 1)
# =============================================================================
# =============================================================================
# verbBigramFreq1 = bigramTagFreq(lemma_list1, 2)
# verbBigramFreq2 = bigramTagFreq(lemma_list2, 2)
# =============================================================================
# =============================================================================
# print('Most Common 50 bigram including nouns: ')
# print(nounBigramFreq1.most_common(50))
# print()
# print(nounBigramFreq2.most_common(50))
# =============================================================================
# =============================================================================
# print('Most Common 50 bigram including verbs: ')
# print(verbBigramFreq1.most_common(50))
# print()
# print(verbBigramFreq2.most_common(50))
# =============================================================================

# =============================================================================
# test = bigramTagFreq(['i','like','dog','i','like','cat','but','i','dislike','snake'], 1)
# print(test.most_common(5))
# =============================================================================







