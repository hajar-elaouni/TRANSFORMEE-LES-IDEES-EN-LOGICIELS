# 🚀 LLM2CODE - Générateur de Code Intelligent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.30.11-green.svg)](https://crewai.com)
[![Flask](https://img.shields.io/badge/Flask-2.0+-red.svg)](https://flask.palletsprojects.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange.svg)](https://ai.google.dev)

## 📋 Description

**LLM2CODE** est une application web révolutionnaire qui utilise l'intelligence artificielle pour transformer vos descriptions en langage naturel en code fonctionnel. L'application utilise CrewAI avec Google Gemini pour créer un système multi-agents capable d'analyser, planifier, générer, tester et documenter du code dans plusieurs langages de programmation.

### ✨ Fonctionnalités Principales

- 🤖 **Génération de Code Multi-Langages** : Python, Java, C++, JavaScript
- 🔍 **Analyse Intelligente des Exigences** : Compréhension automatique des besoins
- 📊 **Planification Architecturale** : Décomposition en tâches structurées
- ✅ **Tests Automatiques** : Validation et correction du code généré
- 📚 **Documentation Complète** : Génération automatique de documentation PDF
- 🌐 **Interface Web Moderne** : Interface utilisateur intuitive et responsive
- 🔧 **Compilation et Exécution** : Test automatique du code généré

## 🏗️ Architecture du Système

Le projet utilise une architecture multi-agents avec CrewAI :

### Agents Spécialisés

1. **🔍 Agent d'Analyse des Exigences** (`requirement_analysis`)
   - Analyse et valide les besoins utilisateur
   - Transforme le langage naturel en spécifications techniques
   - Identifie les exigences fonctionnelles et non-fonctionnelles

2. **📋 Agent de Planification** (`task_planner_agent`)
   - Décompose les exigences en tâches actionables
   - Planifie l'architecture du projet
   - Identifie les meilleures pratiques par langage

3. **💻 Agent de Génération de Code** (`code_generator_agent`)
   - Génère du code propre et documenté
   - Suit les conventions du langage choisi
   - Crée une architecture modulaire et scalable

4. **🧪 Agent de Validation** (`test_validation_agent`)
   - Valide la qualité du code généré
   - Effectue des tests unitaires
   - Identifie les problèmes de performance

5. **🔧 Agent de Correction** (`code_fix_agent`)
   - Corrige automatiquement les erreurs détectées
   - Améliore la qualité du code
   - Résout les problèmes de compilation

6. **📖 Agent de Documentation** (`documentation_agent`)
   - Génère une documentation complète
   - Crée des fichiers PDF professionnels
   - Explique chaque composant du code

## 🛠️ Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Clé API Google Gemini
- Clé API Serper.dev (pour la recherche web)

### Étapes d'Installation

1. **Cloner le repository**
   ```bash
   git clone https://github.com/hajar-elaouni/TRANSFORMEE-LES-IDEES-EN-LOGICIELS.git
   cd LLM2CODE
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   
   # Sur Windows
   venv\Scripts\activate
   
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r crewgooglegemini/requirements.txt
   ```

4. **Configuration des variables d'environnement**
   
   Créez un fichier `.env` dans le dossier `crewgooglegemini/` :
   ```env
   GOOGLE_API_KEY=votre_cle_api_google_gemini
   SERPER_API_KEY=votre_cle_api_serper
   ```

5. **Configuration des compilateurs** (optionnel)
   
   Pour C++ :
   - Installez MinGW ou Visual Studio
   - Modifiez le chemin dans `app.py` ligne 256
   
   Pour Java :
   - Installez JDK
   - Modifiez le chemin dans `app.py` ligne 430

## 🚀 Utilisation

### Lancement de l'Application

1. **Démarrer le serveur Flask**
   ```bash
   cd crewgooglegemini
   python app.py
   ```

2. **Accéder à l'interface web**
   
   Ouvrez votre navigateur et allez à : `http://127.0.0.1:5000`

### Utilisation de l'Interface

1. **Saisir votre projet**
   - Dans le champ "Décrivez votre projet", décrivez ce que vous voulez créer
   - Dans le champ "Langage de programmation", spécifiez le langage (python, java, cpp, javascript)

2. **Exemples de descriptions**
   ```
   Projet: "Système de gestion de bibliothèque"
   Langage: "python"
   
   Projet: "Calculatrice scientifique avec interface graphique"
   Langage: "java"
   
   Projet: "Jeu de morpion en console"
   Langage: "cpp"
   ```

3. **Suivre le processus**
   - L'application affichera chaque étape en temps réel
   - Vous pourrez voir l'analyse, la planification, le code généré, les tests et la documentation

4. **Télécharger les résultats**
   - Le code généré est sauvegardé dans `generated_projects/`
   - La documentation PDF est téléchargeable via l'interface

### Utilisation en Ligne de Commande

Vous pouvez aussi utiliser le script `crew.py` directement :

```bash
cd crewgooglegemini
python crew.py
```

## 📁 Structure du Projet

```
LLM2CODE/
├── crewgooglegemini/           # Code principal de l'application
│   ├── agents.py              # Définition des agents CrewAI
│   ├── tasks.py               # Définition des tâches
│   ├── tools.py               # Outils (recherche web, génération PDF)
│   ├── app.py                 # Application Flask principale
│   ├── crew.py                # Script de démonstration
│   ├── requirements.txt        # Dépendances Python
│   ├── templates/             # Templates HTML
│   │   ├── index.html         # Interface principale
│   │   └── result.html        # Page de résultats
│   ├── static/                # Fichiers statiques
│   │   ├── style.css          # Styles CSS
│   │   ├── backround.jpg      # Image de fond
│   │   └── whats.jpg          # Image explicative
│   └── pdfs/                  # Dossier pour les PDFs générés
├── generated_projects/         # Projets générés
│   ├── pythonProjet/          # Projets Python
│   ├── javaProjet/            # Projets Java
│   └── cppProjet/             # Projets C++
└── README.md                  # Ce fichier
```

## 🔧 Configuration Avancée

### Personnalisation des Agents

Vous pouvez modifier les agents dans `agents.py` :

```python
# Exemple de personnalisation d'un agent
requirement_analysis = Agent(
    role='Senior Requirement Analyst',
    goal='Votre objectif personnalisé',
    backstory='Votre backstory personnalisé',
    tools=[web_search_tool],
    verbose=True,
    llm=llm
)
```

### Ajout de Nouveaux Langages

Pour ajouter un nouveau langage de programmation :

1. Modifiez `tasks.py` pour ajouter le support du langage
2. Mettez à jour `app.py` dans la fonction `save_and_execute_code`
3. Ajoutez les règles de formatage dans `agents.py`

### Personnalisation de l'Interface

Modifiez `templates/index.html` pour personnaliser l'interface utilisateur.

## 🧪 Tests et Validation

### Tests Automatiques

L'application effectue automatiquement :

- **Tests de syntaxe** : Vérification de la validité du code
- **Tests de compilation** : Compilation et exécution du code
- **Tests de qualité** : Analyse de la qualité du code
- **Tests de performance** : Identification des goulots d'étranglement

### Validation Manuelle

Pour valider manuellement :

1. Vérifiez le code généré dans `generated_projects/`
2. Testez l'exécution des programmes
3. Consultez la documentation PDF générée

## 🐛 Dépannage

### Problèmes Courants

1. **Erreur de clé API**
   ```
   Solution: Vérifiez vos clés API dans le fichier .env
   ```

2. **Erreur de compilation C++**
   ```
   Solution: Vérifiez l'installation de MinGW et le chemin dans app.py
   ```

3. **Erreur de compilation Java**
   ```
   Solution: Vérifiez l'installation de JDK et le chemin dans app.py
   ```

4. **Problème de mémoire**
   ```
   Solution: Réduisez la complexité de votre projet ou augmentez la RAM
   ```

### Logs et Debug

Activez le mode debug dans `app.py` :

```python
app.run(host='127.0.0.1', port=5000, debug=True)
```




## 🙏 Remerciements

- [CrewAI](https://crewai.com) - Framework multi-agents
- [Google Gemini](https://ai.google.dev) - Modèle de langage
- [Flask](https://flask.palletsprojects.com) - Framework web
- [Serper.dev](https://serper.dev) - API de recherche

## 🔮 Roadmap

### Version 2.0
- [ ] Support de plus de langages (Go, Rust, TypeScript)
- [ ] Interface de débogage intégrée
- [ ] Génération de tests unitaires avancés
- [ ] Support des frameworks populaires

### Version 2.1
- [ ] API REST pour intégration externe
- [ ] Mode batch pour traitement multiple
- [ ] Intégration avec des IDE populaires
- [ ] Système de plugins

---

**Fait avec ❤️ par l'équipe LLM2CODE**

*Transformez vos idées en code avec l'intelligence artificielle* 🚀
