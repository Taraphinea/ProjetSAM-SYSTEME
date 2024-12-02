# Traitement de Fichiers SAM

Ce projet vise à analyser et extraire des informations pertinentes à partir de fichiers SAM (Sequence Alignment/Map), un format standard utilisé pour stocker des données d'alignement issues de séquençages génomiques.

---
## 🚀 Fonctionnalités principales

- **Vérification du format SAM** : Validation des en-têtes et du nombre minimum de colonnes.
- **Extraction des informations clés** : Nom des reads, flags, chromosome, position, qualité, séquence.
- **Analyse des données** : Calcul de métriques importantes comme la qualité de mapping.

---
## 📂 Structure du projet

- `verif_sam.sh` : Script Bash pour valider le fichier SAM.
- `analyse_sam.py` : Script Python pour extraire les données et effectuer l'analyse.
- `headmapping.sam` : Fichier SAM d'exemple pour tester le workflow.
- `README.md` : Documentation du projet.

---
## 🛠 Prérequis
Avant de commencer, assurez-vous d'avoir installé :
- [Python 3.x](https://www.python.org/) (ou Bash, selon votre version préférée du script)
- Git (facultatif, pour cloner le dépôt)

---
## 🚀 Utilisation
### 1. Vérification du fichier SAM en bash
Exemples de sortie :
* Si le fichier est valide :
Le fichier test.sam est au format SAM.
Vous pouvez continuer avec ce fichier pour la suite du programme. 
* Si le fichier est invalide :
Erreur : Le fichier test.sam n'est pas au format SAM.
Veuillez changer de fichier d'entrée.
### 2.Création d'un dictionnaire : 
Le dictionnaire à bien été créer quand le terminal affiche : Dictionnaire SAM créé avec "n" entrées.)
### 3.Analyse du fichier 

