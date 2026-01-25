# Frontend

React + TypeScript dashboard.

## Files

```
frontend/
├── src/
│   ├── main.tsx          # Entry point, renders App with providers
│   ├── App.tsx           # Router setup, protected routes
│   ├── auth.tsx          # AuthContext - token state, login/logout
│   ├── api.ts            # API client with auth headers
│   ├── pages/
│   │   ├── Login.tsx     # GitHub OAuth login button
│   │   └── Debtors.tsx   # Dashboard page with chart
│   └── components/
│       └── Chart.tsx     # Recharts bar chart
│   ├── index.css         # Global styles
│   └── App.css           # Component styles
│
├── index.html            # HTML template
├── vite.config.ts        # Vite bundler config (dev server, proxy)
├── package.json          # Dependencies + scripts
├── package-lock.json     # Locked dependency versions (auto-generated)
├── tsconfig.json         # TypeScript config (references other tsconfigs)
├── tsconfig.app.json     # TS config for app code
├── tsconfig.node.json    # TS config for vite.config.ts
└── eslint.config.js      # Linting rules
```

## Run

```bash
nvm use 20
npm run dev
```

## Build

```bash
npm run build  # outputs to dist/
```
