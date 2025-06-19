import feedparser
import requests
import os
import json
import time

def telecharger_bulletins_rss(rss_url, dossier):
    rss_feed = feedparser.parse(rss_url)
    os.makedirs(dossier, exist_ok=True)
    for i in rss_feed.entries:
        url = i.link
        response = requests.get(url.rstrip('/') + '/json/')
        if response.status_code == 200:
            avis_json = response.json()
            reference = avis_json.get("reference", "sans_reference")
            with open(os.path.join(dossier, f"{reference}.json"), "w", encoding="utf-8") as f:
                json.dump(avis_json, f, ensure_ascii=False, indent=4)
        else:
            print(f"Erreur lors de la récupération du bulletin {i.title}: {response.status_code}")
        time.sleep(2)

