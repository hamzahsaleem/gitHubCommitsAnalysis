# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 12:17:31 2017

@author: Fahad
"""

import networkx as nx
import csv
import datetime as d
import math
from datetime import datetime
from operator import itemgetter


file1reader = csv.reader(open("topDevsCommits.csv"), delimiter=",")

userProjects = {}
next(file1reader)
index = 0
user_commits = {}
project_commits = {}
for row in file1reader:
    #print(index)
    #index+=1
    timestamp = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S UTC')
    (year, week, day) = d.date(timestamp.year, timestamp.month, timestamp.day).isocalendar()    
    #dict format key:(UserID, ProjectID, Year, Week) value: Commits
    if user_commits.get((row[0],row[2],year,week)) is None:
        user_commits[(row[0],row[2],year,week)] = 1
    else:
        user_commits[(row[0],row[2],year,week)] += 1
    if project_commits.get((row[2],year,week)) is None:
        project_commits[(row[2],year,week)] = 1
    else:
        project_commits[(row[2],year,week)] += 1    
    if (row[0], year, week) in userProjects:
        #key = userId, year, week; value = day, projectId
        userProjects[(row[0], year, week)].append((day,row[2]))
    else:
        userProjects[(row[0], year, week )] = [(day,row[2])]

index = 0

#sort the projects according to days of week

#graphList = []

#testing asasasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

#userProjects2 = {}
#userProjects2[('20603', 2016, 9)] = userProjects[('20603', 2016, 9)]
#del userProjects

#userProjects = userProjects2


#testing asasasaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
day_day_focus = open('DaytoDay.csv', 'w',newline='')
avgproj = csv.writer(day_day_focus)
avgproj.writerow(['User_ID','Year','Week','S_switch'])
S_switch = 0

for key in userProjects.keys():
        index+=1
        #print(index)
        print(key)
        userProjects[key] = sorted(userProjects[key],key=itemgetter(0))
        daysProjects={}
        for item in userProjects[key]:
        	if item[0] not in daysProjects:
        		daysProjects[item[0]] = [item[1]]
        	else:
        		daysProjects[item[0]].append(item[1])	        
        DG=nx.DiGraph(UserID = key[0], Year = key[1], Week = key[2])
        prev = 0
        curr = 0         
        for item in userProjects[key]:            
            if curr != item[0]:
                prev = curr
                curr = item[0]
            if item[1] not in DG.nodes():
                DG.add_node(item[1])            
            if prev != 0:
                for pre in daysProjects[prev]:
                    if item[1] in DG.successors(pre):
                        DG[pre][item[1]]['weight'] += 1
                    else:
                        DG.add_edge(pre,item[1],weight = 1)        
        #S_switch = 0
        nodes = DG.nodes()
        for node in nodes:
            all_neighbor_edges = DG.out_edges(node,data=True)
            edge_weight_sum = 0
            for edge in all_neighbor_edges:
                edge_weight_sum += edge[2]['weight']            
            sum_p_ji = 0
            for edge in all_neighbor_edges:
                p_ji = edge[2]['weight']/edge_weight_sum
                sum_p_ji += p_ji * math.log2(p_ji)                
            p_i = user_commits.get((key[0],node,key[1],key[2]))/project_commits.get((node,key[1],key[2]))
            S_switch += p_i * sum_p_ji        
        avgproj.writerow([key[0],key[1],key[2],str(-1*S_switch)])
        S_switch = 0
        DG = None
day_day_focus.close()
        #graphList.append(DG)
        #del userProjects[key]
        



#G=nx.path_graph(4)
#nx.write_gexf(G, "test.gexf")