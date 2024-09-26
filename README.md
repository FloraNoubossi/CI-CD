# CI-CD

# CI/CD FastAPI Project

Ce projet met en œuvre une application **FastAPI** simple avec une intégration continue et un déploiement continu (CI/CD) à l'aide de **GitHub Actions**. Il inclut également la création d'une image Docker pour l'application et des tests automatisés.

## Table des matières

1. [Installation](#installation)
2. [Structure du Projet](#structure-du-projet)
3. [Exécution de l'application](#exécution-de-lapplication)
4. [Workflows GitHub Actions](#workflows-github-actions)
   - [Test Workflow](#test-workflow)
   - [Build Docker Workflow](#build-docker-workflow)
5. [Utilisation de `act` pour tester localement les workflows GitHub Actions](#utilisation-de-act-pour-tester-localement-les-workflows-github-actions)
6. [Contact](#contact)

---

## Installation

### 1. Cloner le projet

Clonez ce dépôt sur votre machine locale :

```bash
git clone https://github.com/FloraNoubossi/CI-CD.git
cd CI-CD
```

### 2. Créer un environnement virtuel et installer les dépendances

Créez un environnement virtuel Python et installez les dépendances avec `pip` :

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Installer Docker

Si Docker n'est pas déjà installé sur votre machine, vous pouvez suivre les instructions [ici](https://docs.docker.com/get-docker/).

---

## Structure du Projet

Le projet suit la structure suivante :

```
.
├── .github/
│   └── workflows/
│       ├── docker-build.yml        # Workflow GitHub Actions pour construire une image Docker
│       ├── run.yml                 # Workflow GitHub Actions pour exécuter l'application FastAPI
│       └── test.yml                # Workflow GitHub Actions pour exécuter les tests
├── .gitignore                      # Fichiers et dossiers à ignorer par Git
├── README.md                       # Ce fichier README
├── main.py                         # Application FastAPI principale
├── test_main.py                    # Fichier de test pour l'application
├── requirements.txt                # Fichier des dépendances Python
└── start.sh                        # Script pour démarrer l'application localement
```

---

## Exécution de l'application

### Localement

Pour exécuter l'application FastAPI localement, utilisez la commande suivante :

```bash
uvicorn main:app --reload --port=8001
```

L'API sera accessible à l'adresse suivante : [http://127.0.0.1:8001](http://127.0.0.1:8001).

### Exécution avec Docker

#### 1. Construire l'image Docker

Utilisez Docker pour créer une image de l'application :

```bash
docker build -t fastapi-app .
```

#### 2. Exécuter l'image Docker

Exécutez l'application à l'intérieur d'un conteneur Docker avec la commande suivante :

```bash
docker run -p 8001:8001 fastapi-app
```

---

## Workflows GitHub Actions

Nous avons configuré plusieurs workflows pour automatiser les tests et la création d'images Docker.

### Test Workflow

Ce workflow exécute les tests à chaque fois qu'un code est poussé vers la branche `main` ou lorsqu'une Pull Request est ouverte.

#### Contenu du fichier `.github/workflows/test.yml` :

```yaml
name: FastAPI test

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  fastapi-run-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests with pytest
        run: |
          python -m pytest
```

### Build Docker Workflow

Ce workflow crée et pousse une image Docker sur Docker Hub à chaque fois que du code est poussé ou qu'une Pull Request est ouverte sur la branche `main`.

#### Contenu du fichier `.github/workflows/docker-build.yml` :

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t yourdockerhubusername/yourapp:latest .
          docker push yourdockerhubusername/yourapp:latest
```

---

## Utilisation de `act` pour tester localement les workflows GitHub Actions

Nous avons utilisé **`act`** pour tester les workflows GitHub Actions en local sans avoir à pousser les modifications sur GitHub.

### Installation de `act`

#### 1. Installer Homebrew (si ce n'est pas déjà fait) :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. Installer `act` via Homebrew :

```bash
brew install act
```

### Exécuter les workflows localement

#### 1. Lister les workflows disponibles :

```bash
act -l
```

#### 2. Exécuter un workflow spécifique :

Par exemple, pour exécuter le workflow de test :

```bash
act -j fastapi-run-test
```

---

