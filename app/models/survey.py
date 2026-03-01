from app.extensions import db
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum

# ENUM для статусов опроса
class SurveyStatus(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    CLOSED = 'closed'

# ENUM для типов вопросов
class QuestionType(Enum):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    TEXT = 'text'


class Survey(db.Model):
    __tablename__ = 'surveys'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(
        SQLAlchemyEnum(
            SurveyStatus, 
            name='survey_status', 
            create_type=False,
            values_callable=lambda obj: [e.value for e in obj]
        ), 
        default=SurveyStatus.DRAFT,
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Связи
    questions = db.relationship('Question', backref='survey', lazy=True, cascade='all, delete-orphan')
    responses = db.relationship('Response', backref='survey', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_questions=False):
        """Конвертация опроса в словарь для JSON"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'author_id': self.author_id
        }
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions]
        return data


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    q_type = db.Column(
        SQLAlchemyEnum(
            QuestionType, 
            name='question_type', 
            create_type=False,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False
    )
    order = db.Column(db.Integer, default=0)

    # Связи
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Конвертация вопроса в словарь"""
        return {
            'id': self.id,
            'text': self.text,
            'type': self.q_type.value,
            'order': self.order,
            'options': [opt.to_dict() for opt in self.options] if self.options else None
        }


class Option(db.Model):
    __tablename__ = 'options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text
        }