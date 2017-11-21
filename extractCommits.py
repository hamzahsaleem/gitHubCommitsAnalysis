import datetime as d
import csv
import math
import os
import shutil
from github import Github
from datetime import datetime
import base64

def main():
    user_commits = {}
    parentDirectory = "CommitGathering"
    if os.path.exists(parentDirectory):    
        shutil.rmtree(parentDirectory)    
    os.makedirs(parentDirectory)
    gh = Github("m-shayanshafi","K@Rachi0315")

    with open('topDevsCommits.csv') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            timestamp = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S UTC')
            (year, week, day) = d.date(timestamp.year, timestamp.month, timestamp.day).isocalendar()
            if row[0] == '30351173':
                print('stop')

            if user_commits.get((row[0],year,week)) is None:

                print "New user commit being fetched..."
                if not os.path.exists(parentDirectory+"/"+str(row[0])):    
                    os.makedirs(parentDirectory+"/"+str(row[0]));

                thisUserPath = parentDirectory+"/"+str(row[0])

                if not os.path.exists(parentDirectory+"/"+str(row[0])+"/"+str(week)+"_"+str(year)):
                    os.makedirs(parentDirectory+"/"+str(row[0])+"/"+str(week)+"_"+str(year))

                thisDirectoryPath = parentDirectory+"/"+str(row[0])+"/"+str(week)+"_"+str(year)
                print "Commit fetch Started...\n"
                print("Week:"+str(week)+"\n")
                print("Year:"+str(year)+"\n")
                getCommitContents(row,thisDirectoryPath,gh)
                user_commits[(row[0],year,week)] = 1                

            else:

                print "Existing user commit being fetched..."
                thisDirectoryPath = parentDirectory+"/"+str(row[0])+"/"+str(week)+"_"+str(year)
                print "Commit fetch Started...\n"
                print("Week:"+str(week)+"\n")
                print("Year:"+str(year)+"\n")
                getCommitContents(row,thisDirectoryPath,gh)    
                user_commits[(row[0],year,week)] += 1


def getCommitContents(row, thisDirectoryPath,gh):
        
    try:
        thisCommitSha = row[5]; 
        thisProjectUrl = row[4];
        thisProjectFullName = str(thisProjectUrl.split("repos/",1)[1])
        thisRepo = gh.get_repo(thisProjectFullName)
        thisCommit = thisRepo.get_commit(thisCommitSha) 
        files = thisCommit.files
        
        print("User ID: "+str(row[0])+"\n");
        print("Commit Date: "+str(row[3])+"\n");
        print("Project Name:"+str(thisProjectFullName)+"\n")

        for file in files:                   
            try:
                thisFile = thisRepo.get_file_contents(file.contents_url.split("contents/",1)[1])
                fileData = base64.b64decode(thisFile.content)
                fileOut = open(thisDirectoryPath+"/"+thisFile.name, "w")
                fileOut.write(fileData)
                fileOut.close()
            except Exception as e:
                print e;
                continue;
        print "Commit fetched"
    except Exception as e:
            print e
            # continue;
        # sys.exit()
    
if __name__ == '__main__':
    main()