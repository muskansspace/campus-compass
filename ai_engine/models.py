from dataclasses import dataclass
from typing import List


@dataclass
class StudentProfile:
    name: str
    year: str
    branch: str
    skills: List[str]
    interests: List[str]
    hours_per_week: float
    other_skills: str = ""
    other_interests: str = ""