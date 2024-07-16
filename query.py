from typing import Tuple

import requests
import json

from os.path import join

import pickle
import pandas as pd

DATA_PATH = 'scripts/'

JSON_FILE = join(DATA_PATH, 'leetcode.json')
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

    questionCount = {"query":"query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    }\n}\n    ",
                     "variables":{"categorySlug":"all-code-essentials",
                                  "skip":0,
                                  "limit":1,
                                  "filters":{}
                                 },
                     "operationName":"problemsetQuestionList"
                     }

    questionCount = requests.post(url=url, json=questionCount).json()
    questionCount = questionCount['data']['problemsetQuestionList']['total']

    print(f'Total number of questions: {questionCount}')

    body = {"query":"query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList: questionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    total: totalNum\n    questions: data {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      topicTags {\n        name\n        id\n        slug\n      }\n      hasSolution\n      hasVideoSolution\n    }\n  }\n}\n    ",
            "variables":{"categorySlug":"all-code-essentials",
                         "skip":0,
                         "limit":questionCount,
                         "filters":{}
                         },
            "operationName":"problemsetQuestionList"
            }

    responseDict = requests.post(url=url, json=body).json()
    response = json.dumps(responseDict, indent=4)

    with open(JSON_FILE, 'w') as f:
        f.write(response)
        
    return responseDict


def main() -> None :
    question_data = query()
    generate_pickle(question_data)

if __name__ == '__main__':
    main()
