"""Génère profile/README.md du profil GitHub akm12-dev (badges dynamiques réels, aucune donnée inventée)."""
import sys
import urllib.parse

OUT = sys.argv[1]
STATS = "https://raw.githubusercontent.com/akm12-dev/releases/stats/clones.json"
SITE = "https://akm12.com"


def badge(query: str, label: str, prefix: str = "", color: str = "0A5FDB") -> str:
    q = {
        "url": STATS,
        "query": query,
        "label": label,
        "color": color,
        "labelColor": "0E1726",
        "style": "flat-square",
        "cacheSeconds": "1800",
    }
    if prefix:
        q["prefix"] = prefix
    return "https://img.shields.io/badge/dynamic/json?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)


SOFTWARE = [
    ("edendisk", "EdenDisk",
     "Transfère les données d’un ancien poste et prépare les disques en toute sécurité.",
     "Windows 10 / 11", "Disques et stockage"),
    ("sav-service-tool", "SAV Service Tool",
     "Remet à zéro le compteur d’encre usagée (erreur 5B00) et entretient les jet d’encre Canon.",
     "Windows 10 / 11", "Impression"),
    ("canon-scan-setup", "Canon Scan Setup",
     "Configure le scan vers dossier et le scan vers e-mail des multifonctions Canon.",
     "Windows", "Numérisation"),
    ("toshiba-lexmark-scan-setup", "Toshiba &amp; Lexmark Scan Setup",
     "Configure le scan vers dossier et le scan vers e-mail des multifonctions Toshiba et Lexmark.",
     "Windows", "Numérisation"),
]

COMPAT = {
    "edendisk": [("Disques", "Disques reconnus par Windows 10 / 11 (64 bits) ; la préparation refuse toujours le disque système")],
    "sav-service-tool": [
        ("Marque", "Canon uniquement, imprimantes jet d’encre"),
        ("Remise à zéro 5B00", "MAXIFY MB2100 / MB2150 (firmware 1.130), G6000 / G6020"),
        ("Page calibrage et nettoyages", "MAXIFY MB2100 / MB2150, série G3000 (non testée par AKM12)"),
        ("Recherche réseau", "Imprimantes Canon du réseau local"),
    ],
    "canon-scan-setup": [("Matériel", "Imprimantes multifonctions Canon compatibles (Remote UI)")],
    "toshiba-lexmark-scan-setup": [("Matériel", "Multifonctions Toshiba e-STUDIO (TopAccess) et Lexmark (Embedded Web Server)")],
}


def card(sid, name, tagline, system, cat):
    fiche = f"{SITE}/logiciels/{sid}"
    return f"""<td width="50%" valign="top">
<a href="{fiche}"><img src="assets/{sid}.png" alt="Capture d’écran de {name}" width="100%"></a>

### [{name}]({fiche})

{tagline}

<img src="{badge(f'$.software.{sid}.version', 'version', 'v')}" alt="version"> <img src="{badge(f'$.software.{sid}.downloads', 'téléchargements')}" alt="téléchargements"> <img src="{badge(f'$.repos.{sid}.total', 'clones', color='22314D')}" alt="clones">

**{system}** · {cat} · Gratuit

[**Télécharger**]({fiche}#recuperer) &nbsp;·&nbsp; [Code source](https://github.com/akm12-dev/{sid}) &nbsp;·&nbsp; [Guide PDF]({fiche}#documentation)
</td>"""


rows = []
for i in range(0, len(SOFTWARE), 2):
    rows.append("<tr>\n" + "\n".join(card(*s) for s in SOFTWARE[i:i + 2]) + "\n</tr>")

clone_blocks = "\n\n".join(
    f"**{name}**\n\n```bash\ngit clone https://github.com/akm12-dev/{sid}.git\n```"
    for sid, name, *_ in SOFTWARE
)

compat = "\n\n".join(
    f"**{name}**\n\n| | |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in COMPAT[sid])
    for sid, name, *_ in SOFTWARE
)

readme = f"""<p align="center">
  <a href="{SITE}"><img src="assets/banner.svg" alt="AKM12 — Advanced Knowledge &amp; Maintenance : outils gratuits pour les techniciens informatiques" width="100%"></a>
</p>

<p align="center">
  <a href="{SITE}"><img src="https://img.shields.io/badge/site-akm12.com-0A5FDB?style=flat-square&labelColor=0E1726" alt="Site akm12.com"></a>
  <a href="https://github.com/akm12-dev/releases/releases"><img src="https://img.shields.io/badge/t%C3%A9l%C3%A9chargements-gratuits%2C%20sans%20inscription-0F6B3F?style=flat-square&labelColor=0E1726" alt="Téléchargements gratuits, sans inscription"></a>
  <img src="https://img.shields.io/badge/code-consultable-22314D?style=flat-square&labelColor=0E1726" alt="Code consultable">
</p>

<p align="center">
  <b>Des outils simples pour les interventions de tous les jours</b> : imprimantes, numérisation, disques.<br>
  Chaque logiciel est gratuit, vérifiable (empreinte SHA-256) et accompagné d’un guide PDF.
</p>

## Logiciels

<table>
{chr(10).join(rows)}
</table>

<sub>Compteurs réels relevés chez GitHub toutes les heures. Les guides PDF et les fichiers d’empreintes ne sont pas comptés comme téléchargements.</sub>

## Récupérer un logiciel

```mermaid
flowchart LR
    A["Fiche sur akm12.com"] --> B["Télécharger gratuitement"]
    B --> C["Vérifier l’empreinte SHA-256"]
    C --> D["Lancer le logiciel"]
    A -. "développeurs" .-> E["git clone du dépôt"]
    E --> F["Lire ou compiler le code"]
```

<details>
<summary><b>Cloner le code source</b></summary>
<br>

Le dépôt contient le code et sa documentation, pas forcément un logiciel prêt à lancer : pour simplement l’utiliser, prenez le téléchargement direct sur la fiche.

{clone_blocks}

</details>

<details>
<summary><b>Vérifier un téléchargement (SHA-256)</b></summary>
<br>

Dans PowerShell, depuis le dossier du fichier téléchargé :

```powershell
Get-FileHash .\\NomDuFichier.exe -Algorithm SHA256
```

Comparez le résultat avec l’empreinte indiquée sur la fiche du logiciel, ou avec le fichier `SHA256SUMS` joint à chaque [version publiée](https://github.com/akm12-dev/releases/releases). Les exécutables ne sont pas encore signés : Windows SmartScreen peut afficher un avertissement au premier lancement.

</details>

<details>
<summary><b>Modèles compatibles</b></summary>
<br>

{compat}

</details>

<details>
<summary><b>Licence</b></summary>
<br>

Code consultable, tous droits réservés : vous pouvez lire, cloner et compiler le code pour votre propre usage. La redistribution, la publication d’une version modifiée et la réutilisation demandent l’accord d’AKM12. Les versions officielles gratuites sont publiées sur [akm12.com]({SITE}) et dans [akm12-dev/releases](https://github.com/akm12-dev/releases).

</details>

---

<p align="center">
  <a href="{SITE}">akm12.com</a> &nbsp;·&nbsp;
  <a href="{SITE}/logiciels">Tous les logiciels</a> &nbsp;·&nbsp;
  <a href="{SITE}/documentation">Documentation</a> &nbsp;·&nbsp;
  <a href="https://github.com/akm12-dev/releases/releases">Versions publiées</a>
  <br><sub>Chaîne YouTube AKM12 : bientôt disponible.</sub>
</p>
"""

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(readme)
print("ok", len(readme))
