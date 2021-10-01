import datetime
from typing import List

from models import Base, CloneInfo, Repository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


def create_connection() -> Session:
    engine = create_engine("sqlite:///db.sqlite3")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def commit_session(session) -> None:
    try:
        session.commit()
    except Exception as e:
        print(f"An error ocurred trying to commit: {e}")

    session.close()


def add_repos_to_db(repos: List) -> None:
    session = create_connection()

    bulk_repos = [Repository(**repo) for repo in repos]
    session.add_all(bulk_repos)

    commit_session(session)


def add_clone_info(repo_id: int, error: str) -> None:
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


def query_clone_info(repo_id: int, session: Session = None) -> CloneInfo:
    if session is None:
        session = create_connection()

    return session.query(CloneInfo).filter(CloneInfo.repository_id == repo_id).first()


def get_all_repositories(session: Session = None):
    if session is None:
        session = create_connection()

    return session.query(Repository).all()


def get_all_repos_given_clone_info(session: Session = None):
    if session is None:
        session = create_connection()

    now = datetime.datetime.utcnow()
    one_month_ago = now - datetime.timedelta(days=30)

    return (
        session.query(Repository)
        .join(CloneInfo)
        .filter(CloneInfo.repo_id == Repository.id)
        .filter(CloneInfo.updated_at > one_month_ago)
        .all()
    )


def update_clone_info(repo_id: int, error: str = "") -> None:
    session = create_connection()

    info = query_clone_info(repo_id, session)

    if info is None or not info:
        session.close()

        add_clone_info(repo_id, error)
    else:
        info.error = error
        info.updated_at = datetime.datetime.utcnow()

        commit_session(session)
