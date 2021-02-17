import json
import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def __init__(self, methodName: str = ...):  # noqa
        super().__init__(methodName)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.categories_dict = {
            '1': 'Science',
            '2': 'Art',
            '3': 'Geography',
            '4': 'History',
            '5': 'Entertainment',
            '6': 'Sports',
        }

        self.new_question = {
            'question': 'Answer to the ultimate question',
            'answer': '42',
            'category': 1,
            'difficulty': 1,
        }
        self.bad_question = {
            'question': '',
            'answer': '',
            'category': 999,
            'difficulty': 1,
        }

        # how much a quiz randomness test should repeat
        self.quiz_tries = 1

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """GET /categories return all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'], self.categories_dict)

    def test_get_paginated_questions(self):
        """GET /questions returns first 10 questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data.get('total_questions'))
        self.assertEqual(data.get('categories'), self.categories_dict)

    def test_get_questions_beyond_valid_page_404(self):
        """GET /questions with invalid page raises 404"""
        res = self.client().get('/questions?page=999')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_create_new_question(self):
        """POST /questions endpoint creates new question"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(Question.query.get(data['question_id']))

    def test_create_question_400(self):
        """POST /questions with malicious data raises 400"""
        res = self.client().post('/questions', json=self.bad_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        """DELETE /questions/<id> endpoint deletes question"""
        question_id = Question.query.first().id
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(Question.query.get(question_id))

    def test_delete_question_404(self):
        """
        DELETE /questions/<id> with non existing question id
        raises 404
        """
        res = self.client().delete('/questions/999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        """POST /questions for searching questions works"""
        # note the case-insensitivity
        res = self.client().post('/questions', json={'searchTerm': 'ever'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)

    def test_search_non_existing_question(self):
        """
        POST /questions for searching non existing
        question returns empty list
        """
        res = self.client().post('/questions', json={'searchTerm': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)

    def test_get_category_questions(self):
        """
        GET /categories/<id>/questions returns all questions
        belonging to the category
        """
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])

    def test_get_category_questions_404(self):
        """
        GET /categories/<id>/questions raises 404 for non existing
        category id 999
        """
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_category_questions_beyond_valid_page(self):
        """GET /categories/<id>/questions raises 404 if page is invalid"""
        res = self.client().get('/categories/999/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quiz_no_previous_questions(self):
        """POST /quizzes returns a question"""
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_quiz_does_not_return_question_twice(self):
        """Returns random quiz every time"""
        cl = self.client()

        for _ in range(self.quiz_tries):
            res1 = cl.post('/quizzes', json={})
            data1 = json.loads(res1.data)
            q1 = data1['question']['id']
            res2 = cl.post('/quizzes', json={'previous_questions': [q1]})
            data2 = json.loads(res2.data)
            q2 = data2['question']['id']
            self.assertNotEqual(q1, q2)

    def test_quiz_with_category(self):
        """Returned quiz category matches requested category"""
        cid = 1
        res = self.client().post('/quizzes', json={'quiz_category': {'id': cid}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category_id'], cid)

    def test_quiz_invalid_category_id_400(self):
        """If category doesn't exist, raises 404"""
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 999}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_quiz_null_category_id_400(self):
        """If category is malformed, raises 400"""
        res = self.client().post('/quizzes', json={'quiz_category': {}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_quiz_no_quiz_left(self):
        """If no quiz left, returns None"""
        res = self.client().post('/quizzes', json={
            'previous_questions': list(range(
                Question.query.order_by(Question.id).first().id,
                Question.query.order_by(Question.id.desc()).first().id + 1,
            ))
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(data.get('question'))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()