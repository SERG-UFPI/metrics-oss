#! !/usr/bin/env python3
# -*- coding: utf-8 -*-
# enrich_repo.py

import subprocess
from sys import argv
from settings.settings import GITHUB_OAUTH_TOKEN

def enrich_repo(owner, repository):
  # Produce git and git_raw indexes from git repo
  subprocess.run(['p2o.py', '--enrich', '--index', 'git_raw',
    '--index-enrich', 'git', '-e', 'http://localhost:9200',
    '--no_inc', '--debug', 'git',
    f'https://github.com/{owner}/{repository}'])

  # Produce github and github_raw indexes from GitHub issues and prs
  subprocess.run(['p2o.py', '--enrich', '--index', 'github_raw',
    '--index-enrich', 'github', '-e', 'http://localhost:9200',
    '--no_inc', '--debug', 'github', owner, repository,
    '-t', GITHUB_OAUTH_TOKEN, '--sleep-for-rate'])
