# Rules File Writeup

## Part 3: Before/After Comparison

### Feature Tested
Issue #4 Develop Keyword Skill Extraction Engine

**Code Quality:**
### With Rules:
The with-rules code combines everything into one function, which is slightly harder to read. But it has a much larger skill list (60+ skills, organized into categories like Languages, Databases, Frameworks, DevOps). It also has better input validation at the top (if not job_description) and a smarter regex pattern that correctly handles special skills like C++ and Node.js without accidentally matching partial words. The skill list is also typed explicitly as Set[str] which is more precise.

### Code snippet
```
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
    "express", "spring boot", "laravel", "rails", "tailwind", "bootstrap", "sass", 
    "redux", "zustand", "pytorch", "tensorflow", "pandas", "numpy",
    
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
```

### Without Rules:
The without rule code has cleaner, simpler code. It splits the logic into two separate functions: one to find skills in the job description, and another to compare them against the user's skills. This makes the code easier to read and test. However, the skill list is smaller (about 35 skills) and the regex is basic, using simple word boundaries (\b). There is also no input validation, meaning if someone passes in an empty string it could cause issues.

### Code snippet
```
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
```
Overall: Without rules wrote cleaner structured code but with fewer skills. With rules wrote more complete and robust code but packed everything into one function. Neither version generated tests, which the rules file required. The biggest difference is not in the backend code, it is in the UI, where with rules produced a professional dashboard matching the wireframe, while without rules produced a plain basic form.

**Design Intent:**
### Without Rule UI
<img width="1135" height="725" alt="without_rule_screenshot_v1" src="https://github.com/user-attachments/assets/7eabd305-9c9d-4296-b98c-711857e863b9" />
- Plain white form with no design system
- No navbar, no layout structure
- Single centered column — nothing like the wireframe
- Skills entered as plain comma-separated text
- No ring score, no three-column view
- Looks like a basic HTML form

### With Rule UI
<img width="1786" height="947" alt="with_rule_screenshot" src="https://github.com/user-attachments/assets/95a406fb-fe97-48ad-93a5-043ca02b46b1" />
- Looks like the wireframe
- Dark mode dashboard matching the PRD wireframe
- Navbar with logo, Dashboard, Settings, user avatar
- Two-column layout as specified in the rules file
- Skills displayed as interactive chips with ✕ buttons
- Animated ring score area (Existing / Missing / Bonus)
- Learning Roadmap section with numbered steps

**Naming & Architecture:**
With rules produced better naming. For example, CURATED_SKILLS is more descriptive than COMMON_SKILLS, variables are more clearly named, and the skill list is organized into readable categories. Without rules naming was more generic.

**Tests Generated:**
### Without Rules
- No tests generated at all 

### With Rules
- No tests generated either 
- The rules file required TDD with 80% pytest coverage
  but the AI did not follow this in either session

This is a gap to fix in Sprint 2

---

## Part 4: Reflection

### How the Rules File Bridges PRD to Implementation
Without a rules file, the AI only knows what you tell it in the chat. 
It has no idea what your project looks like, what design you want, or 
what coding standards you follow. So it just builds something generic 
that works but does not fit your project at all.

The rules file fixes this by giving the AI the full picture before it 
writes any code. It tells the AI to use Tailwind, follow the wireframe 
layout, put files in the right folders, and use strict TypeScript. 
This is why the with-rules version looked like our actual app, while 
the without-rules version looked like a random form someone built in 
10 minutes.

The biggest example from our comparison is the UI. Our rules file 
referenced the wireframe we provide, so the AI built a dark mode 
dashboard with a navbar, two-column layout, skill chips, and a ring 
score. Without the rules file, the AI had no idea what our design 
looked like and just built a plain white form with a text box.

### How GitHub Scrum Helps AI-Assisted Development
The GitHub Issues and Project board help in two ways.

First, they give the AI a clear scope. When we tell the AI to work
which issue, it knows exactly what to build and what not to touch. Our 
rules file says do not modify code outside your current task, and the 
issue number makes that boundary clear. Without issues, the AI might 
try to build everything at once and make a mess.

Second, the issues keep the team organized. Since we are two people 
working on the same codebase, having Sprint 1 and Sprint 2 milestones 
means we both know what is being worked on and what comes next. When 
the AI suggests a branch name like feature/4-skill-extraction-engine, 
it connects directly back to the issue, so anyone looking at the repo 
can understand what that branch is for.

### What Worked and What We Changed:

The rules file worked well for UI and architecture. 
What did not work was test enforcement, the AI ignored 
it in both sessions. We updated the rules file by adding 
stricter test instructions.

What we want to add in rules file:
```
- **Test File Required**: Every new function or module must have a 
  corresponding test file. Do not consider any task complete without 
  a test file. For example, if you create `engine.py`, you must also 
  create `test_engine.py`.
- **Write Tests First**: Before writing any implementation code, write 
  the test first. This is not optional.
- **Test File Location**: All test files go in the `server/tests/` 
  folder and must be named `test_<module_name>.py`.
```

### What We Would Change for Sprint 2
1. We will enforce tests. Both versions skipped tests even though the 
rules file required TDD. For Sprint 2 we will add a stronger instruction 
like "always generate pytest test file alongside every new function" so 
the AI cannot skip it.

2. We will add the Claude API response format. The rules file mentions 
the Claude API but does not describe what the response should look like. 
We will add the expected JSON format for the learning roadmap before 
Sprint 2 starts so the AI knows exactly what to build.

### Key Takeaway
The biggest thing we learned is that a rules file is not a one-time 
setup. Before this assignment, we thought you just write the rules 
once and the AI follows them. But the comparison showed that even with 
a detailed rules file, the AI still missed things, like writing tests.

This taught us that context engineering is an ongoing process. You 
write the rules, test them, find the gaps, and improve them. The rules 
file is basically a contract between your team and the AI. The more 
specific and strict the contract is, the better the AI performs.

For our project, the rules file made the biggest difference in UI and 
architecture. But it failed on test enforcement because the instruction 
was too vague. Now we know, if you want the AI to do something, you 
have to be very explicit about it. Saying "follow TDD" is not enough. 
You have to say "always create a test file, write tests before code, 
and do not consider the task done without tests."
 
