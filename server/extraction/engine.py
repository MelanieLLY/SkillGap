import re
from typing import List, Dict, Set

# A predefined curated list of tech skills (simplified mapping for the MVP)
# In production, this would be loaded from a database or a more exhaustive config.
CURATED_SKILLS: Set[str] = {
    # Languages & Core
    "python", "javascript", "typescript", "java", "c++", "cpp", "c#", "golang", "go", 
    "rust", "ruby", "php", "swift", "kotlin", "scala", "sql", "html", "css", "node.js", "nodejs",
    
    # Databases & Storage
    "postgresql", "mysql", "mongodb", "redis", "sqlite", "oracle", "mariadb", 
    "elasticsearch", "dynamodb", "cassandra", "firebase", "supabase", "sql server",
    
    # Frameworks & Libraries
    "react", "vue", "angular", "next.js", "nuxt", "svelte", "fastapi", "flask", "django", 
    "express", "spring boot", "spring", "laravel", "rails", "tailwind", "bootstrap", "sass", 
    "redux", "zustand", "pytorch", "tensorflow", "pandas", "numpy", "scikit-learn", "langchain",
    "uiautomator",
    
    # DevOps & Infrastructure
    "docker", "kubernetes", "aws", "azure", "gcp", "google cloud", "terraform", "ansible", 
    "jenkins", "github actions", "ci/cd", "nginx", "linux", "ubuntu",
    
    # Tools & Concepts
    "git", "github", "gitlab", "jira", "figma", "postman", "rest api", "graphql", "grpc", 
    "microservices", "unit testing", "agile", "scrum", "webpack", "vite", "npm", "yarn"
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

    # Normalize inputs for matching
    jd_text = job_description.lower()
    user_skills_normalized = {skill.lower().strip() for skill in user_skills if skill}
    
    # Check both curated skills and user-provided skills
    all_potential_skills = CURATED_SKILLS.union(user_skills_normalized)
    
    jd_skills: Set[str] = set()
    for skill in all_potential_skills:
        # Standardize skill for regex
        escaped_skill = re.escape(skill)
        # Boundary logic: Match skill if it's not preceded or followed by alphanumeric chars, +, or #
        # This allows matching "C++" or ".NET" while avoiding matching "java" in "javascript"
        pattern = rf"(?<![a-zA-Z0-9+#]){escaped_skill}(?![a-zA-Z0-9+#])"
        if re.search(pattern, jd_text):
            jd_skills.add(skill)
            
    # Categorize skills
    have = sorted(list(jd_skills.intersection(user_skills_normalized)))
    missing = sorted(list(jd_skills.difference(user_skills_normalized)))
    bonus = sorted(list(user_skills_normalized.difference(jd_skills)))
    
    return {
        "have": have,
        "missing": missing,
        "bonus": bonus
    }
