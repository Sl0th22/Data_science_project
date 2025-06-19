import smtplib
from email.mime.text import MIMEText
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

# Chargement des variables d'environnement
load_dotenv()

EXPEDITEUR = os.getenv("EMAIL_EXPEDITEUR")
MOT_DE_PASSE = os.getenv("EMAIL_MDP")
DESTINATAIRE = os.getenv("EMAIL_DESTINATAIRE")

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
        return 0

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

    return alertes_envoyees

def run_continu(csv_path="consolidated_cve.csv"):
    if not os.path.isfile(csv_path):
        print(f"Fichier {csv_path} introuvable.")
        return

    last_mtime = os.path.getmtime(csv_path)

    print("Mode continu : en attente de modifications du fichier...")
    print("Appuyez sur Ctrl+C pour quitter le mode continu.")
    try:
        while True:
            time.sleep(5)
            current_mtime = os.path.getmtime(csv_path)
            if current_mtime != last_mtime:
                print("Changement détecté dans le fichier, vérification en cours...")
                verifier_alertes_et_envoyer_emails(csv_path=csv_path, mode="toutes")
                last_mtime = current_mtime
    except KeyboardInterrupt:
        print("\nArrêt du mode continu demandé par l'utilisateur.")

if __name__ == "__main__":
    while True:
        choix = input(
            "\nVoulez-vous envoyer :\n"
            "1 - Toutes les alertes critiques\n"
            "2 - Seulement les alertes critiques récentes (1h)\n"
            "3 - Exécuter en continu et envoyer dès qu'un changement est détecté\n"
            "Q - Quitter\n"
            "Votre choix (1/2/3/Q) : "
        ).strip().lower()

        if choix == "q":
            print("Fin du programme.")
            break
        elif choix == "2":
            verifier_alertes_et_envoyer_emails(mode="recentes")
        elif choix == "1":
            verifier_alertes_et_envoyer_emails(mode="toutes")
        elif choix == "3":
            run_continu()
        else:
            print("Choix invalide, veuillez réessayer.")

        print("Vérification des alertes terminée.")
