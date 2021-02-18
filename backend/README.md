# Full Stack Trivia API Backend

## Getting started

### Database setup
This project uses postgresql as a database.
```shell script
createdb trivia
```

### Run
```shell script
cd backend
python3 -m venv venv --prompt "nano project by an uzbek coder"
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=flaskr
export FLASK_DEBUG=true
flask run

```


And navigate to http://localhost:3000

## Testing
To run all tests (linux/macOS):
```
./test
```

## API documentation
All api methods return JSON. POST endpoints accept JSON.
### Get all categories
#### Endpoint
`GET /categories`

#### Query parameters
None

#### Sample request
`curl "http://localhost:5000/categories"`

The above command returns JSON structured like this:
```json
{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### Raises
This endpoint doesn't raise any errors


### Get all questions
#### Endpoint
`GET /questions`

#### Query parameters
Parameter | Type     | Default | Description
----------|----------|---------|------------
page      | `Number` | 1       | Intended page (10 questions per page)

#### Sample request
`curl "http://localhost:5000/questions"`

The above command returns JSON structured like this:
```json

{
  "success": true,
  "categories": {
    "1": "Science",
    "2": "..."
  },
  "questions": [
    {
      "id": 1,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "answer": "Apollo 13",
      "category": "Entertainment",
      "category_id": 5,
      "difficulty": 4
    },
    {
      "id": 2,
      "question": "..."
    }
  ],
  "total_questions": 19
}
```

#### Raises
This endpoint doesn't raise any errors


### Search for questions
#### Endpoint
`POST /questions`

#### Query parameters
Parameter  | Type     | Description
-----------|----------|------------
searchTerm | `String` | Search string (case-insensitive)

#### Sample request
```shell script
curl "http://localhost:5000/questions" \
  -X POST \
  -H "Content-Type: application/json" \
  --DATA '{"searchTerm": "world"}'
```

The above command returns JSON structured like this:
```json




{
  "success": true,
  "questions": [
    {
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "answer": "Brazil",
      "category": "Sports",
      "category_id": 6,
      "difficulty": 3
    },
    {
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "answer": "Uruguay",
      "category": "Sports",
      "category_id": 6,
      "difficulty": 4
   }
 ]
}
```

#### Raises
This endpoint doesn't raise any errors


### Create a new question
#### Endpoint
`POST /questions`

#### Post parameters
Parameter  | Type     | Description
-----------|----------|------------
question   | `String` | Text of the question
answer     | `String` | Answer of the question
category   | `Number` | ID of the category the question will belong
difficulty | `Number` | Difficulty score (usually between 1 and 5)

#### Sample request
```shell script
curl "http://localhost:5000/questions" \
   -X POST \
   -H "Content-Type: application/json" \
   --DATA '{
     "question": "Answer to the ultimate question",
     "answer": "42",
     "category": 2,
     "difficulty": 1
   }'
```

The above command returns JSON structured like this:
```json

{
  "success": true,
  "question_id": 20
}
```

#### Raises
**400** if any required field is missing/malformed, or if category doesn't exist


### Delete a question
#### Endpoint
`DELETE /questions/<id>`

#### Query parameters
Parameter | Type     | Description
----------|----------|------------
id        | `Number` | The ID of the question to delete

#### Sample request
```
curl "http://localhost:5000/questions/1" \
  -X DELETE
```

The above command returns JSON structured like this:
```json

{
  "success": true
}
```

#### Raises
**404** if question doesn't exist


### Get questions that belong to a category
#### Endpoint
`GET /categories/<id>/questions`

#### Query parameters
Parameter | Type     | Description
----------|----------|------------
id        | `Number` | The ID of the category

#### Sample request
```
curl "http://localhost:5000/categories/2/questions"
```

The above command returns JSON structured like this:
```json

{
  "success": true,
  "questions": [
    {
      "id": 16,
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?",
      "answer":"Escher",
      "category": "Art",
      "category_id": 2,
      "difficulty": 1
    },
    {
      "id": 21,
      "question": "..."
    }
  ]
}
```

#### Raises
**404** if category doesn't exist

### Play quiz
#### Endpoint
`POST /quizzes`

#### Post parameters
Parameter          | Type            | Description
-------------------|-----------------|------------
previous_questions | `Array<Number>` | Array of question ID's that user already answered
quiz_category      | `Object`        | Category by which the next question should be selected

#### Sample request
```
curl "http://localhost:5000/quizzes" \
  -X POST \
  -H "Content-Type: application/json" \
  --DATA '{"quiz_category": {"type": "Science", "id": 1}}'
```

The above command returns JSON structured like this:
```json

{
  "success": true,
  "question": {
    "id": 21,
    "question": "Who discovered penicillin?",
    "answer": "Alexander Fleming",
    "category": "Science",
    "category_id": 1,
    "difficulty": 3
  }
}
```

#### Raises
**400** if category doesn't exist, or is malformed (see sample command above)

#### Notes
`question` field is empty if there are no questions left
