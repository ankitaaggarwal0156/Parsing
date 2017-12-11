#!/usr/bin/env python
from tree import Tree
from bigfloat import log10, bigfloat
from nltk.tokenize import word_tokenize
from dicts import DefaultDict
from random import choice
import time
import re
import matplotlib.pyplot as plt
from bigfloat import log, bigfloat
import sys, fileinput

sentences = [line for line in fileinput.input()]

grammar ={}
def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

def FileRead():
    with open('./train.trees.pre.unk','r') as f:
        for line in f:
            tr1 = Tree.from_str(line)
            q = tr1.bottomup()
            for l in q:
                if l.children == []:
                    continue
                grammar.setdefault(l.label, {})
                children = map(lambda x:str(x), l.children)
                grammar[l.label].setdefault(tuple(children),0 )
                grammar[l.label] [tuple(children)]+=1
    
    #Smoothing by adding additional rules
    i='<unk>'
    for k,v in grammar.iteritems():
        if i not in str(v):
            grammar[k][('<unk>',)]=1
            
    count =0
    for k,v in grammar.iteritems():
        count+=len(v)
    
    print "QUESTION 1 - \n Number of rules in grammar = ", count
    
    answer=[ [None,[None]],0]
    for k,v in grammar.iteritems():
        
        denominator=0
        for k1, v1 in v.iteritems():
            denominator+=v1
            
            if v1 > answer[1]:
                answer[1] = v1
                answer[0][0] = k
                answer[0][1] = k1
        
    
    print "Most Frequent Rule: \n ",str(answer[0][0]),"->"+ str(answer[0][1]),"Count =", str(answer[1])
    
    for k,v in grammar.iteritems():
        s1=0
        for k1,v1 in v.iteritems():
            s1 = s1 + v1 
        for k1,v1 in v.iteritems():
            p = float(v1)/float(s1)
            v[k1]= log10(bigfloat(p))
            #v[k1] = p
    
def ReadStringFile():
    global sentences
    count =0
    time1 =[]
    len_strings=[]
    fileW = open('./strings.out', 'w')
    
    for line in sentences:
        l = len(line)
        len_strings.append(l) 
        count = count +1
        tokens = word_tokenize(line)
        t1 = time.time()
        tree = str(parse(tokens))
        tree = tree.replace('[', '(')
        tree = tree.replace(']',')')
        tree = tree.replace(',','')
        tree = tree.replace('"','')
        tree = tree.replace('\'','')
        #if count==1:
        #    print "QUESTION 2 - \n", tree
        fileW.write(str(tree))
        fileW.write("\n")
        t2 = time.time()
        time1.append(t2-t1) 
    fileW.close()
    
#    print "QUESTION 3 - length of string vs parsing time plot"
    fig = plt.figure()
    ax = plt.gca()
    len_strings_3 = [pow(x,2) for x in len_strings]
    ax.scatter(len_strings_3, time1  , c='red')
    plt.xlabel('Length of strings power 2')
    plt.ylabel(' Time to parse')
    plt.title("Length vs Time on log-log scale")
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlim([10**0,10**5])
    plt.ylim([10**-3,10**1])
    plt.show()
#     

def producers(i):
    added = False
    results = []
    for k,v in grammar.iteritems():
        if type(i)==str:
            if i in str(v):
                for k1, v1 in v.iteritems():
                    if i in k1:
                        added = True
                        if len(k1)==1:
                            results.append(k)
        else:
            for k1, v1 in v.iteritems():
                added = True
                if i == k1:
                    results.append(k)
    
    if(added==False):
        i='<unk>'
        for k,v in grammar.iteritems():
            if i in str(v):
                for k1, v1 in v.iteritems():
                    if i in k1:
                        results.append(k)
    return results


def printtable(table, wordlist):
    print "    ", wordlist
    for row in table:
        print row

def parse(sentence):
    global grammar
    # Create the table; index j for rows, i for columns
    length = len(sentence)
    score = [None] * (length)
    prob_table = DefaultDict(float)
    trace = {}
    list2=[]

    for j in range(length):
        score[j] = [None] * (length+1)
        for i in range(length+1):
            score[j][i] = []
            
    # Fill the diagonal of the table with the parts-of-speech of the words
    for k in range(1,length+1):
        results = producers(sentence[k-1])
        for item in results:
            try:
                prob = grammar[item][sentence[k-1],]
            except:
                prob = grammar[item]['<unk>',]
            prob_table[k-1,k, item] = prob
        score[k-1][k].extend(results)

    #Weighted CYK
    for width in range(2,length+1): 
        for start in range(0,length+1-width): 
            end = start + width 
            for mid in range (start, end): 
                args = None
                for x in score[start][mid]: 
                    for y in score[mid][end]:
                        results = producers((x,y))
                        for item in results:
                            prob1 = grammar[item][(x,y)]
                            prob2 = prob1 + prob_table[start, mid, x] + prob_table[mid, end, y]
                            check = start, end, item
                            if check in prob_table:
                                if prob2 > prob_table[start, end, item]:
                                    prob_table[start, end, item] = prob2
                            else:
                                prob_table[start, end, item] = prob2
                            args2 = x, y, mid
                            if check in trace:
                                if prob2 >= prob_table[start, end, item]:
                                    args = x, y, mid
                                    trace[start, end, item] = args
                            else:
                                args = x, y, mid
                                trace[start, end, item] = args
                            if item not in score[start][end]:
                                score[start][end].append(item)

    
    try:
        if prob_table[0, length, 'TOP']:
            return  get_tree(sentence, trace, 0, length, 'TOP')
    except:
        print "",
#         print "The Tags Table"
#         printtable(score, sentence)
#         print "\nProbability Table"
#         print prob_table
#         print "\n log probability"
#         print prob_table[(0, length, 'TOP')]
#         print "\n trace tree"
#         print trace
    
    

def get_tree(x, trace, i, j, X):
    n = j - i
    if n == 1:
        return (X, x[i])
    else:
        Y, Z, s = trace[i, j, X]
        return [X, get_tree(x, trace, i, s, Y),
                   get_tree(x, trace, s, j, Z)]
        


if __name__ == '__main__':
    
    FileRead()
    ReadStringFile()
