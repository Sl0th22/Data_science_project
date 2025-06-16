import requests
import time
from Extraction_CVE import extraction_cve

def Enrichissement_MITRE_API(cve_list, delay=0):
    enriched = []
    for cve_id in cve_list:
        url = f"https://cveawg.mitre.org/api/cve/{cve_id}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Erreur API pour {cve_id}: {response.status_code}")
                continue
            data = response.json()
            cna = data.get("containers", {}).get("cna", {})

            description = cna.get("descriptions", [{}])[0].get("value", "Non disponible")

            cvss_score = "Non disponible"
            metrics = cna.get("metrics", [])
            for metric in metrics:
                for key in metric:
                    if key.startswith("cvssV3"):
                        cvss_score = metric[key].get("baseScore", "Non disponible")
                        break

            cwe = "Non disponible"
            cwe_desc = "Non disponible"
            problemtype = cna.get("problemTypes", [])
            if problemtype and "descriptions" in problemtype[0]:
                desc = problemtype[0]["descriptions"][0]
                cwe = desc.get("cweId", "Non disponible")
                cwe_desc = desc.get("description", desc.get("value", "Non disponible"))

            produits = []
            affected = cna.get("affected", [])
            for product in affected:
                vendor = product.get("vendor", "")
                product_name = product.get("product", "")
                versions = [v.get("version", "") for v in product.get("versions", []) if v.get("status") == "affected"]
                produits.append({
                    "vendor": vendor,
                    "product": product_name,
                    "versions": versions
                })

            enriched.append({
                "cve": cve_id,
                "description": description,
                "cvss_score": cvss_score,
                "cwe": cwe,
                "cwe_desc": cwe_desc,
                "produits": produits
            })
        except Exception as e:
            print(f"Erreur pour {cve_id}: {e}")
    return enriched

extracted_cves = extraction_cve()
enriched_data = Enrichissement_MITRE_API(extracted_cves)
print(enriched_data[0])