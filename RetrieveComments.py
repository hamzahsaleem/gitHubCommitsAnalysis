#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  21 12:05:52 2017

@author: hamzasaleem
"""
import csv


file1reader = csv.reader(open("Commit_Comments.csv"), delimiter=",")

userComments = {}

next(file1reader)
index = 0

for row in file1reader:
    print(index)
    index+=1

    if row[0] in userComments:
        userComments[row[0]].append(row[3])
    else:
        userComments[row[0]] = [row[3]]


#userCommitCountDf = p.DataFrame.from_records(userCommitCount, columns=labels)


for key in userComments.keys():
    file = open('UserComments/'+key+'.txt','w')
    for comment in userComments[key]:
        file.write(comment)
        file.write('\n')
    file.close()     
    