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

pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)

print(len(df_flux), "bulletins chargés")
print(df_flux.loc[2701])
