 RCW-E25 — Gestion de Transactions 

 Lancer en local

1) Backend (Docker)
```bash
docker compose down -v
docker compose up --build

//pour admin : admin@rcw.local / admin123

 2)Frontend 
cd web
npm install
npm run dev
 // avoir en place le fichier .env 
 VITE_API_URL=http://localhost:8010
