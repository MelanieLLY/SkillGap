import re
from typing import List, Dict, Set

# A predefined curated list of tech skills (simplified mapping for the MVP)
# In production, this would be loaded from a database or a more exhaustive config.
CURATED_SKILLS: Set[str] = {
    "python", "javascript", "typescript", "react", "fastapi", "node.js", 
    "nodejs", "sql", "postgresql", "docker", "aws", "kubernetes", "java", 
    "c++", "cpp", "html", "css", "tailwind", "git", "ci/cd", "vue", "angular",
    "go", "rust", "ruby", "django", "flask", "express", "mongodb", "redis"
}

def extract_skills(job_description: str, user_skills: List[str]) -> Dict[str, List[str]]:
    """
    Extracts skills from a job description and compares them against user's skills.
    
    Args:
        job_description (str): The raw text of the job description.
        user_skills (List[str]): A list of skills the user already possesses.
        
    Returns:
        Dict: A dictionary categorizing skills into 'have', 'missing', and 'bonus'.
              Keys are 'have', 'missing', 'bonus', and values are lists of skill strings.
    """
    if not job_description or not isinstance(job_description, str):
        return {"have": [], "missing": [], "bonus": []}

    # Normalize inputs
    jd_text = job_description.lower()
    
    # Clean up user skills to be lowercase and stripped of excess whitespace
    user_skills_normalized: Set[str] = {skill.lower().strip() for skill in user_skills if skill}
    
    # Extract skills present in the JD based on a curated list of keywords
    jd_skills: Set[str] = set()
    for skill in CURATED_SKILLS:
        # Simple word boundary regex to avoid partial matches (e.g. matching 'java' in 'javascript')
        # We handle special characters in skills like 'c++', 'node.js'
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, jd_text):
            jd_skills.add(skill)
            
    # Categorize skills
    # 'have': skills in JD that the user also has
    have = sorted(list(jd_skills.intersection(user_skills_normalized)))
    
    # 'missing': skills in JD that the user does not have
    missing = sorted(list(jd_skills.difference(user_skills_normalized)))
    
    # 'bonus': skills the user has that are not explicitly mentioned in the JD
    bonus = sorted(list(user_skills_normalized.difference(jd_skills)))
    
    return {
        "have": have,
        "missing": missing,
        "bonus": bonus
    }
