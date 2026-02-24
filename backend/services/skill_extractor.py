import re
from typing import List, Dict

# A predefined set of common skills for simple extraction.
# In a real application, this could be backed by an external API or NLP model.
COMMON_SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "react", "angular", "vue", "django", "flask", "fastapi", "spring", "node.js",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd", "git",
    "machine learning", "data analysis", "agile", "scrum", "project management",
    "html", "css", "rest api", "graphql"
}

def extract_skills_from_jd(job_description: str) -> List[str]:
    """Extracts potential skills from a job description text."""
    jd_lower = job_description.lower()
    found_skills = set()
    for skill in COMMON_SKILLS:
        # Avoid partial word matches using word boundaries
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_lower):
            found_skills.add(skill)
    return list(found_skills)

def match_skills(job_description: str, user_skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorizes user skills against a job description.
    Returns a dictionary mapping 'have', 'missing', and 'bonus' to lists of skills.
    
    Parameters:
        job_description (str): Full text of the job description.
        user_skills (List[str]): List of skills the user possesses.
        
    Returns:
        Dict[str, List[str]]: Categorized skills.
    """
    jd_skills = set(extract_skills_from_jd(job_description))
    user_skills_set = set(skill.lower() for skill in user_skills)

    have = list(jd_skills.intersection(user_skills_set))
    missing = list(jd_skills.difference(user_skills_set))
    bonus = list(user_skills_set.difference(jd_skills))

    return {
        "have": sorted(have),
        "missing": sorted(missing),
        "bonus": sorted(bonus)
    }
