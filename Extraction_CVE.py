import os
import json

def extraction_cve():
    all_cves = []
    path_alerte = ".\\data_Etape1\\alerte"
    for filename in os.listdir(path_alerte):
        if filename.endswith(".json"):
            with open(os.path.join(path_alerte, filename), 'r') as file:
                data = json.load(file)
                cves = data.get("cves", [])
                for cve in cves:
                    name = cve["name"]
                    if name.startswith("CVE-"):
                        all_cves.append(name)
    path_avis = ".\\data_Etape1\\avis"
    for filename in os.listdir(path_avis):
        if filename.endswith(".json"):
            with open(os.path.join(path_avis, filename), 'r') as file:
                data = json.load(file)
                cves = data.get("cves", [])
                for cve in cves:
                    name = cve["name"]
                    if name.startswith("CVE-"):
                        all_cves.append(name)
    return sorted(list(set(all_cves)))

