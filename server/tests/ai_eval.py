import asyncio
import json
import os
import sys
from typing import Any, Dict, List, cast

# Ensure server modules are discoverable when running this file directly.
SERVER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(SERVER_DIR)

from anthropic import AsyncAnthropic  # noqa: E402
from core.config import settings  # noqa: E402
from extraction.engine import extract_skills  # noqa: E402
from roadmap.services import generate_roadmap_with_claude  # noqa: E402

# ── Configuration & Paths ────────────────────────────────────────────────────
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
ROADMAPS_DIR = os.path.join(DOCS_DIR, "eval_roadmaps")
RESULTS_FILE = os.path.join(DOCS_DIR, "ai_eval_results.md")

# Model from project rules
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# ── Sample Job Descriptions ──────────────────────────────────────────────────
SAMPLES = [
    {
        "id": "backend_sr",
        "role": "Senior Backend Engineer",
        "jd": "Role: Senior Backend Engineer\nCompany: TechLogix\nWe are looking for a Python expert to lead our backend team. Must have deep experience with FastAPI, PostgreSQL, and Redis. Experience with Docker and Kubernetes is a plus.",
        "user_skills": ["Python", "SQL"],
    },
    {
        "id": "frontend_dev",
        "role": "Frontend Developer",
        "jd": "Position: Frontend Developer\nCompany: WebFlow Solutions\nJoin us building reactive UIs with React 18, TypeScript, and Tailwind CSS. We use Zustand for state management and Framer Motion for animations.",
        "user_skills": ["HTML", "CSS", "JavaScript"],
    },
    {
        "id": "fullstack_eng",
        "role": "Full Stack Engineer",
        "jd": "Title: Full Stack Engineer\nCompany: StartupGo\nWe need a developer comfortable with Node.js/Express but also React on the frontend. Data is stored in MongoDB. You should know how to deploy on AWS.",
        "user_skills": ["JavaScript", "Node.js", "Express"],
    },
    {
        "id": "data_scientist",
        "role": "Data Scientist",
        "jd": "Job: Data Scientist\nCompany: InsighData\nLooking for someone to build ML models using Python, Pandas, and scikit-learn. Experience with PyTorch or TensorFlow for deep learning is highly desired. Knowledge of SQL and Docker is required.",
        "user_skills": ["Python", "SQL", "Pandas"],
    },
    {
        "id": "devops_eng",
        "role": "Devops Engineer",
        "jd": "Position: DevOps Engineer\nCompany: CloudCore\nMandatory skills: AWS, Kubernetes, and Terraform. You should also be proficient with Github Actions and Docker. Ansible or Jenkins experience is a plus.",
        "user_skills": ["Linux", "Git", "Docker"],
    },
]

# ── Balanced Judge Prompt ───────────────────────────────────────────────────
JUDGE_PROMPT = """
You are a senior technical educator. Evaluate the following learning roadmap generated for a specific Job Description (JD). 
The goal is to provide a FAIR but RIGOROUS assessment. Avoid giving empty 5/5 scores unless the content is truly exceptional.

JOB DESCRIPTION:
{jd}

GENERATED ROADMAP JSON:
{roadmap}

SCORE THE ROADMAP (1-5) based on:

1. **Relevance (1-5)**: Does the roadmap precisely target the missing skills? 
   - 5: Perfect alignment.
   - 3: Good, but includes generic "fluff" (like generic Soft Skills not in the JD).
   - 1: Misses the core technical requirements.

2. **Specificity & Depth (1-5)**: 
   - 5: Uses tool-specific terminology (e.g., "Zustand Middleware" for state management, "React Context" instead of just "React").
   - 3: Uses correct technology names but stays at the surface level.
   - 1: Extremely vague or generic milestones.

3. **Feasibility (1-5)**: Is the learning journey logical and the pace realistic?
   - 5: Realistic timeline for a dedicated learner.
   - 3: Slightly too fast or slow, but workable.
   - 1: Claims to teach complex devops/backend mastery in impossible timeframes (e.g., 2 weeks for Kubernetes).

RETURN THE RESULT IN JSON FORMAT ONLY:
{{
  "relevance": <int>,
  "specificity": <int>,
  "completeness": <int>,
  "justification": "<CONCISE_CONSTRUCTIVE_FEEDBACK>"
}}
"""


async def judge_roadmap(
    client: AsyncAnthropic, jd: str, roadmap: str
) -> Dict[str, Any]:
    """Uses Sonnet as a balanced Judge to score the roadmap."""
    prompt = JUDGE_PROMPT.format(jd=jd, roadmap=roadmap)

    response = await client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw_text = response.content[0].text
    try:
        # Robust JSON extraction
        start_idx = raw_text.find("{")
        end_idx = raw_text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            raw_text = raw_text[start_idx : end_idx + 1]
        return cast(Dict[str, Any], json.loads(raw_text))
    except Exception as e:
        return {
            "relevance": 0,
            "specificity": 0,
            "completeness": 0,
            "justification": f"Critique Parse Error: {e}",
        }


async def run_eval():
    print("🚀 Starting Professional AI vs AI Evaluation...")

    if not settings.anthropic_api_key:
        print("❌ Error: ANTHROPIC_API_KEY is not set.")
        return

    os.makedirs(ROADMAPS_DIR, exist_ok=True)
    client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    results: List[Dict[str, Any]] = []

    for sample in SAMPLES:
        print(f"Evaluating: {sample['role']}...")

        # 1. Extract missing skills
        extracted = extract_skills(sample["jd"], sample["user_skills"])
        missing = extracted["missing"]

        if not missing:
            print("  - Skipping (no missing skills)")
            continue

        # 2. Generate roadmap
        try:
            roadmap_response = await generate_roadmap_with_claude(missing, sample["jd"])
            roadmap_json_str = roadmap_response.model_dump_json(indent=2)

            # Save raw JSON
            filename = f"roadmap_{sample['id']}.json"
            filepath = os.path.join(ROADMAPS_DIR, filename)
            with open(filepath, "w") as f:
                f.write(roadmap_json_str)

            # 3. Judge roadmap
            score = await judge_roadmap(client, sample["jd"], roadmap_json_str)

            results.append(
                {
                    "id": sample["id"],
                    "role": sample["role"],
                    "missing": missing,
                    "scores": score,
                    "json_file": filename,
                }
            )
            avg_score = (
                score.get("relevance", 0)
                + score.get("specificity", 0)
                + score.get("completeness", 0)
            ) / 3
            print(f"  - Done. (Avg Score: {round(avg_score, 1)})")

        except Exception as e:
            print(f"  - ❌ Failed: {e}")
            results.append(
                {
                    "id": sample["id"],
                    "role": sample["role"],
                    "missing": missing,
                    "error": str(e),
                }
            )

    # 4. Generate Premium Markdown Report
    md = [
        "# 🤖 SkillGap AI Mastery Assessment Dashboard",
        "",
        "## 📝 Overview",
        f"This report provides an automated analysis of the **{CLAUDE_MODEL}** roadmap generation engine. We used the same model as an independent technical judge to evaluate the quality of {len(results)} distinct roadmap scenarios based on real-world Job Descriptions.",
        "",
        "### 📏 Evaluation Criteria",
        "- **Technical Precision**: Alignment with industry standards and advanced terminology.",
        "- **Project Challenge**: Quality and complexity of recommended practical projects.",
        "- **Feasibility & Pacing**: Realism of the timeline for mastering complex technical domains.",
        "",
        "---",
        "",
        "## 📊 Executive Summary",
    ]

    valid_results = [r for r in results if "error" not in r]
    count = len(valid_results)
    if count > 0:
        total_r = sum(float(r["scores"].get("relevance", 0)) for r in valid_results)
        total_s = sum(float(r["scores"].get("specificity", 0)) for r in valid_results)
        total_c = sum(float(r["scores"].get("completeness", 0)) for r in valid_results)

        avg_r = total_r / count
        avg_s = total_s / count
        avg_c = total_c / count
        total_avg = (avg_r + avg_s + avg_c) / 3

        md.append(f"- **Overall AI Mastery Score**: `{round(total_avg, 2)} / 5.0`")
        md.append(
            f"- **Relevance**: `{round(avg_r, 2)}/5` | **Specificity**: `{round(avg_s, 2)}/5` | **Completeness**: `{round(avg_c, 2)}/5` "
        )
        md.append("")

        md.append("### 🏆 Result Matrix")
        md.append("| Role Profile | Missing Targets | Rel | Spec | Comp | Artifact |")
        md.append("|:---|:---|:---:|:---:|:---:|:---|")
        for r in results:
            if "error" in r:
                md.append(
                    f"| {r['role']} | {', '.join(r['missing'])} | ❌ | ❌ | ❌ | Error |"
                )
            else:
                s = r["scores"]
                md.append(
                    f"| {r['role']} | {', '.join(r['missing'])} | {s.get('relevance', 0)} | {s.get('specificity', 0)} | {s.get('completeness', 0)} | [JSON](./eval_roadmaps/{r['json_file']}) |"
                )

    md.append("")
    md.append("---")
    md.append("")
    md.append("## 🔍 Detailed Feedback per Scenario")
    md.append("")

    for r in results:
        md.append(f"### 📍 {r['role']}")
        if "error" in r:
            md.append(f"> ❌ **Assessment Failed**: {r['error']}")
        else:
            s = r["scores"]
            md.append(f"- **Skills Evaluated**: `{', '.join(r['missing'])}`")
            md.append(f"- **Justification**: {s.get('justification', 'N/A')}")
            md.append("")
            md.append("#### ⚖️ Criterion Breakdown")
            md.append("| Criterion | Score | Definition |")
            md.append("|:---|:---:|:---|")
            md.append(
                f"| **Technical Precision** | {s.get('relevance', 0)}/5 | Focus on JD requirements |"
            )
            md.append(
                f"| **Project Challenge** | {s.get('specificity', 0)}/5 | Technical depth and terminology |"
            )
            md.append(
                f"| **Feasibility & Pacing** | {s.get('completeness', 0)}/5 | Logical learning path & project |"
            )
        md.append("")

    md.append("---")
    md.append("*Generated on: 2026-03-11*")

    with open(RESULTS_FILE, "w") as f:
        f.write("\n".join(md))

    print("\n✨ Assessment complete. Dashboard and JSON artifacts updated in 'docs/'")


if __name__ == "__main__":
    asyncio.run(run_eval())
