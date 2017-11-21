#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 12:05:52 2017

@author: hamzasaleem
"""
import csv
import datetime as d
from datetime import datetime, date, time


file1reader = csv.reader(open("topDevsCommits.csv"), delimiter=",")

userProjects = {}

next(file1reader)
index = 0

for row in file1reader:
    print(index)
    index+=1
    timestamp = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S UTC')
    (year, week, day) = d.date(timestamp.year, timestamp.month, timestamp.day).isocalendar()
    
    if (row[0], year, week,day) in userProjects:
        userProjects[(row[0], year, week, day)].append((row[2]))
    else:
        userProjects[(row[0], year, week, day)] = [(row[2])]

index = 0

#userCommitCountDf = p.DataFrame.from_records(userCommitCount, columns=labels)


with open('output.csv', 'w') as csvfile:
    fieldnames = ['User_ID', 'Year', 'Week', 'Day', 'No_Of_Projects']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for key in userProjects.keys():
        index+=1
        print(index)
        writer.writerow({'User_ID': key[0], 'Year': key[1], 'Week': key[2], 'Day': key[3], 'No_Of_Projects': len(set(userProjects[key]))  })
        

    
file1reader = csv.reader(open("output.csv"), delimiter=",")    
userWeeklyAvgProjects = {}
next(file1reader)
index = 0


for row in file1reader:
    print(index)
    index+=1
    
    if (row[0], row[1], row[2]) in userWeeklyAvgProjects:
        userWeeklyAvgProjects[(row[0], row[1], row[2])] = ( userWeeklyAvgProjects[(row[0], row[1], row[2])][0]+1 , userWeeklyAvgProjects[(row[0], row[1], row[2])][1]+int(row[4]))
    else:
        userWeeklyAvgProjects[(row[0], row[1], row[2])] = (1,int(row[4]))

for key in userWeeklyAvgProjects.keys():
    userWeeklyAvgProjects[key] = userWeeklyAvgProjects[key][1]/userWeeklyAvgProjects[key][0]


with open('topDevsAvgProjects_Metric1.csv', 'w') as csvfile:
    fieldnames = ['User_ID', 'Year', 'Week', 'Avg_Projects']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for key in userWeeklyAvgProjects.keys():
        index+=1
        print(index)
        writer.writerow({'User_ID': key[0], 'Year': key[1], 'Week': key[2], 'Avg_Projects': userWeeklyAvgProjects[key]  })
        