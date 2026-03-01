from app.extensions import db
from datetime import datetime


class Response(db.Model):
    __tablename__ = 'responses'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Один пользователь может пройти опрос только один раз
    __table_args__ = (
        db.UniqueConstraint('survey_id', 'user_id', name='unique_user_survey_response'),
    )

    # Связи
    answers = db.relationship('Answer', backref='response', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'survey_id': self.survey_id,
            'user_id': self.user_id,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'answers': [a.to_dict() for a in self.answers]
        }


class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer, db.ForeignKey('responses.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text_value = db.Column(db.Text, nullable=True)  # Для текстовых вопросов
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'), nullable=True)  # Для вопросов с выбором

    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'text_value': self.text_value,
            'option_id': self.option_id
        }