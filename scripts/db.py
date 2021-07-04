from typing import List

from models import Base, Repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_connection():
    engine = create_engine("sqlite:///db.sqlite3")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def add_repos_to_db(repos: List):
    session = create_connection()

    bulk_repos = [Repository(**repo) for repo in repos]
    session.add_all(bulk_repos)

    try:
        session.commit()
    except Exception as e:
        print(f"An error ocurred trying to commit: {e}")

    session.close()
