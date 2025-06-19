import smtplib
from email.mime.text import MIMEText
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Chargement des variables d'environnement
load_dotenv()

EXPEDITEUR = os.getenv("EMAIL_EXPEDITEUR")
MOT_DE_PASSE = os.getenv("EMAIL_MDP")
DESTINATAIRE = os.getenv("EMAIL_DESTINATAIRE")

# Liste des produits du client à surveiller
CLIENT_PRODUCTS = ["Linux", "Apache", "Windows", "Chrome"]

def send_email(subject, body, to_email=DESTINATAIRE):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = EXPEDITEUR
    msg["To"] = to_email
    msg["Subject"] = subject

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EXPEDITEUR, MOT_DE_PASSE)
            server.sendmail(EXPEDITEUR, to_email, msg.as_string())
        print(f"[✓] Email envoyé à {to_email}")
    except Exception as e:
        print(f"[✗] Erreur lors de l'envoi du mail : {e}")

def construire_url(row):
    ref = row.get("ID du bulletin (ANSSI)", "")
    if "ALE" in ref:
        return f"https://www.cert.ssi.gouv.fr/alerte/{ref}/"
    elif "AVI" in ref:
        return f"https://www.cert.ssi.gouv.fr/avis/{ref}/"
    else:
        return "Lien non fourni"

def verifier_alertes_et_envoyer_emails(csv_path="consolidated_cve.csv", mode="toutes"):
    if not os.path.isfile(csv_path):
        print(f"Fichier {csv_path} introuvable.")
        return

    df = pd.read_csv(csv_path)

    if mode == "recentes":
        df["Date de publication"] = pd.to_datetime(df["Date de publication"], errors="coerce")
        seuil = datetime.now() - timedelta(hours=1)
        df = df[df["Date de publication"] >= seuil]

    alertes_df = df[
        (df["Base Severity"].str.lower() == "critique") &
        (
            df["Produit"]
            .fillna("")
            .str.lower()
            .apply(lambda x: any(prod.lower() in x for prod in CLIENT_PRODUCTS))
        )
    ]

    alertes_envoyees = 0

    for _, row in alertes_df.iterrows():
        titre = row.get("Titre du bulletin (ANSSI)", "Alerte sécurité ANSSI")
        reference = row.get("ID du bulletin (ANSSI)", "Inconnu")
        date_pub = row.get("Date de publication", "Inconnu")
        url = construire_url(row)

        corps = (
            f"Alerte ANSSI détectée concernant vos produits :\n\n"
            f"Titre : {titre}\n"
            f"Référence : {reference}\n"
            f"Date : {date_pub}\n"
            f"Lien : {url}\n"
            f"\nVeuillez vérifier au plus vite."
        )

        subject = f"[ALERTE] {titre}"
        send_email(subject, corps)
        alertes_envoyees += 1

    if alertes_envoyees == 0:
        if mode == "recentes":
            print("Aucune alerte critique détectée pour vos produits dans la dernière heure.")
        else:
            print("Aucune alerte critique détectée pour vos produits.")
    else:
        print(f"{alertes_envoyees} alerte(s) critique(s) envoyée(s).")

if __name__ == "__main__":
    choix = input("Voulez-vous envoyer :\n1 - Toutes les alertes critiques\n2 - Seulement les alertes critiques récentes (1h)\nVotre choix (1/2) : ").strip()
    if choix == "2":
        verifier_alertes_et_envoyer_emails(mode="recentes")
    else:
        verifier_alertes_et_envoyer_emails(mode="toutes")

    print("Vérification des alertes terminée.")
