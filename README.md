# SkillGap

## 🚀 Setup
```bash
# Install repo-level tooling
npm install

# Install frontend dependencies
npm run install:client

# Install backend dependencies
npm run install:server
```

You can also install everything with:

```bash
npm run install:all
```

## 💻 Run
```bash
# Start frontend + backend together from the repo root
npm run dev
```

## 🌐 Deployment Roots
```text
Frontend: client/
Backend: server/
```

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
