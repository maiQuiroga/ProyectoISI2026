from src.qa_app.extensions import db
import enum
import uuid


class RoleType (enum.Enum):
    ADMIN = "Admin"
    GENERAL_USER = "GeneralUser"



class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.String(36), primary_key = True, default = lambda: str (uuid.uuid4()))
    name = db.Column(db.String(100), nullable = False)
    type = db.Column(db.String(50))                       #Guarda que hijo es 

    __mapper_args__ = {
        "polymorphic_identity": "author",  #padre
        "polymorphic_on": type,   
    }


    #Method

    def get_name(self) -> str:
        return self.name


class HumanUser(Author):
    __tablename__ = "HumanUser"


    id = db.Column(db.String(36), db.ForeignKey("author.id"), primary_key = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(250), nullable = False)
    role = db.Column(db.Enum(RoleType), nullable = False, default = RoleType.GENERAL_USER)


    __mapper_args__ = {
        "polymorphic_identity": "HumanUser",
    }



class AiAgent(Author):
    __tablename__ = "AiAgente"


    id = db.Column(db.String(36), db.ForeignKey("author.id"), primary_key = True)
    provider = db.Column(db.String(100), nullable = False)
    version = db.Column(db.String(50), nullable = False)


    __mapper_args__ = {
        "polymorphic_identity": "AiAgente",
    }