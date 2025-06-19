
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

