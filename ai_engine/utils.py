import re

"""
Utility functions for extracting predefined
keywords from text used in the recommendation engine.
"""

# All possible skills we want to detect
KNOWN_KEYWORDS = [

    # Programming Languages
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",

    # Frameworks / Tools
    "react",
    "node",
    "git",
    "github",
    "aws",
    "canva",

    # AI / ML
    "artificial intelligence",
    "ai",
    "machine learning",
    "deep learning",
    "computer vision",
    "nlp",
    "data science",

    # Domains
    "blockchain",
    "robotics",
    "cyber security",
    "cloud",

    # Development
    "web development",
    "app development",

    # Core Skills
    "problem solving",
    "competitive programming",
    "dsa",
    "communication",
    "leadership",
    "teamwork",
    "event management",
    "public speaking",
    "research",

    # Creative
    "photography",
    "design",
    "ui",
    "ux",
    "ui/ux"
]


def extract_keywords(text):
    """
    Extracts predefined keywords from text
    using case-insensitive whole-word matching.
    """

    if text is None:
        return set()

    text = str(text).lower()

    text = re.sub(r"[^\w\s+/#-]", " ", text)

    keywords = set()

    for keyword in KNOWN_KEYWORDS:

        pattern = r"\b" + re.escape(keyword) + r"\b"

        if re.search(pattern, text):
            keywords.add(keyword)

    return keywords