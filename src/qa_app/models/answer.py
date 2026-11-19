from datetime import date
import uuid
from src.qa_app.extensions import db

class Answer(db.Model):
    __tablename__ = "answer"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    body = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.Date, nullable=False, default=date.today)
    is_accepted = db.Column(db.Boolean, nullable=False, default=False)
    author_id = db.Column(db.String(36), db.ForeignKey("author.id"), nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey("question.id"), nullable=False)

    # Relaciones
    author = db.relationship("Author", backref="answers")
    question = db.relationship("Question", back_populates="answers")

    def mark_accepted(self) -> bool:
        self.is_accepted = True
        return self.is_accepted