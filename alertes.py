import smtplib
from email.mime.text import MIMEText
import json
import os
import time
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()

EXPEDITEUR = os.getenv("EMAIL_EXPEDITEUR")
MOT_DE_PASSE = os.getenv("EMAIL_MDP")
DESTINATAIRE = os.getenv("EMAIL_DESTINATAIRE")

# Liste des produits du client à surveiller
CLIENT_PRODUCTS = ["Linux", "Apache", "Windows"]

def send_email(subject, body, to_email=DESTINATAIRE):
    msg = MIMEText(body, "plain", "utf-8")
    msg['From'] = EXPEDITEUR
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EXPEDITEUR, MOT_DE_PASSE)
            server.sendmail(EXPEDITEUR, to_email, msg.as_string())
        print(f"[✓] Email envoyé à {to_email}")
    except Exception as e:
        print(f"[✗] Erreur lors de l'envoi du mail : {e}")

def produit_concerne(alert_data, produits_client):
    contenu = json.dumps(alert_data).lower()
    return any(prod.lower() in contenu for prod in produits_client)

def construire_url(data):
    ref = data.get("reference", "")
    if "ALE" in ref:
        return f"https://www.cert.ssi.gouv.fr/alerte/{ref}/"
    elif "AVI" in ref:
        return f"https://www.cert.ssi.gouv.fr/avis/{ref}/"
    else:
        return "Lien non fourni"

def verifier_alertes_et_envoyer_emails(dossier_alertes="./data_Etape1/alerte"):
    maintenant = time.time()
    une_heure = timedelta(hours=1).total_seconds()

    alertes_envoyees = 0
    max_alertes = 5  # Limite pour éviter de spammer

    for fichier in os.listdir(dossier_alertes):
        if fichier.endswith(".json"):
            chemin = os.path.join(dossier_alertes, fichier)
            if os.path.isfile(chemin):
                if maintenant - os.path.getmtime(chemin) < une_heure:
                    with open(chemin, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    if produit_concerne(data, CLIENT_PRODUCTS):
                        titre = data.get("title", "Alerte sécurité ANSSI")
                        url = construire_url(data)
                        date_revision = data.get("revisions", [{}])[0].get("revision_date", "Inconnu")
                        reference = data.get("reference", "Inconnu")

                        corps = (
                            f"Alerte ANSSI détectée concernant vos produits :\n\n"
                            f"Titre : {titre}\n"
                            f"Référence : {reference}\n"
                            f"Date : {date_revision}\n"
                            f"Lien : {url}\n"
                            f"\nVeuillez vérifier au plus vite."
                        )

                        send_email(subject=f"[ALERTE] {titre}", body=corps)
                        alertes_envoyees += 1

                        if alertes_envoyees >= max_alertes:
                            print("[!] Nombre maximal d'alertes envoyées atteint.")
                            break

    if alertes_envoyees == 0:
        print("Aucune alerte critique détectée pour vos produits.")

if __name__ == "__main__":
    verifier_alertes_et_envoyer_emails()
    print("Vérification des alertes terminée.")
