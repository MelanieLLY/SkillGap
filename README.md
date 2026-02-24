# SkillGap

SkillGap is an AI-powered tool designed to help job seekers identify the gap between their current skills and the requirements of a specific job description. It automatically extracts key skills from a JD and categorizes them into "Have", "Missing", and "Bonus" skills.

## 🚀 Features

- **Skill Extraction**: Automatically parses job descriptions to find relevant technical skills.
- **Gap Analysis**: Compares your skills against JD requirements.
- **Visual Feedback**: Clean, badge-based UI for easy reading of skill categories.
- **FastAPI Backend**: High-performance Python backend for skill matching logic.
- **React Frontend**: Responsive and interactive user interface.

## 🛠 Tech Stack

- **Frontend**: React (Vite), TypeScript, Vanilla CSS
- **Backend**: Python, FastAPI, Uvicorn
- **Logic**: Regular Expression based skill extraction (extensible to NLP)

## 📦 Getting Started

### Prerequisites

- Node.js (v18+)
- Python (v3.9+)

### Installation & Running

#### 1. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if requirements.txt exists, else install manually)
pip install fastapi uvicorn pydantic

# Start the backend server
uvicorn main:app --reload --port 8000
```
The backend will be running at `http://localhost:8000`.

#### 2. Frontend Setup
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
The frontend will be running at `http://localhost:5173` (or similar, check terminal output).

## 💡 Usage

1. Open the application in your browser.
2. Paste a **Job Description** into the textarea.
3. Type your **Skills** (separated by commas) in the input field.
4. Click **"Match Skills"** to see the analysis.

## 📁 Project Structure

```
SkillGap/
├── backend/
│   ├── main.py              # FastAPI entry point
│   └── services/
│       └── skill_extractor.py # Skill matching logic
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main application logic
│   │   └── components/
│   │       └── SkillMatchResult.tsx # Display component
└── README.md
```