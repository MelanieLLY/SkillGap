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
- **Deployed frontend app URL** (Netlify): `https://skillgapweb.netlify.app`

### Frontend (Vite) API base URL

The frontend reads the backend base URL from `VITE_API_BASE_URL` and automatically appends `/api`:

- **Env variable**: `VITE_API_BASE_URL`
  - **Local dev example**: `VITE_API_BASE_URL=http://127.0.0.1:8000`
  - **Production example (Render)**: `VITE_API_BASE_URL=https://skillgap-api-hrsc.onrender.com`

When deploying the frontend (e.g. to Vercel), configure `VITE_API_BASE_URL` in the project settings using the deployed backend URL above.

## 🧪 Sample test accounts

For reviewers who want to quickly explore the app without creating their own accounts, two sample users are provisioned:

- `alice@example.com`
- `bob@example.com`

The **passwords are not stored in this repository**. They are managed in a 1Password shared item for security and can be retrieved via the shared link provided separately (link valid until **2026-04-10**; after that date, please contact the author for a refreshed link at `liuyyang07@gmail.com`):

- 1Password shared item: `https://share.1password.com/s#8DvZd2OfKOUsNgBEWJWydtwPS6u8fWgIQRJdEK1DYhA`

### Auto-Deploy (deployment platforms)

Both the frontend and backend are configured to deploy automatically when the repo is updated:

- **Render (backend):** Auto-Deploy is enabled with trigger **On Commit**. By default, Render deploys the service whenever you push code or change its configuration. You can disable this in the Render dashboard to deploy manually. [Learn more](https://render.com/docs/configure-repo-sync).
- **Netlify (frontend):** Builds and deploys are triggered on push to the connected branch (e.g. `main`). Same idea: code or config updates trigger a new deploy unless you turn off automatic deploys in the Netlify site settings.