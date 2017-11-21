# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sentiment_tutorial]
"""Demonstrates how to make a simple call to the Natural Language API."""

# [START sentiment_tutorial_import]
import argparse
import glob, os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
# [END sentiment_tutorial_import]


# [START def_print_result]
def print_result(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    #for index, sentence in enumerate(annotations.sentences):
        #sentence_sentiment = sentence.sentiment.score
        #print('Sentence {} has a sentiment score of {}'.format(
            #index, sentence_sentiment))

    #print('Overall Sentiment: score of {} with magnitude of {}'.format(
        #score, magnitude))
    msg = str(score)+ ' '+ str(magnitude)
    return msg
# [END def_print_result]


# [START def_analyze]
def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()
    msg = ""
    
    with open(movie_review_filename, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(content=content,type=enums.Document.Type.PLAIN_TEXT)
    try:
        annotations = client.analyze_sentiment(document=document)
        movie_review_filename = movie_review_filename[:-4]
        msg = print_result(annotations)
        msg = movie_review_filename + ' ' + msg  
    except:
        print(movie_review_filename + ' couldnot be analyzed\n')
    
    return msg

    # Print the results
    
# [END def_analyze]


if __name__ == '__main__':
    
    os.chdir("/Users/hamzasaleem/Desktop/UserComments")
    #analyze('1051.txt')
    #os.chdir("/Users/hamzasaleem/Desktop/UserComments")
    
    file1 = open('/Users/hamzasaleem/Desktop/UserCommentsAnalysis.txt','w')
    
    for file in glob.glob("*.txt"):
        print(file)
        msg = analyze(file)
        if len(msg) != 0:
            file1.write(msg)
            file1.write('\n')
            
            
    file1.close()    
    
# [END sentiment_tutorial]
