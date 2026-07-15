import re

"""
Utility functions for keyword extraction and semantic matching.
"""

KNOWN_KEYWORDS = {

    # Programming
    "python", "java", "c programming", "c++", "javascript",
    "html", "css", "sql",

    # Tools
    "react", "node", "git", "github", "aws",
    "cloud", "docker", "linux",

    # AI
    "ai",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "computer vision",
    "nlp",
    "data science",

    # Development
    "web development",
    "app development",
    "frontend",
    "backend",

    # Domains
    "blockchain",
    "cybersecurity",
    "cyber security",
    "robotics",
    "web3",

    # Core
    "dsa",
    "problem solving",
    "competitive programming",
    "research",
    "leadership",
    "teamwork",
    "communication",
    "personality development",
    "public speaking",
    "event management",

    # Creative
    "design",
    "ui",
    "ux",
    "ui/ux",
    "photography",

    # Dataset specific
    "tech",
    "technology",
    "technical",
    "coding",
    "programming",
    "innovation",
    "hardware",
    "networking",
    "open source",
    "community",
    "community building",
    "current affairs",
    "debate",
    "mun",
    "literature",
    "oration",
    "finance",
    "entrepreneurship",
    "social impact",
    "music",
    "dance",
    "theatre",
    "street play",
    "instruments",
    "economics",
    "skill development",

    # Added to support expanded Home.py skill/interest dropdowns —
    # these terms appear literally in society domain/skills text
    # but weren't recognized before, so selecting them never matched.
    "ai/ml",
    "creative writing",
    "content writing",
    "data analysis",
    "video editing",
    "mental health",
    "sustainability",
    "women empowerment",
    "mechanical design",
}

# -------------------------------------------------
# Canonical Concept Map
# -------------------------------------------------
# Several recognized keywords are really the same underlying concept
# expressed different ways (a society description that says "tech,
# technical, engineering, innovation" isn't 4 distinct things — it's
# one "this is a tech society" signal said 4 times). Without collapsing
# these, tech-heavy societies racked up 3-4x the match count of a
# niche society (e.g. B.H.A.V, whose only concepts are "public
# speaking", "debate", "mun", "creative writing") purely because their
# descriptions are wordier — not because the student is a better fit.
# Canonicalizing keeps each concept worth exactly one match, on both
# the society side and the student side.
CANONICAL_MAP = {
    "tech": "technology",
    "technical": "technology",
    "engineering": "technology",
    "innovation": "technology",

    "artificial intelligence": "ai",
    "machine learning": "ai",
    "deep learning": "ai",

    "ui": "ui/ux",
    "ux": "ui/ux",

    "community building": "community",

    "cyber security": "cybersecurity",

    "web development":"webdev",
}

def canonicalize(keyword):
    return CANONICAL_MAP.get(keyword, keyword)


STOP_WORDS = {
    "the","a","an","and","or","for","of","to","in",
    "on","with","at","by","from","into","is","are",
    "interest","interested","basic","good","strong",
    "passion","enthusiasm","preferred","knowledge",
    "skills","skill","learn","learning","contribute",
    "consistently","required"
}

SYNONYMS = {

    "python": {
        "python",
        "programming",
        "coding"
    },

    "git": {
        "git",
        "github",
        "version control"
    },

    "aws": {
        "aws",
        "cloud",
        "cloud computing",
        "amazon web services"
    },

    "machine learning": {
        "machine learning",
        "ai",
        "artificial intelligence",
        "deep learning"
    },

    "web development": {
        "frontend",
        "backend",
        "html",
        "css",
        "javascript",
        "react"
    },

    "tech": {
        "technology",
        "technical",
        "innovation",
        "engineering"
    }
}


def expand_keywords(words):

    expanded = set(words)

    for word in list(words):

        for values in SYNONYMS.values():

            if word in values:
                expanded.update(values)

    return expanded


def extract_keywords(text):

    if text is None:
        return set()

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9+#/ ]", " ", text)

    words = {
        w.strip()
        for w in text.split()
        if len(w) > 2 and w not in STOP_WORDS
    }

    # Only keep words that are recognized, meaningful keywords.
    # Previously EVERY non-stopword token (e.g. "join", "opportunity",
    # "students", "team") was treated as a keyword, which diluted the
    # match score with noise unrelated to actual skills/domains.
    keywords = {w for w in words if w in KNOWN_KEYWORDS}

    for keyword in KNOWN_KEYWORDS:

        # Word-boundary check instead of plain substring — plain "in text"
        # caused false positives like "mun" matching inside "community",
        # or "ai" matching inside "maintain"/"domain".
        pattern = r"(?<![a-z0-9])" + re.escape(keyword) + r"(?![a-z0-9])"

        if re.search(pattern, text):
            keywords.add(keyword)

    return {canonicalize(k) for k in expand_keywords(keywords)}