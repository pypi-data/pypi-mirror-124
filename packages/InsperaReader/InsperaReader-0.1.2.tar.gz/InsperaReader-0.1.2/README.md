# inspera-reader
A tool to parse the output of exams/assignments from Inspera

## setup
`pip install InsperaReader`

## usage
Can be used either in python directly or as a command-line tool to create the dataset directly.
### in python
```
from inspera import InsperaReader
reader = InsperaReader('path/fall_exam_2021.json')

for candidate in reader.candidates():
    for question in candidate.questions():
        # access any desired field and build your data 
        my_custom_data = [question.id(), question.grading(), question.clean_response()]
        # or access the predefined make-row field, intended for further use with pandas
        my_custom_data = question.make_row()
```
peek data:
```
from inspera import InsperaReader
reader = InsperaReader('path/fall_exam_2021.json')
print(reader.candidates()[0].questions()[0].clean_response())
```

### command line (NOT IMPLEMENTED)
`python -m insperareader --file path --outfile path --name name`

a default setting that includes the following fields for each candidate's response (through `make_row`):
- question id
- responses
- parsed responses
- grading
- max score
- duration

## classes
### InsperaCandidate
- id (candidate id) -> int
- score (total score) -> int
- start_end (date_from - date_to) -> str
- questions (data related to each question in the assignment) -> list[InsperaQuestion]

### InsperaQuestion
- question_num -> int
- question_title -> str
- responses (raw data) -> list(str)
- clean_response (parsed data) -> list(str)
- grading (list of grades) -> list(int)
- grader (name of graders) -> list(str)
- max_score -> int
- duration -> int
- make_row -> list of above fields

Also implements a print override, containing simplified information.


# TODO:
- [ ] implement CLI
- [ ] generalize field names in a config file (e.g. yml)
