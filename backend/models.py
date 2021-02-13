from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

database_name = "trivia"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'postgres', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Question
'''
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category_id = Column('category', Integer, ForeignKey('categories.id'),
                         nullable=False)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def __repr__(self):
        return f'<Question {self.id} {self.question[:20]}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.type,
            'category_id': self.category_id,
            'difficulty': self.difficulty,
        }


'''
Category
'''
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = relationship('Question', backref='category', lazy=True)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f'<Category {self.id} {self.type}>'

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
        }
