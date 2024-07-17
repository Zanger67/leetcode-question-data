import requests
import json

from os import mkdir
from os.path import join, isdir

import pickle
import pandas as pd

DATA_PATH = 'data/'

JSON_FILE = join(DATA_PATH, 'leetcode.json')
JSON_FILE_ONELINER = join(DATA_PATH, 'leetcode_oneline.json')
PICKLE_FILE = join(DATA_PATH, 'leetcode.pkl')

# Edit readme updater to take from a single pickle and remove this later
PICKLE_FILE_TOPICS = join(DATA_PATH, 'leetcode_topics.pkl')
PICKLE_FILE_QUESTIONS = join(DATA_PATH, 'leetcode_questions.pkl')

CSV_FILE = join(DATA_PATH, 'leetcode.csv')

def generate_pickle(data: dict) -> None:
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(data, f)

def query() -> dict:
    '''
    ### Returns:
    - `responseDict`: dict
        - Dictionary containing the json data
    '''
    url = 'https://leetcode.com/graphql/'

    questionCount = {
        "query":
            """query problemsetQuestionList(
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
                            questions: data 
                            {
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
    
    # For a JSON that has no indentation or new lines
    with open(JSON_FILE_ONELINER, 'w') as f:
        json.dump(responseDict, f)
    
    # For a JSON that's aesthentically readable
    response = json.dumps(responseDict, indent=4)
    with open(JSON_FILE, 'w') as f:
        f.write(response)
        
    return responseDict


def main() -> None :
    if not isdir(DATA_PATH):
        mkdir(DATA_PATH)
    
    question_data = query()
    generate_pickle(question_data)

if __name__ == '__main__':
    main()
