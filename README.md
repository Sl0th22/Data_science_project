
# Data_science_project

Ce projet traite de l'extraction, enrichissement, consolidation, alerte et visualisation de bulletins de sécurité ANSSI et de vulnérabilités CVE.

---

## Prérequis

- Python 3.8+
- Installez les dépendances nécessaires avec :

```bash
pip install -r requirements.txt
```

---

## Description des scripts

| Script                    | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| `Extraction_RSS.py`       | Télécharge les bulletins RSS de l'ANSSI (avis et alertes) au format JSON.   |
| `Extraction_CVE.py`       | Extrait les identifiants CVE présents dans les bulletins téléchargés.       |
| `Enrichissement_CVE.py`   | Récupère les infos CVE via les API de MITRE (CVSS, CWE) et FIRST (EPSS).    |
| `consolidate.py`          | Consolide toutes les données en un fichier CSV unique prêt pour l’analyse. |
| `alertes.py`              | Envoie des alertes par email si des produits critiques sont concernés.     |
| `visualisation.ipynb`     | Analyse exploratoire, visualisation et modèles ML (supervisé + non supervisé).        |
| `main.py`                 | Interface menu pour exécuter automatiquement toutes les étapes.             |

---

## Ordre d'exécution

### Mode automatique
Pour exécuter tout le pipeline automatiquement :

```bash
python main.py
```

### Étape par étape (mode manuel)

> Attention : le dossier `data_Etape1/` est nécessaire au bon fonctionnement du code.  
> Supprimez les triples guillemets `"""` à la fin des fichiers si nécessaire.

1. `Extraction_RSS.py`
2. `Extraction_CVE.py`
3. `Enrichissement_CVE.py`
4. `consolidate.py`
5. Ouvrir et exécuter `visualisation.ipynb`
6. `alertes.py`

---
## Fonctionnement général
Notre code fait l’extraction et l’enrichissement des bulletins de sécurité ANSSI et des vulnérabilités CVE en suivant ces étapes :
1. Téléchargement des données : Les scripts accèdent aux flux RSS de l’ANSSI (Extraction_RSS.py) et aux API publiques de MITRE et FIRST (Enrichissement_CVE.py) pour récupérer les bulletins, CVE, scores CVSS, CWE, EPSS et autres métadonnées.
2. Stockage local :Toutes les informations récupérées sont enregistrées sous forme de fichiers JSON dans des sous-dossiers de data_Etape1/ :

- data_Etape1/avis/ et data_Etape1/alerte/ pour les bulletins ANSSI

- data_Etape1/Mitre/ pour les données enrichies via l’API MITRE

- data_Etape1/First/ pour les scores EPSS via l’API FIRST

3. Consolidation :Le script consolidate.py lit ces fichiers locaux et fusionne toutes les données en un fichier CSV unique (consolidated_cve.csv) qui est ensuite utilisé pour les alertes par email et l’analyse (visualisations et modèles machine learning).
---
## Structure du projet

```
.
|- data_Etape1/
|  |- avis/
|  |- alerte/
|  |- Mitre/
|  |- First/
|- requirements.txt
|- README.md
|- Extraction_RSS.py
|- Extraction_CVE.py
|- Enrichissement_CVE.py
|- consolidate.py
|- alertes.py
|- visualisation.ipynb
|- main.py
```

---

## Contenu du Notebook

Le fichier `visualisation.ipynb` contient :

- Histogrammes des scores CVSS
- Répartition des vulnérabilités par CWE
- Nuages de points (CVSS vs EPSS)
- Classements des produits/éditeurs les plus affectés
- Clustering (KMeans) sur les données enrichies
- Classification (KNN) et validation

---

## Dépendances principales

```
pandas
requests
feedparser
matplotlib
seaborn
scikit-learn
```

---

## Exemple d'alerte

Un email est envoyé dès qu'un produit critique (ex: Windows, Apache...) est détecté dans une alerte ANSSI.

---

