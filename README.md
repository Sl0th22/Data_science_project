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

## **Fichier `.env`**

Créez un fichier `.env` à la racine du projet contenant :

```
EMAIL_EXPEDITEUR=sebxu2004@gmail.com
EMAIL_MDP=mot_de_passe_ou_token
EMAIL_DESTINATAIRE=destinataire@example.com
```

👉 Ce fichier sert à sécuriser vos informations d’envoi d’emails.  
👉 **Ne commitez jamais ce fichier sur GitHub** (assurez-vous qu’il est listé dans `.gitignore`).

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

---

##  **Ordre d'exécution**

1. `python Extraction_RSS.py`  
2. `python Extraction_CVE.py`  
3. `python Enrichissement_CVE.py`  
4. `python consolidate.py`  
5. Ouvrir et exécuter `visualisation.ipynb`  
6. `python alertes.py` 

---

## **Structure du projet**

```
.
├── data_Etape1/
│   ├── avis/
│   ├── alerte/
│   ├── Mitre/
│   └── First/
├── .env
├── .gitignore
├── requirements.txt
├── README.md
├── Extraction_RSS.py
├── Extraction_CVE.py
├── Enrichissement_CVE.py
├── consolidate.py
├── alertes.py
├── visualisation.ipynb
```

---

##  **Sécurité**

- **Ne publiez jamais votre `.env`**
- Changez immédiatement vos mots de passe si un secret a été exposé
- Un fichier `config_example.env` a été créé pour vous aider pour votre .env
