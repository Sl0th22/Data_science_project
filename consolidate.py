import os
import json
import pandas as pd

def get_bulletin_data(avis_dir, alerte_dir):
    bulletins = []
    for bulletin_type, path in [("Avis", avis_dir), ("Alerte", alerte_dir)]:
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(os.path.join(path, filename), encoding="utf-8") as f:
                    data = json.load(f)
                    bulletin_id = data.get("reference", filename.replace(".json", ""))
                    titre = data.get("title", "")
                    date_pub = data["revisions"][0]["revision_date"] if data.get("revisions") else "inconnu"
                    cves = [cve["name"] for cve in data.get("cves", []) if cve["name"].startswith("CVE-")]
                    
                    url = ""
                    if "AVI" in bulletin_id:
                        url = f"https://www.cert.ssi.gouv.fr/avis/{bulletin_id}/"
                    elif "ALE" in bulletin_id:
                        url = f"https://www.cert.ssi.gouv.fr/alerte/{bulletin_id}/"
                    else:
                        url = ""
                    for cve in cves:
                        bulletins.append({
                            "ID du bulletin (ANSSI)": bulletin_id,
                            "Titre du bulletin (ANSSI)": titre,
                            "Type de bulletin": bulletin_type,
                            "Date de publication": date_pub,
                            "Identifiant CVE": cve,
                            "Lien du bulletin (ANSSI)": url
                        })
    return pd.DataFrame(bulletins)

def get_mitre_data(mitre_dir):
    mitre_data = []
    for filename in os.listdir(mitre_dir):
        if filename.endswith(".json"):
            with open(os.path.join(mitre_dir, filename), encoding="utf-8") as f:
                data = json.load(f)
                mitre_data.append({
                    "Identifiant CVE": data.get("cve", filename.replace(".json", "")),
                    "Score CVSS": data.get("cvss_score", "Non disponible"),
                    "Base Severity": data.get("base_severity", "Non disponible"),
                    "Type CWE": data.get("cwe", "Non disponible"),
                    "CWE Description": data.get("cwe_desc", "Non disponible"),
                    "Description": data.get("description", "Non disponible"),
                    "Éditeur/Vendor": ", ".join([p.get("vendor", "") for p in data.get("produits", [])]),
                    "Produit": ", ".join([p.get("product", "") for p in data.get("produits", [])]),
                    "Versions affectées": "; ".join([", ".join(p.get("versions", [])) for p in data.get("produits", [])])
                })
    return pd.DataFrame(mitre_data)

def get_epss_data(epss_dir):
    epss_data = []
    for filename in os.listdir(epss_dir):
        if filename.endswith(".json"):
            with open(os.path.join(epss_dir, filename), encoding="utf-8") as f:
                data = json.load(f)
                epss_data.append({
                    "Identifiant CVE": data.get("cve", filename.replace(".json", "")),
                    "Score EPSS": data.get("epss_score", "Non disponible")
                })
    return pd.DataFrame(epss_data)

def consolidate_all():
    avis_dir = "data_Etape1/avis"
    alerte_dir = "data_Etape1/alerte"
    mitre_dir = "data_Etape1/Mitre"
    epss_dir = "data_Etape1/First"

    df_bulletins = get_bulletin_data(avis_dir, alerte_dir)
    df_mitre = get_mitre_data(mitre_dir)
    df_epss = get_epss_data(epss_dir)

    df = df_bulletins.merge(df_mitre, on="Identifiant CVE", how="left")
    df = df.merge(df_epss, on="Identifiant CVE", how="left")

    def get_severity(score):
        try:
            score = float(score)
            if 9 <= score <= 10:
                return "Critique"
            elif 7 <= score < 9:
                return "Élevée"
            elif 4 <= score < 7:
                return "Moyenne"
            elif 0 < score < 4:
                return "Faible"
            else:
                return "Non disponible"
        except:
            return "Non disponible"

    df["Base Severity"] = df["Score CVSS"].apply(get_severity)

    columns = [
        "ID du bulletin (ANSSI)",
        "Titre du bulletin (ANSSI)",
        "Type de bulletin",
        "Date de publication",
        "Identifiant CVE",
        "Score CVSS",
        "Base Severity",
        "Type CWE",
        "Score EPSS",
        "Lien du bulletin (ANSSI)",
        "Description",
        "Éditeur/Vendor",
        "Produit",
        "Versions affectées"
    ]
    df = df[columns]
    return df

