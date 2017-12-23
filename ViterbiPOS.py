
trainingFile = "berp-POS-training.txt"
developmentFile = "assgn2-test-set.txt"

import copy
import collections
import numpy



class sentences(object):        #used for sentence computation in viterbi algo
    def __init__(self):
        self.list = []

        self.sentencesMax = 0       #max value for viterbi algo

    def addWord(self, gram):
        for sentence in self.list:
            sentence.bigrams.append(gram)                   #appending the best gram

    def addSentence(self):
        sent = sentence()
        self.list.append(sent)

    def replicate(self, gram):

        holdList = []
        for s in self.list:
            c = sentence()
            c = copy.deepcopy(s)

            c.bigrams.pop()
            c.bigrams.append(gram)

            holdList.append(c)

        self.list = self.list[:] + holdList[:]


class sentence(object):
    def __init__(self):             #initialize the bigrams and score of sentence and as per the
        self.bigrams = []           #score get the best possible pos for each word in the training set
        self.score = 0
        self.max = 0

    def sentScore(self):
        switch = 0
        for gram in self.bigrams:
            if switch == 0:
                self.score = gram.finalProb                     #multiply with start value of pie as 1
                switch = 1
            else:
                self.score = self.score * float(gram.finalProb)         #multiply by previous value
                                                                        #as dynamic programming principle



class bigramsh(object):  #define the bigram object type with respect to its probability for future calculations
    def __init__(self):         # define the variables for storing the elements of a biagram and unigrams
        self.priorWord = ''
        self.priorTag = ''
        self.currentWord = ''
        self.currentTag = ''

        self.transition = ()
        self.emission = ()

        self.wordCount = 0
        self.tagCount = 0
        self.priorTagCount = 0
        self.transCount = 0
        self.emitCount = 0

        self.possTags = []

        self.transProb = 0
        self.emishProb = 0
        self.finalProb = 0

    def scoreCalculate(self):   #calculate the counts to be used in transition matrix
        self.transProb = self.transCount / float(self.priorTagCount)
        self.emishProb = self.emitCount / float(self.tagCount)
        self.finalProb = self.transProb * self.emishProb            #step 2 of viterbi algo



file = open(trainingFile, "r")

theBigrams = []             #list for bigrams


wordDictionary = collections.defaultdict(int)          #dictionaries for storing the transactions
tagDictionary = collections.defaultdict(int)
transDictionary = collections.defaultdict(int)
emitDictionary = collections.defaultdict(int)
possDictionary1 = collections.defaultdict(list)
possDictionary2 = collections.defaultdict(int)


lastDic = collections.defaultdict(str)


lastWord = ''
lastTag = ''
lastTagCount = 0


file.seek(0)
for line in file:

    unigram = bigramsh()
    thisLine = line.split()
    listLen = len(thisLine)                     # individually accessing each word of individual training set


    unigram.priorWord = lastWord
    unigram.priorTag = lastTag
    unigram.priorTagCount = lastTagCount

    if listLen > 1:                             # checking whether there is a word or not

        unigram.currentWord = thisLine[1]          #taking the word column
        unigram.currentTag = thisLine[2]           #taking the tag column

        possDictionary1[unigram.currentWord].append(unigram.currentTag)          #matching words with given tags

    else:
        unigram.currentWord = ''
        unigram.currentTag = ''

    unigram.transition = (unigram.priorTag, unigram.currentTag)          #matching transition and emission prob
    unigram.emission = (unigram.currentTag, unigram.currentWord)

    transDictionary[unigram.transition] += 1              #calculating various numbers
    emitDictionary[unigram.emission] += 1
    wordDictionary[unigram.currentWord] += 1
    tagDictionary[unigram.currentTag] += 1
    possDictionary2[unigram.currentWord] += 1

    theBigrams.append(unigram)             #append the previous word and the current word

    lastWord = unigram.currentWord
    lastTag = unigram.currentTag
    lastTagCount = unigram.tagCount

for thingy in possDictionary1:
    possDictionary1[thingy] = list(set(possDictionary1[thingy]))     #matches word with set of all possible tags

copyTagDic = copy.deepcopy(tagDictionary)
copyTransDic = copy.deepcopy(transDictionary)

for tag in copyTagDic:
    lastDic[tag] = ""           #lastDic matches the unknown word in sequence

for trans in transDictionary:
    copyTagDic[trans[0]] += 1           #for calculating tag prob

for trans in transDictionary:
    copyTransDic[trans] = transDictionary[trans] / float(copyTagDic[trans[0]])

for tag in copyTagDic:
    copyTagDic[tag] = 0

for item in copyTransDic:
    if copyTagDic[item[0]] < copyTransDic[item]:
        copyTagDic[item[0]] = copyTransDic[item]

for item in copyTransDic:
    if copyTagDic[item[0]] == copyTransDic[item]:
        lastDic[item[0]] = item[1]

gramDic = collections.defaultdict(bigramsh)

for item in theBigrams:

    item.wordCount = wordDictionary[item.currentWord]
    item.tagCount = tagDictionary[item.currentTag]
    item.priorTagCount = tagDictionary[item.priorTag]
    item.transCount = transDictionary[item.transition]

    if item.emission[0] == item.currentTag and item.emission[1] == item.currentWord:
        item.emitCount = emitDictionary[item.emission]

    item.possTags = possDictionary1[item.currentWord]

    item.scoreCalculate()            #OUTPUTS THE VALUES TO BE USED IN CALCULATION OF VITERBI ALGO
    gramDic[(item.currentWord, item.currentTag)] = item

file = open(developmentFile, 'r')

sentencesList = []
newSentences = 1
sentencesListNum = 0
theLastTag = ''
for word in file:

    wordList = word.split()
    currentTag = ''

    if len(wordList) > 0:
        theWord = wordList[1]
        tags = possDictionary1[theWord]

        if newSentences == 1:
            newSentences = 0
            sentssh = sentences()
            sentssh.addSentence()

        if len(tags) >= 1:

            Maxtag = 0
            for tag in tags:
                unigram = gramDic[(theWord, tag)]
                currentTag = tag

                if unigram.finalProb >= Maxtag:   #basically in viterbi we take the max of any column(with smoothing)
                                                #(we get non zero values also)
                                                #at any stage and we use backpointer to represent that state
                    Maxtag = unigram.finalProb

            for tag in tags:
                unigram = gramDic[(theWord, tag)]

                if unigram.finalProb == Maxtag:                #if word and tag has the highest value
                    sentssh.addWord(unigram)                     #add that sentence to backpointer sents

        else:
            if len(tags) == 0:
                unigram = bigramsh()
                unigram.currentWord = theWord
                unigram.currentTag = lastDic[theLastTag]
                #gram.finalProb = 1/len(list)
                unigram.finalProb = .0001      #taking this probability for unseen values for smoothing
                                            #as 1/15001 approximately equals to 0 as it
                                            #original value is difficult to be stored in matrix
                gramDic[(unigram.currentWord, unigram.currentTag)] = unigram

            else:
                unigram = gramDic[(theWord, tags[0])]
                currentTag = tags[0]

            sentssh.addWord(unigram)

    else:
        newSentences = 1
        sentencesList.append(sentssh)
        sentencesListNum = sentencesListNum + 1

    theLastTag = currentTag

for sentssh in sentencesList:
    for sent in sentssh.list:
        sent.sentScore()
        if sent.score > sentssh.sentsMax:
            sentssh.sentsMax = sent.score

outputfile = open("out.txt", "w")          #writing the result in output file


for sentssh in sentencesList:
    num = 0
    counter=0
    for sent in sentssh.list:
        if sent.score == sentssh.sentsMax and num == 0:
            for unigram in sent.bigrams:
                counter=counter+1
                if(str(unigram.currentWord!= '')):
                    outputfile.write(str(counter) + "\t" + str(unigram.currentWord) + "\t" + str(unigram.currentTag) + "\n")
                else:
                    outputfile.write(str(unigram.currentWord) + "\t" + str(unigram.currentTag) + "\n")
                    counter=0
            num += 1
            outputfile.write("\n")

outputfile.write("\n")