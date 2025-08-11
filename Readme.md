RCW-E25 — API de Gestion de Transactions
Plateforme de gestion et de suivi des transactions financières multi-services (RIA, Western Union, MoneyGram).
Le projet inclut un backend API en FastAPI, un frontend React, et un environnement Docker avec PostgreSQL.

Technologies utilisées
Backend : FastAPI (Python)

Frontend : React (Vite + Tailwind CSS)

Base de données : PostgreSQL

Conteneurisation : Docker & Docker Compose

Authentification : JWT

Autres : ESLint, Git

Installation et exécution
Cloner le dépôt :


git clone https://github.com/Mohandsaid01/RCW-E25---API-de-Gestion-de-Transactions.git
cd RCW-E25---API-de-Gestion-de-Transactions

Créer un fichier .env dans backend/ à partir de .env.example et y mettre les valeurs nécessaires.

Lancer le projet avec Docker :


docker compose up --build
Accéder :

Backend API : http://localhost:8010/docs

Frontend : http://localhost:5173

Fonctionnalités principales
Gestion des clients (création, liste, recherche)

Gestion des taux de change

Enregistrement de transactions multi-devises

Génération de rapports par service, devise et pays

Authentification et rôles (admin, utilisateur)

Déploiement facile via Docker RCW-E25 — Gestion de Transactions 

 Lancer en local

1) Backend (Docker)

docker compose down -v
docker compose up --build

//pour admin : admin@rcw.local / admin123

 2)Frontend 
cd web
npm install
npm run dev

 // avoir en place le fichier .env 
 VITE_API_URL=http://localhost:8010
