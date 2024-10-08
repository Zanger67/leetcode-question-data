# leetcode-question-data

This repository will automatically query for the full list of LeetCode questions once a week with all data being saved in `data/`. I made this for a few other projects I've worked on just in order to have an updated list without having to manually query [leetcode.com](leetcode.com) redundantly, especially given the size of the query.

The data can be found in the following file formats:
- [JSON (Pretty)](https://raw.githubusercontent.com/Zanger67/leetcode-question-data/main/data/leetcode.json)
- [JSON (Single Line)](https://raw.githubusercontent.com/Zanger67/leetcode-question-data/main/data/leetcode_s.json)
- Pickle (Python Dictionary pickled using the pickle package)

## Update Times
- All question data (including newly added questions)
  - `5:00 AM UTC` (shortly after the weekly contest since at least 4-8 questions will be added by then)
- Daily / Weekly Questions
  - `0:05 AM UTC` (shortly after the daily updates)

## How to Use
Since most of the projects I wanted to use this for are GitHub-based, I created GitHub Actions to auto import or retrieve the JSON from this repo.

### Github Actions (repo updating)
If you want your own repo to be updated at certain times, you could do something like this inside a `GitHub action`...

```powershell
git clone https://github.com/Zanger67/leetcode-question-data.git temp
cp 'temp/data/leetcode.json' 'leetcode.json'
```

This would copy the most recent file into your own repo. Optionally, you could have it commit that file with this following...

```powershell
git config --global user.name "Zanger67/query-data"
git config --global user.email "Zanger67[bot]@Zanger67.github.io"
git add 'leetcode.json'
git commit -m 'Updated question data' || exit 0
git push
```

If you don't need a constantly updated list, you can decrease the frequency of your updates or just download the JSON directly.

Below is an example of how it would look in a GitHub action:

```yml
name: '[Updating LeetCode question data]'

on:
    schedule:
        - cron: "15 5 * * 0"    # runs at 5:15 am UTC on SUNDAYS
    workflow_dispatch:

permissions: 
    contents: write

jobs: 
    build:
        runs-on: ubuntu-latest
        steps:
            - name: Checkout the current repository content
              uses: actions/checkout@v2
              with:
                submodules: "true"

            - name: Clone data and copy
              run: |
                git clone https://github.com/Zanger67/leetcode-question-data.git temp
                cp 'temp/data/leetcode.json' 'leetcode.json'

            - name: Commit and push the updated JSON file
              run: |
                git config --global user.name "Zanger67/query-data"
                git config --global user.email "Zanger67[bot]@Zanger67.github.io"
                git add 'leetcode.json'
                git commit -m 'Updated question data' || exit 0
                git push
```

### Clone when needed / submodule

I also use this repo as a submodule where I simply update the submodule so the data is most recent when it's needed. See [here](https://github.com/Zanger67/WikiLeet/blob/main/action.yml) for an example where it initializes both submodules and recursively udpates them. This could also be done with cloning and avoiding adding it when you commit.

## Future Planned Additions
- CSV
- Links to question in the JSON directly


## Formatting Details

`Slug`: the `snake-case` name used at the end of [LeetCode.com](LeetCode.com) urls for each question
`paidOnly:` premium or not


### [Leetcode.json](data/leetcode.json)
```json
{
    "data": {
        "problemsetQuestionList": {
            "total": 3230,
            "questions": [
                {
                    "acRate": 53.181370001706604,
                    "difficulty": "Easy",
                    "freqBar": null,
                    "frontendQuestionId": "1",
                    "isFavor": false,
                    "paidOnly": false,
                    "status": null,
                    "title": "Two Sum",
                    "titleSlug": "two-sum",
                    "topicTags": [
                        {
                            "name": "Array",
                            "id": "ASDF1234=",
                            "slug": "array"
                        },
                        {
                            "name": "Hash Table",
                            "id": "QWER6789=",
                            "slug": "hash-table"
                        }
                    ],
                    "hasSolution": true,
                    "hasVideoSolution": true
                },
                ...
                ... etc.
                ...
            ]
        }
    }
}
```

### [Dailies](data/dailies_weeklies/dailies.json)
```json
{
    "2024-06-01": {
        "date": "2024-06-01",
        "userStatus": "NotStart",
        "link": "/problems/score-of-a-string/",
        "question": {
            "questionFrontendId": "3110",
            "title": "Score of a String",
            "titleSlug": "score-of-a-string"
        }
    },
    ...
    ... etc.
    ...
}
```


### [Weeklies](data/dailies_weeklies/weeklies.json)
```json
{
    "2024-06-01": {
        "date": "2024-06-01",
        "userStatus": "NotStart",
        "link": "/problems/longest-common-subsequence-between-sorted-arrays/",
        "question": {
            "questionFrontendId": "1940",
            "title": "Longest Common Subsequence Between Sorted Arrays",
            "titleSlug": "longest-common-subsequence-between-sorted-arrays",
            "isPaidOnly": true
        }
    },
    ...
    ... etc.
    ...
}
```