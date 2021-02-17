import os
import random
from sys import exc_info

import flask
from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def mock(*args, **kwargs):
    return {'success': True}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Enables CORS for all endpoints
    CORS(app)

    @app.after_request
    def after_request(response: flask.Response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    DONE:
    Create an endpoint to handle GET requests 
    for all available categories.
    '''

    @app.route('/categories')
    def all_categories():
        return {
            'success': True,
            'categories': {str(c.id): c.type for c in Category.query.all()},
        }

    '''
    DONE:
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
  
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    @app.route('/questions')
    def all_questions():
        """Returns questions paginated by 10"""
        questions = Question.query.all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        sliced_questions = questions[start:end]

        if page != 1 and not sliced_questions:
            # don't raise 404 on first page
            abort(404)

        formatted_questions = [q.format() for q in questions]
        categories = {str(c.id): c.type for c in Category.query.all()}

        return {
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': categories,
        }

    '''
    DONE:
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id: int):
        question = Question.query.get(id)
        if not question:
            abort(404)

        try:
            # we cannot use abort here because try block will catch it
            db.session.delete(question)
            db.session.commit()
            return {'success': True}

        except Exception:
            print(exc_info())
            abort(422)

    '''
    DONE:
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    @app.route('/questions', methods=['POST'])
    def post_question():
        data = request.get_json()
        search = data.get('searchTerm')

        if search is not None:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search}%')
            ).all()
            formatted_questions = [q.format() for q in questions]

            return {
                'success': True,
                'questions': formatted_questions,
            }
        else:
            try:
                category_id = int(data['category'])
                category = Category.query.get(category_id) or abort(400)  # 400 or 404?
                question = Question(
                    question=data['question'],
                    answer=data['answer'],
                    category=category,
                    difficulty=int(data['difficulty'])
                )
                db.session.add(question)
                db.session.commit()
                return {'success': True, 'question_id': question.id}
            except (TypeError, KeyError):
                print(exc_info())
                abort(400)

    '''
    DONE:
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    app.route('/categories/<int:id>/questions')(mock)

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    @app.errorhandler(400)
    def bad_request(_error):
        return {
            'success': False,
            'error': 400,
            'message': 'bad request',
        }, 400

    @app.errorhandler(404)
    def not_found(_error):
        return {
            'success': False,
            'error': 404,
            'message': 'not found',
        }, 404

    @app.errorhandler(422)
    def unprocessable(_error):
        return {
            'success': False,
            'error': 422,
            'message': 'unprocessable',
        }, 422

    @app.errorhandler(500)
    def internal_server_error(_error):
        return {
           'success': False,
           'error': 500,
           'message': 'internal server error',
        }, 500

    return app
