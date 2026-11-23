import os
from pathlib import Path


class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
	SQLALCHEMY_DATABASE_URI = os.environ.get(
		"DATABASE_URL",
		f"sqlite:///{Path(__file__).resolve().parents[2] / 'instance' / 'qa_app.db'}",
	)
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	LOCAL_AUTHOR_EMAIL = "usuario-local@localhost"
