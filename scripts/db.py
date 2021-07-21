import datetime
from typing import List

from models import Base, CloneInfo, Repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_connection():
    engine = create_engine("sqlite:///db.sqlite3")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def commit_session(self, session):
    try:
        session.commit()
    except Exception as e:
        print(f"An error ocurred trying to commit: {e}")

    session.close()


def add_repos_to_db(repos: List):
    session = create_connection()

    bulk_repos = [Repository(**repo) for repo in repos]
    session.add_all(bulk_repos)

    commit_session(session)


def add_clone_info(repo_id: int, error: str):
    session = create_connection()

    clone_data = {
        "repository_id": repo_id,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
        "error": error,
    }

    info = CloneInfo(**clone_data)
    session.add(info)

    commit_session(session)
