import uuid
from src.qa_app.extensions import db


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.String(36), primary_key = True, default = lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique = True, nullable = False)