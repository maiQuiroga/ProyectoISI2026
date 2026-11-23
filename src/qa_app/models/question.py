import uuid
from datetime import date

from qa_app.extensions import db

question_tags = db.Table(
    "question_tags",
    db.Column(
        "question_id", db.String(36), db.ForeignKey("question.id"), primary_key=True
    ),
    db.Column("tag_id", db.String(36), db.ForeignKey("tag.id"), primary_key=True),
)


class Question(db.Model):
    __tablename__ = "question"

    id = db.Column(
        db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String(200), nullable = False)
    body = db.Column(db.Text, nullable = False)
    publication_date = db.Column(db.Date, nullable = False, default = date.today)
    # Autor humano que publicó la pregunta.
    author_id = db.Column(
        db.String(36), db.ForeignKey("HumanUser.id"), nullable=False
    )
    # Categoría asociada a la pregunta.
    category_id = db.Column(
        db.String(36), db.ForeignKey("category.id"), nullable=False
    )

    
    author = db.relationship("HumanUser", backref="question")
    category = db.relationship("Category", backref="question")
    tags = db.relationship("Tag", secondary=question_tags, backref="question")
    answers = db.relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )




    #Metodo
    def add_answer(self, answer) -> None:
        self.answers.append(answer)