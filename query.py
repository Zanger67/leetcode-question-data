import requests
import json

from datetime import datetime
from typing import Tuple

from os import listdir, mkdir
from os.path import join, isdir, isfile

from icecream import ic

import pickle
import pandas as pd

URL = 'https://leetcode.com/graphql/'
DAILY_CHALLENGES_START = {'year': 2020, 'month': 4}

DIRS = []

DATA_PATH = 'data/'

JSON_FILE = join(DATA_PATH, 'leetcode.json')
JSON_FILE_ONELINER = join(DATA_PATH, 'leetcode_s.json')
PICKLE_FILE = join(DATA_PATH, 'leetcode.pkl')

DIRS.append(DATA_PATH)

DAILIES_AND_WEEKLIES_DIR = join(DATA_PATH, 'dailies_weeklies/')

DW_CUMULATIVE_DAILIES = join(DAILIES_AND_WEEKLIES_DIR, 'dailies.json')
DW_CUMULATIVE_WEEKLIES = join(DAILIES_AND_WEEKLIES_DIR, 'weeklies.json')
DW_CUMULATIVE_DAILIES_S = join(DAILIES_AND_WEEKLIES_DIR, 'dailies_s.json')
DW_CUMULATIVE_WEEKLIES_S = join(DAILIES_AND_WEEKLIES_DIR, 'weeklies_s.json')

DW_FOLDERS = ['formatted/', 'oneliners/']
DW_FILE_FORMAT = join(DAILIES_AND_WEEKLIES_DIR, DW_FOLDERS[0], '{year}_{month}.json')
DW_FILE_FORMAT_ONELINER = join(DAILIES_AND_WEEKLIES_DIR, DW_FOLDERS[1], '{year}_{month}_s.json')

DIRS.extend([DAILIES_AND_WEEKLIES_DIR, 
             join(DAILIES_AND_WEEKLIES_DIR, DW_FOLDERS[0]), 
             join(DAILIES_AND_WEEKLIES_DIR, DW_FOLDERS[1])])

# Edit readme updater to take from a single pickle and remove this later
PICKLE_FILE_TOPICS = join(DATA_PATH, 'leetcode_topics.pkl')
PICKLE_FILE_QUESTIONS = join(DATA_PATH, 'leetcode_questions.pkl')

CSV_FILE = join(DATA_PATH, 'leetcode.csv')

from questionDataclass import questionDataclass as Question
def generate_pickle(questions: dict) -> None:
    '''Writes the JSON data into a pickled dictionary file for Python users'''
    
    output = {}
    for question in questions :
        questionNo = int(question['frontendQuestionId'])
        
        output[questionNo] = Question(questionNo=questionNo,
                                      acRate=question['acRate'],
                                      difficulty=question['difficulty'],
                                      isFavor=question['isFavor'],
                                      paidOnly=question['paidOnly'],
                                      title=question['title'],
                                      slug=question['titleSlug'],
                                      topics=[topic['name'] for topic in question['topicTags']],
                                      hasSolution=question['hasSolution'],
                                      hasVideoSolution=question['hasVideoSolution'])
        
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(output, f)

DEFAULT_DAILY_QUERY = {
    'query':
        '''
        query dailyCodingQuestionRecords(
            $year: Int!, 
            $month: Int!
            ) {
                dailyCodingChallengeV2(
                    year: $year, 
                    month: $month
                    ) {
                        challenges {
                            date
                            userStatus
                            link
                            question {
                                questionFrontendId
                                title
                                titleSlug
                            }
                        }
                        weeklyChallenges {
                            date
                            userStatus
                            link
                            question {
                                questionFrontendId
                                title
                                titleSlug
                                isPaidOnly
                            }
                        }
                    }
            }
        ''',
    "variables":{
        "year":2024,
        "month":7
    },
    "operationName":"dailyCodingQuestionRecords"
}

# This should use the same instance of the default similar to a static method
def getChallengeQuery(year: int, month: int, query: dict = DEFAULT_DAILY_QUERY) -> dict:
    query['variables'] = {'year': year, 'month': month}
    return query
    
        
def query_month_dailies(year: int, month: int) -> dict:
    return requests.post(url=URL, json=getChallengeQuery(year, month)).json()
    
        

def query_dailies(*,
                  start_year:int=DAILY_CHALLENGES_START['year'],
                  start_month:int=DAILY_CHALLENGES_START['month'],
                  reset:bool=False,
                  limit:int=-1,
                  force_print:bool=False) -> Tuple[dict, dict]:
    '''
    
    ### Parameters:
    - `reset`: bool
        - If `True`, will reset the query and re-query all the data.
    - `limit`: int
        - The number of queries to make. -1 default to avoid limit==0 check so no limit.
    '''

    year, month = start_year, start_month
    currentDate = datetime.now()
    
    weeklies = {}
    dailies = {}
    
    while year <= currentDate.year or (month <= currentDate.month and year == currentDate.year) :  
        curr_file = DW_FILE_FORMAT.format(year=year, month=month)
        curr_file_s = DW_FILE_FORMAT_ONELINER.format(year=year, month=month)
        ic(curr_file)
        
        if reset or not isfile(curr_file) :
            request = query_month_dailies(year, month)
            ic(json.dumps(request))
        
            with open(f'{curr_file_s}', 'w') as f:
                json.dump(request, f)
            with open(f'{curr_file}', 'w') as f:
                json.dump(request, f, indent=4)
                
                
            for daily in request['data']['dailyCodingChallengeV2']['challenges'] :
                ic(f'd:{daily["date"]}')
                dailies[daily['date']] = daily
            
            ic(request['data']['dailyCodingChallengeV2']['weeklyChallenges'])
            for weekly in request['data']['dailyCodingChallengeV2']['weeklyChallenges'] :
                ic(f'w:{weekly["date"]}')
                weeklies[weekly['date']] = weekly
                    
            limit -= 1
            if limit == 0 :
                break
                
        print(f'{year = }, {month = }')
        month += 1
        if month > 12 :
            month = 1
            year += 1
        
    print(weeklies)
    if force_print or limit < 0 :
        with open(DW_CUMULATIVE_DAILIES_S, 'w') as f:
            json.dump(dailies, f)
        with open(DW_CUMULATIVE_DAILIES, 'w') as f:
            json.dump(dailies, f, indent=4)
        with open(DW_CUMULATIVE_WEEKLIES, 'w') as f:
            json.dump(weeklies, f)
        with open(DW_CUMULATIVE_WEEKLIES_S, 'w') as f:
            json.dump(weeklies, f, indent=4)
        
    return (dailies, weeklies)
    
    
def query() -> dict:
    '''
    ### Returns:
    Queries leetcode.com/graphql for all questions and their details, writing the JSON to
    `leetcode.json` and `leetcode_oneline.json` files.
     
    - `responseDict`: dict
        - Dictionary containing the json data
    '''
    
    url = 'https://leetcode.com/graphql/'

    # Query to retrieve the number of questions present on LeetCode
    questionCount = {
        "query":
            """
            query problemsetQuestionList(
                $categorySlug: String, 
                $limit: Int, 
                $skip: Int, 
                $filters: QuestionListFilterInput
                ) {
                    problemsetQuestionList: questionList(
                        categorySlug: $categorySlug
                        limit: $limit
                        skip: $skip
                        filters: $filters
                        ) {
                            total: totalNum
                        }
                }
            """,
        "variables":{
            "categorySlug":"all-code-essentials",
            "skip":0,
            "limit":1,
            "filters":{}
        },
        "operationName":"problemsetQuestionList"
    }

    questionCount = requests.post(url=url, json=questionCount).json()
    questionCount = questionCount['data']['problemsetQuestionList']['total']

    print(f'Total number of questions: {questionCount}')


    # Query to retrieve all questions and their details based on the question count above
    body = {
        "query":
            """
            query problemsetQuestionList(
                $categorySlug: String, 
                $limit: Int, 
                $skip: Int, 
                $filters: QuestionListFilterInput
                ) {
                    problemsetQuestionList: questionList(
                        categorySlug: $categorySlug
                        limit: $limit
                        skip: $skip
                        filters: $filters
                        ) {
                            total: totalNum
                            questions: data {
                                acRate
                                difficulty
                                freqBar
                                frontendQuestionId: questionFrontendId
                                isFavor
                                paidOnly: isPaidOnly
                                status
                                title
                                titleSlug
                                topicTags {
                                    name
                                    id
                                    slug
                                }
                                hasSolution
                                hasVideoSolution
                            }
                        }
                }
            """,
        "variables":{
            "categorySlug":"all-code-essentials",
            "skip":0,
            "limit":questionCount,
            "filters":{}
        },
        "operationName":"problemsetQuestionList"
    }

    responseDict = requests.post(url=url, json=body).json()
    
    # Outputs a JSON that has no indentation or new lines
    with open(JSON_FILE_ONELINER, 'w') as f:
        json.dump(responseDict, f)
    
    # Outputs a JSON that's aesthentically readable using indents
    response = json.dumps(responseDict, indent=4)
    with open(JSON_FILE, 'w') as f:
        f.write(response)
        
    return responseDict




def main() -> None :
    for x in DIRS :
        if not isdir(x) :
            mkdir(x)
    
    print('Querying LeetCode...')
    question_data = query()
    
    print('Pickling dictionary...')
    generate_pickle(question_data['data']['problemsetQuestionList']['questions'])

    print('Querying LeetCode dailies...')
    # query_dailies(limit=4, force_print=True, reset=True)
    query_dailies()

    print('Complete. Exiting...')


if __name__ == '__main__':
    # ic.disable()
    
    main()
