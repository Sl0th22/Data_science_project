import os
import json
import pandas as pd

def charger_bulletins(chemin, type_bulletin):
    data_flux = []
    for fichier in os.listdir(chemin):
        with open(os.path.join(chemin, fichier)) as f:
            data = json.load(f)
            reference = data.get("reference")
            titre = data.get("title")
            date_pub = data["revisions"][0]["revision_date"] if data.get("revisions") else "inconnu"
            cves = [cve["name"] for cve in data.get("cves", [])]
            description = data.get("summary", "")

            liens = ""
            if "links" in data and data["links"]:
                liens = ", ".join([link["url"] for link in data["links"] if "url" in link and link["url"]])

            data_flux.append({
                "id": reference,
                "titre": titre,
                "description": description,
                "date": date_pub,
                "lien": liens,
                "cves": cves,
                "type": type_bulletin
            })
    return data_flux


avis_path = "data_pour_TD_final/Avis/"
alertes_path = "data_pour_TD_final/Alertes/"

data_flux = charger_bulletins(avis_path, "Avis")
data_flux += charger_bulletins(alertes_path, "Alerte")

df_flux = pd.DataFrame(data_flux)

print(df_flux.loc[2701])


## Etape 2 : Extraction des CVEs dans une liste
def extraire_cves(df):
    cve_list = []
    for index, row in df.iterrows():
        for cve in row['cves']:
            cve_list.append(cve)
    return cve_list

cve_list = extraire_cves(df_flux)

print(len(cve_list))

## Etape 3 : Enrichissement des données CVE

def enrichir_cves_mitre(cve_list):
    cve_data = []
    cpt = 0
    for cve in cve_list:
        try:
            with open(f"data_pour_TD_final/mitre/{cve}", encoding="utf-8") as f:
                data = json.load(f)
                cna = data.get("containers", {}).get("cna", {})

                description = cna.get("descriptions", [{}])[0].get("value", "Non disponible")

                cvss_score = "Non disponible"
                metrics = cna.get("metrics", [])
                for metric in metrics:
                    for key in metric:
                        if key.startswith("cvssV3"):
                            cvss_score = metric[key].get("baseScore", "Non disponible")
                            break

                cwe_type = "Non disponible"
                problemtype = cna.get("problemTypes", [])
                if problemtype and "descriptions" in problemtype[0]:
                    desc = problemtype[0]["descriptions"][0]
                    cwe_type = desc.get("description", desc.get("value", "Non disponible"))
                elif "x_legacyV4Record" in cna:
                    legacy = cna["x_legacyV4Record"]
                    try:
                        pt = legacy["problemtype"]["problemtype_data"][0]["description"][0]
                        cwe_type = pt.get("value", "Non disponible")
                    except Exception:
                        pass
                elif "x_legacyV4Record" in data:
                    legacy = data["x_legacyV4Record"]
                    try:
                        pt = legacy["problemtype"]["problemtype_data"][0]["description"][0]
                        cwe_type = pt.get("value", "Non disponible")
                    except Exception:
                        pass

                references = []
                if "references" in cna:
                    references = [ref.get("url", "") for ref in cna["references"]]

                cve_data.append({
                    "cve": cve,
                    "description": description,
                    "cvss": cvss_score,
                    "cwe_type": cwe_type,
                    "references": references
                })
        except FileNotFoundError:
            cpt += 1
    print("Nombre de fichiers non trouvés :", cpt, "sur", len(cve_list))
    return pd.DataFrame(cve_data)


cve_liste_enrichie = enrichir_cves_mitre(cve_list)
print("Nombre de CVE avec un score CVSS :", (cve_liste_enrichie['cvss'] != "Non disponible").sum())
print(cve_liste_enrichie.loc[1515])
#53283