# SkillGap

# System Architecture
<img width="636" height="512" alt="Screenshot 2026-03-12 at 2 00 02 PM" src="https://github.com/user-attachments/assets/d3def8ab-c815-4c69-aa8d-dd8b4037d7ce" />

## Request flow when user submits a job description
<img width="522" height="300" alt="Screenshot 2026-03-12 at 2 00 43 PM" src="https://github.com/user-attachments/assets/b5f22eee-229e-4164-9734-40b3c3a0bd4f" />

The user pastes a job description, our server compares it against their saved skill profile, calculates a match score, and asks Claude AI to generate a learning plan for the gap

# Getting Started

This document provides step-by-step instructions for setting up and running the Tech Stack Skill Gap Analyzer application locally on macOS.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- **Python 3.11+**: for the backend FastAPI server
- **Node.js (18+ recommended)**: for the frontend React/Vite development server
- **PostgreSQL**: for the database. (Alternatively, Docker can be used to run a local PostgreSQL instance).

## 1. Clone the Repository

Clone the project repository to your local machine:
```bash
git clone https://github.com/MelanieLLY/SkillGap
cd SkillGap
```

## 2. Environment Variables

Both the backend and frontend rely on environment variables.

1. **Create the `.env` file** in the root of the project:

```bash
touch .env
```

2. **Populate the `.env` file**. You will need database connection strings, JWT secrets, and API keys. The `.env` file should look something like this:

```ini
# Backend Database Configuration (Replace with your distinct credentials if needed)
DATABASE_URL=postgresql://user:password@localhost:5432/skillgapdb

# Authentication
SECRET_KEY=your_super_secret_jwt_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
CLAUDE_API_KEY=your_anthropic_claude_api_key
```

*Note: Never commit your `.env` file. It should be ignored by Git.*

## 3. Installation

The application is structured as a monorepo containing both `client/` and `server/` directories. A root `package.json` script handles installing everything at once.

1. Create and activate a Python virtual environment at the root level:
```bash
python -m venv venv
source venv/bin/activate
```

2. Run the root install script:
```bash
# This installs root dependencies, frontend Node modules, and backend Python packages requirements.txt
npm run install:all
```

*If you prefer manual installation:*
- **Backend:** `cd server && pip install -r requirements.txt`
- **Frontend:** `cd client && npm install`

## 4. Database Setup

`npm run dev` **does not** spin up a database server for you. You must ensure PostgreSQL is running locally.

1. Install and start PostgreSQL on your Mac (e.g., via Homebrew or Postgres.app).
2. Create the database specified in your `.env` file (e.g., `skillgapdb`).
3. The FastAPI server uses SQLAlchemy, which connects to the existing database using the `DATABASE_URL` environment variable.

## 5. Run the Application

The root `package.json` includes a script that runs both the frontend and backend development servers **concurrently**.

Ensure your Python virtual environment is activated before running:
```bash
source venv/bin/activate
npm run dev
```

This will start:
- **Backend (FastAPI)**: Running locally on `http://localhost:8000`
- **Frontend (React)**: Running locally on `http://localhost:5173` (or depending on your Vite config).

You can access the backend auto-generated API documentation at `http://localhost:8000/docs`.

## 6. Testing (Pytest)

`npm run dev` **does not** run the testing suite. Backend tests must be run separately manually.

To run the backend test suite (built with `pytest`):

```bash
cd server
pytest
```

## 7. Deployment

`npm run dev` is strictly for creating a **local development environment**. It does not build or deploy the application to a live server.

For a production deployment:
- **Frontend**: Run `npm run build` inside the `client/` directory to generate optimized static files (usually deployed to Vercel, Netlify, or an S3 bucket).
- **Backend**: The FastAPI server would be packaged, likely into a Docker container, and deployed to a cloud provider (e.g., AWS ECS, Render, Heroku).
- The project documentation mentions that moving forward, CI/CD will be handled via **GitHub Actions**.

## 🌐 Environment configuration

- **Local development backend**: `http://127.0.0.1:8000` (started by `npm run dev`)
- **Deployed backend API base URL** (Render): `https://skillgap-api-hrsc.onrender.com`
- **Deployed frontend app URL** (Netlify): 

### Frontend (Vite) API base URL

The frontend reads the backend base URL from `VITE_API_BASE_URL` and automatically appends `/api`:

- **Env variable**: `VITE_API_BASE_URL`
  - **Local dev example**: `VITE_API_BASE_URL=http://127.0.0.1:8000`
  - **Production example (Render)**: `VITE_API_BASE_URL=https://skillgap-api-hrsc.onrender.com`

When deploying the frontend (e.g. to Vercel), configure `VITE_API_BASE_URL` in the project settings using the deployed backend URL above.
