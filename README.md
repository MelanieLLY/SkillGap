# SkillGap — Tech Stack Skill Gap Analyzer

A web app that helps job seekers identify skill gaps from job descriptions.
Paste a JD, see your match score, and get an AI-generated learning roadmap.

**Team 7:** Jing Ng · Liuyi 

## Tech Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Zustand
- **Backend:** FastAPI, Python 3.11, SQLAlchemy, PostgreSQL
- **AI:** Claude API (claude-sonnet-4-20250514)

## Screenshots

### Login page
<img width="600" alt="Login page" src="https://github.com/user-attachments/assets/e87a84cc-509c-4268-af6e-f27dbcf52289" />

### Sign up page
<img width="600" alt="Sign up page" src="https://github.com/user-attachments/assets/80c94f72-4cc7-4d7c-a633-ef2272248f9c" />

### Main Dashboard
<img width="1000" alt="Screenshot 2026-03-12 at 2 34 27 PM" src="https://github.com/user-attachments/assets/feed4cb7-fe63-4ec8-826e-c52d9be6dc3e" />

### Profile Setup Page
<img width="1000" alt="Screenshot 2026-03-12 at 2 44 13 PM" src="https://github.com/user-attachments/assets/3a92c5ea-fade-4b8b-9baa-9a702f9cbda9" />

### Skill Match Analysis
<img width="1000" height="1123" alt="Screenshot 2026-03-12 at 2 45 52 PM" src="https://github.com/user-attachments/assets/e433e3e5-441d-4729-9898-be4fd5e98ff0" />


## System Architecture

<img width="600" alt="System architecture" src="https://github.com/user-attachments/assets/d3def8ab-c815-4c69-aa8d-dd8b4037d7ce" />

### Request flow when user submits a job description

<img width="500" alt="Request flow" src="https://github.com/user-attachments/assets/b5f22eee-229e-4164-9734-40b3c3a0bd4f" />

The user pastes a job description, our server compares it against their saved skill profile, calculates a match score, and asks Claude AI to generate a learning plan for the gap.

## Project Structure
```
SkillGap/
├── client/           # React frontend (Vite, Tailwind, Zustand)
├── server/           # FastAPI backend
│   ├── tests/        # pytest test suite
│   ├── core/         # DB config & settings
│   ├── auth/         # Auth module
│   └── ...           # other logic modules (extraction, roadmap, etc.)
├── .env              # Environment variables (not committed)
└── package.json      # Root scripts (dev, install:all)
```

## Live URLs

| | URL |
|---|---|
| Frontend (Netlify) | coming soon |
| Backend API (Render) | https://skillgap-api-hrsc.onrender.com |
| API Docs | https://skillgap-api-hrsc.onrender.com/docs |

---

# Getting Started

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL**

## 1. Clone the Repository
```bash
git clone https://github.com/MelanieLLY/SkillGap
cd SkillGap
```

## 2. Environment Variables

Create the `.env` file in the root of the project:
```bash
touch .env
```

Populate it with the following:
```ini
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/skillgapdb

# Authentication
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
CLAUDE_API_KEY=your_anthropic_claude_api_key

# Frontend
VITE_API_BASE_URL=http://127.0.0.1:8000
```

> Never commit your `.env` file. It should be listed in `.gitignore`.

## 3. Installation

Create and activate a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install all dependencies:
```bash
npm run install:all
```

<details>
<summary>Manual installation (optional)</summary>
```bash
cd server && pip install -r requirements.txt
cd client && npm install
```
</details>

## 4. Database Setup

`npm run dev` does not spin up a database for you. Ensure PostgreSQL is running first.
```bash
createdb skillgapdb
```

## 5. Run the Application
```bash
source venv/bin/activate
npm run dev
```

| Server | URL |
|---|---|
| Frontend (React) | http://localhost:5173 |
| Backend (FastAPI) | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

## 6. Run Tests
```bash
cd server
pytest
```

## 7. Deployment

For production, set `VITE_API_BASE_URL` to the deployed backend URL in your frontend host's environment settings (e.g. Netlify).

- **Frontend:** `npm run build` inside `client/` → deploy to Netlify or Vercel
- **Backend:** Docker container → deploy to Render or AWS
- **CI/CD:** GitHub Actions
