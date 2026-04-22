# 👑 LORD-CREATE — Générateur de Devis Professionnel

> **Code With Royalty** — Application graphique de création de devis pour ventes de sites web

---

## 📦 Installation rapide (Kali Linux)

```bash
# 1. Rendre le script exécutable
chmod +x install.sh

# 2. Lancer l'installation
./install.sh
```

L'installation :
- Vérifie/installe Python3 & tkinter
- Installe WeasyPrint pour l'export PDF
- Crée un alias `lord-create` dans votre terminal
- Ajoute l'app dans votre menu applications graphique

---

## 🚀 Lancer l'application

```bash
# Option 1 — Via alias (après installation)
lord-create

# Option 2 — Direct
python3 lord_create_devis.py

# Option 3 — Sans installation
python3 lord_create_devis.py
```

---

## ✨ Fonctionnalités

### 3 Types de sites préconfigurés
| Type | Prix de base | Description |
|------|-------------|-------------|
| 🌐 Site Vitrine | 150 000 XOF | Présence en ligne pour TPE/PME |
| 🛒 E-Commerce | 400 000 XOF | Boutique avec paiement intégré |
| ⚙️ Application Web | 700 000 XOF | SaaS, dashboard, outil métier |

### Champs du devis
- **Identité** : N° devis auto, dates d'émission et validité
- **Vendeur** : Nom, email, tél, adresse, NINEA/SIRET
- **Client** : Nom, email, tél, pays (27 pays), adresse
- **Devise** : 12 devises (XOF, EUR, USD, GBP, MAD, CAD…)
- **Offres** : Checkboxes avec prix par option
- **Délai** : 5 options (Express à Flexible) avec modificateur de prix
- **Remise** : Pourcentage personnalisable
- **TVA** : Activable avec taux configurable
- **Paiement** : 5 modalités prédéfinies
- **Conditions générales** : Texte éditable
- **Notes** : Message personnalisé au client

### Export
- **PDF** via WeasyPrint (pip install weasyprint)
- **HTML** (fallback, ouvrable dans navigateur, imprimable)
- **JSON** : Sauvegarde/rechargement complet du devis

---

## 🖨️ Activer l'export PDF

```bash
# Option A — WeasyPrint (recommandé)
pip3 install weasyprint

# Option B — wkhtmltopdf
sudo apt install wkhtmltopdf
```

---

## 🎨 Design

L'application reprend la charte graphique **LORD-CREATE** :
- Fond sombre (`#0D1B2A`) + accents bleu royal (`#3B63E8`)
- Typographie Georgia/serif
- Devis exporté en HTML professionnel style magazine

---

## 📋 Dépendances

| Package | Usage | Requis |
|---------|-------|--------|
| `tkinter` | Interface graphique | ✅ Oui |
| `weasyprint` | Export PDF | ⚡ Optionnel |
| `wkhtmltopdf` | Export PDF (alt) | ⚡ Optionnel |

Tout le reste utilise la bibliothèque standard Python 3.

---

## 📁 Structure des fichiers

```
lord-create/
├── lord_create_devis.py   # Application principale
├── install.sh             # Script d'installation Kali
└── README.md              # Ce fichier
```

---

*LORD-CREATE © 2025 — Code With Royalty 👑*
