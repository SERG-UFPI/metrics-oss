from dataclasses import dataclass


@dataclass
class Author:
    name: str
    commits: int
    projects: int
    added_lines: int
    removed_lines: int
    avg_files: float
