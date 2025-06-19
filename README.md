# Data_science_project

Ce projet traite de l'extraction, enrichissement, consolidation, alerte et visualisation de bulletins de sécurité et CVE


---

##  **Prérequis**

Python 3.8+  
Installez les dépendances :

```bash
pip install -r requirements.txt
```

---

##  **Description des scripts**

| Script | Description |
|---------|-------------|
| `Extraction_RSS.py` | Télécharge les bulletins de l'ANSSI (avis et alertes) au format JSON. |
| `Extraction_CVE.py` | Extrait les identifiants CVE présents dans les bulletins téléchargés. |
| `Enrichissement_CVE.py` | Récupère les infos des CVE via les API de MITRE et FIRST (EPSS). |
| `consolidate.py` | Consolide toutes les données en un fichier CSV prêt pour la visualisation. |
| `alertes.py` | Vérifie les alertes récentes et envoie un email si des produits critiques sont concernés. |
| `visualisation.ipynb` | Analyse, visualisation et ML des données consolidées. |
| `main.py`| Lancement de l'application. |

---

##  **Ordre d'exécution**
Si le testeur veut lancer l'application :
Lancer le `main.py` 

Si le testeur veut lancer étape par étape il faut enlever les """ """ à la fin de chaque fichier, voici l'ordre:
Attention, le dossier data_Etape1 est essentiel pour le bon fonctionnement des programmes sans cela, il faut alors lancer depuis l'étape 1
1. `Extraction_RSS.py`  
2. `Extraction_CVE.py`  
3. `Enrichissement_CVE.py`  
4. `consolidate.py`  
5. Ouvrir et exécuter `visualisation.ipynb`  
6. `alertes.py` 

---

## **Structure du projet**

```
.
├── data_Etape1/
│   ├── avis/
│   ├── alerte/
│   ├── Mitre/
│   └── First/
├── requirements.txt
├── README.md
├── Extraction_RSS.py
├── Extraction_CVE.py
├── Enrichissement_CVE.py
├── consolidate.py
├── alertes.py
├── visualisation.ipynb
```
