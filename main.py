import os
from Extraction_RSS import telecharger_bulletins_rss
from Extraction_CVE import extraction_cve
from Enrichissement_CVE import Enrichissement_MITRE_API, enrichissement_first_api
from consolidate import consolidate_all


def menu():
    print("Bienvenue dans notre application de données d'alertes RSS de l'ANSSI !")
    print("1. Télécharger et traiter les bulletins RSS de l'ANSSI et extraire les informations en un CSV")
    print("2. Activer les alertes par email")
    print("3. Quitter l'application")
    choix = input("Veuillez entrer votre choix (1/2/3) : ")
    if choix == "1":
        print("Téléchargement des bulletins RSS de l'ANSSI...")
        telecharger_bulletins_rss("https://www.cert.ssi.gouv.fr/avis/feed", "./data_Etape1/avis")
        telecharger_bulletins_rss("https://www.cert.ssi.gouv.fr/alerte/feed", "./data_Etape1/alerte")
        
        print("Extraction des CVE...")
        cves = extraction_cve()
        
        print("Enrichissement des données avec l'API MITRE...")
        Enrichissement_MITRE_API(cves)
        
        print("Enrichissement des données avec l'API First...")
        enrichissement_first_api(cves)

        print("Consolidation des données...")
        df = consolidate_all()
        df.to_csv("consolidated_cve.csv", index=False, encoding="utf-8")
        print("Traitement terminé. Les données consolidées sont enregistrées dans 'consolidated_cve.csv'.")

    elif choix == "2":
        from alertes import run_continu, email_valide, verifier_alertes_et_envoyer_emails
        while True:
            destinataire = input("Veuillez entrer l'adresse email du destinataire : ").strip()
            if email_valide(destinataire):
                break
            else:
                print("Adresse email invalide. Merci de réessayer.")

        while True:
            print(f"\nDestinataire actuel : {destinataire}")
            choix = input(
                "\nQue souhaitez-vous faire ?\n"
                "1 - Envoyer toutes les alertes critiques\n"
                "2 - Envoyer seulement les alertes critiques récentes (1h)\n"
                "3 - Exécuter en continu et envoyer dès qu'un changement est détecté\n"
                "4 - Changer l'adresse email du destinataire\n"
                "Q - Quitter\n"
                "Votre choix (1/2/3/4/Q) : "
            ).strip().lower()

            if choix == "q":
                print("Fin du programme.")
                break
            elif choix == "1":
                verifier_alertes_et_envoyer_emails(destinataire, mode="toutes")
            elif choix == "2":
                verifier_alertes_et_envoyer_emails(destinataire, mode="recentes")
            elif choix == "3":
                run_continu(destinataire)
            elif choix == "4":
                while True:
                    destinataire = input("Nouvelle adresse email du destinataire : ").strip()
                    if email_valide(destinataire):
                        break
                    else:
                        print("Adresse email invalide. Merci de réessayer.")
            else:
                print("Choix invalide, veuillez réessayer.")

            print("Vérification des alertes terminée.")
    
    elif choix == "3":
        print("Merci d'avoir utilisé notre application. À bientôt !")
        exit()
    
    else:
        print("Choix invalide, veuillez réessayer.")
        menu()




if __name__ == "__main__":
    menu()