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
    "dance"
}

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

    keywords = set(words)

    for keyword in KNOWN_KEYWORDS:

        if keyword in text:
            keywords.add(keyword)

    return expand_keywords(keywords)