import datetime
import json
from typing import Text

from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Repository(Base):
    __tablename__ = "repository"
    id = Column(BigInteger, primary_key=True)
    node_id = Column(String)
    name = Column(String)
    full_name = Column(String)
    private = Column(Boolean)
    html_url = Column(String)
    description = Column(String)
    fork = Column(Boolean)
    url = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    pushed_at = Column(String)
    git_url = Column(String)
    ssh_url = Column(String)
    cloned_url = Column(String)
    svn_url = Column(String)
    homepage = Column(String)
    size = Column(BigInteger)
    stargazers_count = Column(Integer)
    watchers_count = Column(Integer)
    language = Column(String)
    has_issues = Column(Boolean)
    has_projects = Column(Boolean)
    has_downloads = Column(Boolean)
    has_wiki = Column(Boolean)
    has_pages = Column(Boolean)
    forks_count = Column(Integer)
    mirror_url = Column(String)
    archived = Column(Boolean)
    disabled = Column(Boolean)
    open_issues_count = Column(Integer)
    license = Column(String)
    forks = Column(Integer)
    open_issues = Column(Integer)
    watchers = Column(Integer)
    default_branch = Column(String)
    score = Column(Float)

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.node_id = kwargs.get("node_id")
        self.name = kwargs.get("name")
        self.full_name = kwargs.get("full_name")
        self.private = kwargs.get("private")
        self.html_url = kwargs.get("html_url")
        self.description = kwargs.get("description")
        self.fork = kwargs.get("fork")
        self.url = kwargs.get("url")
        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")
        self.pushed_at = kwargs.get("pushed_at")
        self.git_url = kwargs.get("git_url")
        self.ssh_url = kwargs.get("ssh_url")
        self.cloned_url = kwargs.get("cloned_url")
        self.svn_url = kwargs.get("svn_url")
        self.homepage = kwargs.get("homepage")
        self.size = kwargs.get("size")
        self.stargazers_count = kwargs.get("stargazers_count")
        self.watchers_count = kwargs.get("watchers_count")
        self.language = kwargs.get("language")
        self.has_issues = kwargs.get("has_issues")
        self.has_projects = kwargs.get("has_projects")
        self.has_downloads = kwargs.get("has_downloads")
        self.has_wiki = kwargs.get("has_wiki")
        self.has_pages = kwargs.get("has_pages")
        self.forks_count = kwargs.get("forks_count")
        self.mirror_url = kwargs.get("mirror_url")
        self.archived = kwargs.get("archived")
        self.disabled = kwargs.get("disabled")
        self.open_issues_count = kwargs.get("open_issues_count")
        self.license = (
            json.dumps(kwargs.get("license"))
            if kwargs.get("license") is not None
            else None
        )
        self.forks = kwargs.get("forks")
        self.open_issues = kwargs.get("open_issues")
        self.watchers = kwargs.get("watchers")
        self.default_branch = kwargs.get("default_branch")
        self.score = kwargs.get("score")

class CloneInfo(Base):
    __tablename__ = "clone_info"
    repository_id = Column(Integer, ForeignKey("repository.id"))
    repository = relationship("Repository", backref=backref("clone", uselist=False)) # One to One relationship
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    error = Column(Text)

    def __init__(self, **kwargs):
        self.repository_id = kwargs.get('repository_id')
        self.created_at = kwargs.get('created_at', datetime.datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', datetime.datetime.utcnow())
        self.error = kwargs.get('error', '')
