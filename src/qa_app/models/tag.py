import uuid
from src.qa_app.extensions import db


class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.String(36), primary_key = True, default = lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique = True, nullable = False)