import pandas as pd

# === 1. Charger les deux fichiers CSV ===
fichier1 = "consolidate.ipynb"
fichier2 = "Projet_Mastercamp_Notebook.ipynb"

#print(f"Tentative de lecture de : {fichier1}")
#df1 = pd.read_csv(fichier1)

print(f"Tentative de lecture de : {fichier2}")
df2 = pd.read_csv(fichier2)


# === 2. Résumé global ===
print(f"📊 Fichier 1 : {fichier1} contient {len(df1)} lignes")
print(f"📊 Fichier 2 : {fichier2} contient {len(df2)} lignes\n")

# === 3. Identifier les CVE uniques ===
cve1 = set(df1["Identifiant CVE"])
cve2 = set(df2["Identifiant CVE"])

print("🔍 CVE dans fichier 1 mais pas dans fichier 2 :", len(cve1 - cve2))
print("🔍 CVE dans fichier 2 mais pas dans fichier 1 :", len(cve2 - cve1))
print("🟰 CVE communes :", len(cve1 & cve2), "\n")

# === 4. Lignes strictement identiques ===
colonnes_communes = list(set(df1.columns) & set(df2.columns))
df1_sorted = df1[sorted(colonnes_communes)].sort_values(by="Identifiant CVE").reset_index(drop=True)
df2_sorted = df2[sorted(colonnes_communes)].sort_values(by="Identifiant CVE").reset_index(drop=True)

# On aligne par nombre minimal de lignes
min_len = min(len(df1_sorted), len(df2_sorted))
diffs = (df1_sorted.head(min_len) != df2_sorted.head(min_len)).sum().sum()

print(f"📌 Différences de contenu (cellules différentes sur les lignes communes) : {diffs}")

# === 5. Exemple de lignes différentes sur CVE communes ===
cve_communes = list(cve1 & cve2)
for cve in cve_communes[:5]:  # tester sur les 5 premières
    row1 = df1[df1["Identifiant CVE"] == cve]
    row2 = df2[df2["Identifiant CVE"] == cve]
    if not row1.equals(row2):
        print(f"\n🔁 Différence détectée pour {cve}")
        display(row1)
        display(row2)

# === 6. Optionnel : Export des CVE différents ===
pd.DataFrame(sorted(cve1 - cve2), columns=["CVE uniquement dans fichier 1"]).to_csv("diffs_fichier1.csv", index=False)
pd.DataFrame(sorted(cve2 - cve1), columns=["CVE uniquement dans fichier 2"]).to_csv("diffs_fichier2.csv", index=False)
