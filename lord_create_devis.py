#!/usr/bin/env python3
"""
LORD-CREATE - Générateur de Devis Professionnel
Application graphique pour la création de devis de sites web
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from datetime import datetime, timedelta
import subprocess
import re

# ─────────────────────────────────────────────
# CONSTANTES & CONFIG
# ─────────────────────────────────────────────

APP_TITLE = "LORD-CREATE — Générateur de Devis"
VERSION = "1.0.0"

DEVISES = {
    "XOF – Franc CFA (BCEAO)": "XOF",
    "EUR – Euro": "EUR",
    "USD – Dollar américain": "USD",
    "GBP – Livre sterling": "GBP",
    "CAD – Dollar canadien": "CAD",
    "MAD – Dirham marocain": "MAD",
    "CDF – Franc congolais": "CDF",
    "GNF – Franc guinéen": "GNF",
    "XAF – Franc CFA (BEAC)": "XAF",
    "CHF – Franc suisse": "CHF",
    "JPY – Yen japonais": "JPY",
    "BRL – Real brésilien": "BRL",
}

PAYS = [
    "Sénégal", "France", "Côte d'Ivoire", "Mali", "Burkina Faso",
    "Guinea", "Togo", "Bénin", "Niger", "Cameroun", "Maroc",
    "Algérie", "Tunisie", "RD Congo", "Congo", "Gabon",
    "Belgique", "Suisse", "Canada", "États-Unis", "Royaume-Uni",
    "Espagne", "Italie", "Portugal", "Allemagne", "Pays-Bas",
    "Autre"
]

TYPES_SITES = {
    "🌐 Site Vitrine": {
        "desc": "Présence en ligne professionnelle, idéal pour TPE/PME",
        "icon": "🌐",
        "base_prix": 150000,
        "offres": {
            "Design UI/UX personnalisé": {"prix": 50000, "inclus": True},
            "Site responsive (mobile/tablette)": {"prix": 30000, "inclus": True},
            "Formulaire de contact": {"prix": 20000, "inclus": True},
            "SEO de base": {"prix": 25000, "inclus": True},
            "Jusqu'à 5 pages": {"prix": 0, "inclus": True},
            "Pages supplémentaires (par page)": {"prix": 15000, "inclus": False},
            "Chat en direct / WhatsApp": {"prix": 20000, "inclus": False},
            "Blog intégré": {"prix": 35000, "inclus": False},
            "Galerie photo avancée": {"prix": 20000, "inclus": False},
            "Animations avancées": {"prix": 30000, "inclus": False},
            "Multilingue (par langue)": {"prix": 25000, "inclus": False},
            "Hébergement 1 an inclus": {"prix": 30000, "inclus": False},
            "Nom de domaine .com 1 an": {"prix": 10000, "inclus": False},
            "SSL / HTTPS": {"prix": 10000, "inclus": False},
            "Google Analytics": {"prix": 10000, "inclus": False},
            "Maintenance 3 mois": {"prix": 40000, "inclus": False},
        }
    },
    "🛒 E-Commerce": {
        "desc": "Boutique en ligne complète avec paiement intégré",
        "icon": "🛒",
        "base_prix": 400000,
        "offres": {
            "Design boutique personnalisé": {"prix": 80000, "inclus": True},
            "Catalogue produits (jusqu'à 50)": {"prix": 60000, "inclus": True},
            "Panier & Checkout sécurisé": {"prix": 50000, "inclus": True},
            "Gestion des stocks": {"prix": 40000, "inclus": True},
            "Dashboard admin": {"prix": 50000, "inclus": True},
            "Site responsive": {"prix": 30000, "inclus": True},
            "SEO e-commerce": {"prix": 40000, "inclus": True},
            "Paiement Mobile Money (Wave/Orange)": {"prix": 50000, "inclus": False},
            "Paiement Stripe / PayPal": {"prix": 60000, "inclus": False},
            "Paiement à la livraison": {"prix": 20000, "inclus": False},
            "Produits illimités": {"prix": 50000, "inclus": False},
            "Gestion multi-devises": {"prix": 40000, "inclus": False},
            "Emails transactionnels": {"prix": 30000, "inclus": False},
            "Programme de fidélité": {"prix": 45000, "inclus": False},
            "Codes promo / Réductions": {"prix": 25000, "inclus": False},
            "Intégration livraison": {"prix": 35000, "inclus": False},
            "Application mobile (iOS/Android)": {"prix": 300000, "inclus": False},
            "Hébergement 1 an inclus": {"prix": 50000, "inclus": False},
            "Nom de domaine .com 1 an": {"prix": 10000, "inclus": False},
            "Maintenance 3 mois": {"prix": 60000, "inclus": False},
        }
    },
    "⚙️ Application Web": {
        "desc": "Plateforme SaaS, dashboard, outil métier sur mesure",
        "icon": "⚙️",
        "base_prix": 700000,
        "offres": {
            "Architecture & Conception": {"prix": 100000, "inclus": True},
            "Authentification utilisateurs": {"prix": 60000, "inclus": True},
            "Dashboard interactif": {"prix": 80000, "inclus": True},
            "Base de données personnalisée": {"prix": 70000, "inclus": True},
            "API REST / Backend": {"prix": 100000, "inclus": True},
            "Design UI/UX custom": {"prix": 80000, "inclus": True},
            "Gestion des rôles & permissions": {"prix": 50000, "inclus": False},
            "Notifications email & SMS": {"prix": 40000, "inclus": False},
            "Rapports & exports PDF/Excel": {"prix": 60000, "inclus": False},
            "Intégration API tierce": {"prix": 50000, "inclus": False},
            "Paiement en ligne": {"prix": 80000, "inclus": False},
            "Multi-tenant (SaaS)": {"prix": 150000, "inclus": False},
            "Intelligence Artificielle / ML": {"prix": 200000, "inclus": False},
            "Application mobile (iOS + Android)": {"prix": 500000, "inclus": False},
            "Tests automatisés": {"prix": 80000, "inclus": False},
            "Documentation technique": {"prix": 50000, "inclus": False},
            "Formation équipe client": {"prix": 50000, "inclus": False},
            "Support & Maintenance 6 mois": {"prix": 120000, "inclus": False},
            "Hébergement cloud 1 an": {"prix": 80000, "inclus": False},
        }
    }
}

DELAIS = {
    "7 jours (Express +30%)": 1.30,
    "14 jours (Rapide +15%)": 1.15,
    "21 jours (Standard)": 1.00,
    "30 jours (Confort -5%)": 0.95,
    "45 jours (Flexible -10%)": 0.90,
}

STATUT_PAIEMENT = [
    "100% à la commande",
    "50% acompte / 50% à la livraison",
    "30% acompte / 70% à la livraison",
    "30% / 30% / 40% (3 jalons)",
    "Sur devis personnalisé",
]

COULEURS = {
    "bg_dark": "#0D1B2A",
    "bg_card": "#162032",
    "bg_input": "#1C2A3A",
    "accent_blue": "#3B63E8",
    "accent_light": "#6B8FF0",
    "accent_gold": "#F0B429",
    "text_white": "#EEF2FF",
    "text_gray": "#8B9EC7",
    "text_muted": "#4A5A7A",
    "border": "#243450",
    "success": "#22C55E",
    "danger": "#EF4444",
    "warning": "#F59E0B",
}

# ─────────────────────────────────────────────
# APPLICATION PRINCIPALE
# ─────────────────────────────────────────────

class LordCreateApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg=COULEURS["bg_dark"])
        
        # Variables
        self.site_type_var = tk.StringVar(value=list(TYPES_SITES.keys())[0])
        self.devise_var = tk.StringVar(value=list(DEVISES.keys())[0])
        self.pays_var = tk.StringVar(value="Sénégal")
        self.delai_var = tk.StringVar(value=list(DELAIS.keys())[2])
        self.paiement_var = tk.StringVar(value=STATUT_PAIEMENT[1])
        self.tva_var = tk.BooleanVar(value=False)
        self.tva_taux_var = tk.StringVar(value="18")
        self.remise_var = tk.StringVar(value="0")
        self.offres_vars = {}
        self.total_var = tk.StringVar(value="0")
        
        # Numéro de devis auto
        self.numero_devis = self._generer_numero()
        
        self._setup_styles()
        self._build_ui()
        self._update_offres()
        self._calculer_total()

    def _generer_numero(self):
        now = datetime.now()
        return f"LC-{now.strftime('%Y%m')}-{now.strftime('%d%H%M')}"

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Dark.TFrame", background=COULEURS["bg_dark"])
        style.configure("Card.TFrame", background=COULEURS["bg_card"])
        style.configure("Dark.TLabel",
            background=COULEURS["bg_dark"],
            foreground=COULEURS["text_white"],
            font=("Georgia", 11))
        style.configure("Card.TLabel",
            background=COULEURS["bg_card"],
            foreground=COULEURS["text_white"],
            font=("Georgia", 11))
        style.configure("Title.TLabel",
            background=COULEURS["bg_dark"],
            foreground=COULEURS["text_white"],
            font=("Georgia", 22, "bold"))
        style.configure("Section.TLabel",
            background=COULEURS["bg_card"],
            foreground=COULEURS["accent_light"],
            font=("Georgia", 12, "bold"))
        style.configure("Total.TLabel",
            background=COULEURS["bg_card"],
            foreground=COULEURS["accent_gold"],
            font=("Georgia", 18, "bold"))
        style.configure("Muted.TLabel",
            background=COULEURS["bg_card"],
            foreground=COULEURS["text_gray"],
            font=("Georgia", 9))
        
        style.configure("Dark.TCombobox",
            fieldbackground=COULEURS["bg_input"],
            background=COULEURS["bg_input"],
            foreground=COULEURS["text_white"],
            selectbackground=COULEURS["accent_blue"],
            borderwidth=0)
        style.map("Dark.TCombobox",
            fieldbackground=[("readonly", COULEURS["bg_input"])],
            foreground=[("readonly", COULEURS["text_white"])])
        
        style.configure("Dark.TCheckbutton",
            background=COULEURS["bg_card"],
            foreground=COULEURS["text_white"],
            font=("Georgia", 10),
            indicatorbackground=COULEURS["bg_input"],
            indicatorforeground=COULEURS["accent_blue"])
        style.map("Dark.TCheckbutton",
            background=[("active", COULEURS["bg_card"])],
            foreground=[("active", COULEURS["accent_light"])])
        
        style.configure("Dark.TEntry",
            fieldbackground=COULEURS["bg_input"],
            foreground=COULEURS["text_white"],
            insertcolor=COULEURS["text_white"],
            borderwidth=0)
        
        style.configure("Dark.TNotebook",
            background=COULEURS["bg_dark"],
            tabmargins=[2, 5, 2, 0])
        style.configure("Dark.TNotebook.Tab",
            background=COULEURS["bg_card"],
            foreground=COULEURS["text_gray"],
            padding=[15, 8],
            font=("Georgia", 10))
        style.map("Dark.TNotebook.Tab",
            background=[("selected", COULEURS["accent_blue"])],
            foreground=[("selected", COULEURS["text_white"])])

    def _build_ui(self):
        # ── HEADER ──
        header = tk.Frame(self.root, bg=COULEURS["bg_card"], pady=12)
        header.pack(fill=tk.X)
        
        tk.Label(header,
            text="👑  LORD-CREATE",
            bg=COULEURS["bg_card"],
            fg=COULEURS["accent_blue"],
            font=("Georgia", 20, "bold")).pack(side=tk.LEFT, padx=20)
        
        tk.Label(header,
            text="Générateur de Devis Professionnel",
            bg=COULEURS["bg_card"],
            fg=COULEURS["text_gray"],
            font=("Georgia", 11)).pack(side=tk.LEFT, padx=5)
        
        tk.Label(header,
            text=f"v{VERSION}",
            bg=COULEURS["bg_card"],
            fg=COULEURS["text_muted"],
            font=("Georgia", 9)).pack(side=tk.RIGHT, padx=20)
        
        # Ligne séparatrice
        tk.Frame(self.root, bg=COULEURS["accent_blue"], height=2).pack(fill=tk.X)
        
        # ── BODY ──
        body = tk.Frame(self.root, bg=COULEURS["bg_dark"])
        body.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Colonne gauche (formulaire)
        left_col = tk.Frame(body, bg=COULEURS["bg_dark"])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Colonne droite (récap + actions)
        right_col = tk.Frame(body, bg=COULEURS["bg_dark"], width=300)
        right_col.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 0))
        right_col.pack_propagate(False)
        
        # Onglets dans la colonne gauche
        self.notebook = ttk.Notebook(left_col, style="Dark.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1 – Client
        tab_client = tk.Frame(self.notebook, bg=COULEURS["bg_dark"])
        self.notebook.add(tab_client, text="  👤 Client  ")
        self._build_tab_client(tab_client)
        
        # Tab 2 – Offre
        tab_offre = tk.Frame(self.notebook, bg=COULEURS["bg_dark"])
        self.notebook.add(tab_offre, text="  🛠 Offre  ")
        self._build_tab_offre(tab_offre)
        
        # Tab 3 – Conditions
        tab_cond = tk.Frame(self.notebook, bg=COULEURS["bg_dark"])
        self.notebook.add(tab_cond, text="  📋 Conditions  ")
        self._build_tab_conditions(tab_cond)
        
        # Panneau droit
        self._build_right_panel(right_col)

    # ── TAB CLIENT ──────────────────────────────
    def _build_tab_client(self, parent):
        canvas = tk.Canvas(parent, bg=COULEURS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COULEURS["bg_dark"])
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        p = 15
        
        # ── Identité Devis ──
        self._section_card(frame, "📄 Identité du Devis", [
            ("N° Devis", "numero_devis_entry", self.numero_devis, "entry"),
            ("Date d'émission", "date_emission_entry", datetime.now().strftime("%d/%m/%Y"), "entry"),
            ("Date de validité", "date_validite_entry",
             (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y"), "entry"),
        ], p)
        
        # ── Vendeur ──
        self._section_card(frame, "🏢 Votre Entreprise", [
            ("Votre nom / société", "vendeur_nom_entry", "LORD-CREATE", "entry"),
            ("Email", "vendeur_email_entry", "contact@lord-create.com", "entry"),
            ("Téléphone", "vendeur_tel_entry", "+221 77 000 00 00", "entry"),
            ("Adresse", "vendeur_adresse_entry", "Dakar, Sénégal", "entry"),
            ("NINEA / SIRET", "vendeur_ninea_entry", "", "entry"),
        ], p)
        
        # ── Client ──
        self._section_card(frame, "👤 Informations Client", [
            ("Nom complet / Société", "client_nom_entry", "", "entry"),
            ("Email client", "client_email_entry", "", "entry"),
            ("Téléphone", "client_tel_entry", "", "entry"),
            ("Pays", "client_pays_combo", self.pays_var, "combo", PAYS),
            ("Adresse client", "client_adresse_entry", "", "entry"),
            ("Devise du devis", "devise_combo", self.devise_var, "combo", list(DEVISES.keys())),
        ], p)

    # ── TAB OFFRE ───────────────────────────────
    def _build_tab_offre(self, parent):
        canvas = tk.Canvas(parent, bg=COULEURS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.offre_frame = tk.Frame(canvas, bg=COULEURS["bg_dark"])
        
        self.offre_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.offre_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mousewheel
        canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))
        
        p = 15
        
        # Type de site
        card = self._make_card(self.offre_frame, p)
        ttk.Label(card, text="🌍 Type de Site Web", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        
        for site_type in TYPES_SITES:
            info = TYPES_SITES[site_type]
            rb_frame = tk.Frame(card, bg=COULEURS["bg_input"], pady=8, padx=10, cursor="hand2")
            rb_frame.pack(fill=tk.X, pady=3)
            
            rb = tk.Radiobutton(rb_frame,
                text=f"  {site_type}",
                variable=self.site_type_var,
                value=site_type,
                bg=COULEURS["bg_input"],
                fg=COULEURS["text_white"],
                selectcolor=COULEURS["accent_blue"],
                activebackground=COULEURS["bg_input"],
                activeforeground=COULEURS["accent_light"],
                font=("Georgia", 11, "bold"),
                command=self._update_offres)
            rb.pack(side=tk.LEFT)
            
            prix_base = info["base_prix"]
            tk.Label(rb_frame,
                text=f"à partir de {prix_base:,} XOF",
                bg=COULEURS["bg_input"],
                fg=COULEURS["accent_gold"],
                font=("Georgia", 9)).pack(side=tk.RIGHT)
            
            tk.Label(rb_frame,
                text=info["desc"],
                bg=COULEURS["bg_input"],
                fg=COULEURS["text_gray"],
                font=("Georgia", 9)).pack(side=tk.LEFT, padx=5)
        
        # Titre du projet
        card2 = self._make_card(self.offre_frame, p)
        ttk.Label(card2, text="📝 Détail du Projet", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        
        tk.Label(card2, text="Titre du projet",
            bg=COULEURS["bg_card"], fg=COULEURS["text_gray"],
            font=("Georgia", 9)).pack(anchor="w")
        self.projet_titre_entry = tk.Entry(card2,
            bg=COULEURS["bg_input"], fg=COULEURS["text_white"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 11), relief=tk.FLAT, bd=6)
        self.projet_titre_entry.pack(fill=tk.X, pady=(2, 10))
        self.projet_titre_entry.insert(0, "Création de site web professionnel")
        
        tk.Label(card2, text="Description / Cahier des charges",
            bg=COULEURS["bg_card"], fg=COULEURS["text_gray"],
            font=("Georgia", 9)).pack(anchor="w")
        self.projet_desc_text = tk.Text(card2,
            bg=COULEURS["bg_input"], fg=COULEURS["text_white"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 10), relief=tk.FLAT, bd=6,
            height=4, wrap=tk.WORD)
        self.projet_desc_text.pack(fill=tk.X, pady=(2, 10))
        self.projet_desc_text.insert("1.0", "Développement d'un site web sur mesure selon les spécifications du client.")
        
        # Délai
        card3 = self._make_card(self.offre_frame, p)
        ttk.Label(card3, text="⏱ Délai de Livraison", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        delai_combo = ttk.Combobox(card3, textvariable=self.delai_var,
            values=list(DELAIS.keys()), state="readonly",
            style="Dark.TCombobox", font=("Georgia", 10))
        delai_combo.pack(fill=tk.X)
        delai_combo.bind("<<ComboboxSelected>>", lambda e: self._calculer_total())
        
        # ── Options du site (dynamique) ──
        self.options_card = self._make_card(self.offre_frame, p)
        ttk.Label(self.options_card, text="✅ Options & Services Inclus", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        self.options_container = tk.Frame(self.options_card, bg=COULEURS["bg_card"])
        self.options_container.pack(fill=tk.X)
        
        # Prix personnalisé
        card5 = self._make_card(self.offre_frame, p)
        ttk.Label(card5, text="💰 Ajustements Tarifaires", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        
        row_remise = tk.Frame(card5, bg=COULEURS["bg_card"])
        row_remise.pack(fill=tk.X, pady=3)
        tk.Label(row_remise, text="Remise (%)", bg=COULEURS["bg_card"],
            fg=COULEURS["text_gray"], font=("Georgia", 10), width=18, anchor="w").pack(side=tk.LEFT)
        remise_entry = tk.Entry(row_remise, textvariable=self.remise_var,
            bg=COULEURS["bg_input"], fg=COULEURS["accent_gold"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 11), relief=tk.FLAT, bd=6, width=8)
        remise_entry.pack(side=tk.LEFT, padx=5)
        remise_entry.bind("<KeyRelease>", lambda e: self._calculer_total())
        
        row_tva = tk.Frame(card5, bg=COULEURS["bg_card"])
        row_tva.pack(fill=tk.X, pady=3)
        tva_cb = ttk.Checkbutton(row_tva, text="Appliquer la TVA",
            variable=self.tva_var, style="Dark.TCheckbutton",
            command=self._calculer_total)
        tva_cb.pack(side=tk.LEFT)
        tk.Entry(row_tva, textvariable=self.tva_taux_var,
            bg=COULEURS["bg_input"], fg=COULEURS["accent_gold"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 11), relief=tk.FLAT, bd=6, width=5).pack(side=tk.LEFT, padx=5)
        tk.Label(row_tva, text="%", bg=COULEURS["bg_card"],
            fg=COULEURS["text_gray"], font=("Georgia", 10)).pack(side=tk.LEFT)

    # ── TAB CONDITIONS ───────────────────────────
    def _build_tab_conditions(self, parent):
        canvas = tk.Canvas(parent, bg=COULEURS["bg_dark"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COULEURS["bg_dark"])
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        p = 15
        
        # Modalités de paiement
        card1 = self._make_card(frame, p)
        ttk.Label(card1, text="💳 Modalités de Paiement", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        pay_combo = ttk.Combobox(card1, textvariable=self.paiement_var,
            values=STATUT_PAIEMENT, state="readonly",
            style="Dark.TCombobox", font=("Georgia", 10))
        pay_combo.pack(fill=tk.X)
        
        # Conditions générales
        card2 = self._make_card(frame, p)
        ttk.Label(card2, text="📜 Conditions Générales", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.cg_text = tk.Text(card2,
            bg=COULEURS["bg_input"], fg=COULEURS["text_white"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 9), relief=tk.FLAT, bd=6,
            height=10, wrap=tk.WORD)
        self.cg_text.pack(fill=tk.X)
        self.cg_text.insert("1.0", 
            "1. PROPRIÉTÉ INTELLECTUELLE\n"
            "Les droits de propriété intellectuelle sur le site livré sont intégralement transférés au client après règlement complet de la facture.\n\n"
            "2. DÉLAIS\n"
            "Les délais de livraison sont indicatifs et peuvent être révisés en cas de modifications demandées par le client ou de retard dans la fourniture des contenus.\n\n"
            "3. RÉVISIONS\n"
            "Le devis inclut 2 rounds de révisions. Toute modification supplémentaire fera l'objet d'un avenant tarifaire.\n\n"
            "4. HÉBERGEMENT & DOMAINE\n"
            "Sauf mention contraire, l'hébergement et le nom de domaine ne sont pas inclus dans cette offre.\n\n"
            "5. CONFIDENTIALITÉ\n"
            "LORD-CREATE s'engage à ne pas divulguer les informations confidentielles du client à des tiers.\n\n"
            "6. RÉSILIATION\n"
            "En cas d'annulation après démarrage des travaux, l'acompte versé reste acquis à titre d'indemnisation.\n\n"
            "7. GARANTIE\n"
            "Une garantie de correction de bugs est assurée pendant 30 jours après la livraison finale."
        )
        
        # Notes supplémentaires
        card3 = self._make_card(frame, p)
        ttk.Label(card3, text="📝 Notes & Message personnalisé", style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        
        self.notes_text = tk.Text(card3,
            bg=COULEURS["bg_input"], fg=COULEURS["text_white"],
            insertbackground=COULEURS["text_white"],
            font=("Georgia", 10), relief=tk.FLAT, bd=6,
            height=5, wrap=tk.WORD)
        self.notes_text.pack(fill=tk.X)
        self.notes_text.insert("1.0", "Nous vous remercions de votre confiance. N'hésitez pas à nous contacter pour toute question.")

    # ── PANNEAU DROIT ────────────────────────────
    def _build_right_panel(self, parent):
        # Récap total
        recap = tk.Frame(parent, bg=COULEURS["bg_card"], padx=15, pady=15)
        recap.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(recap, text="📊 Récapitulatif", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        
        self.recap_lines_frame = tk.Frame(recap, bg=COULEURS["bg_card"])
        self.recap_lines_frame.pack(fill=tk.X)
        
        # Séparateur
        tk.Frame(recap, bg=COULEURS["border"], height=1).pack(fill=tk.X, pady=10)
        
        # Total
        total_row = tk.Frame(recap, bg=COULEURS["bg_card"])
        total_row.pack(fill=tk.X)
        tk.Label(total_row, text="TOTAL TTC",
            bg=COULEURS["bg_card"], fg=COULEURS["text_white"],
            font=("Georgia", 11, "bold")).pack(side=tk.LEFT)
        self.total_label = tk.Label(total_row, textvariable=self.total_var,
            bg=COULEURS["bg_card"], fg=COULEURS["accent_gold"],
            font=("Georgia", 14, "bold"))
        self.total_label.pack(side=tk.RIGHT)
        
        # Actions
        actions = tk.Frame(parent, bg=COULEURS["bg_dark"])
        actions.pack(fill=tk.X)
        
        def btn(parent, text, color, command):
            b = tk.Button(parent, text=text, bg=color, fg="white",
                font=("Georgia", 10, "bold"), relief=tk.FLAT, cursor="hand2",
                padx=10, pady=8, bd=0, command=command,
                activebackground=color, activeforeground="white")
            b.pack(fill=tk.X, pady=3)
            return b
        
        btn(actions, "📄 Générer Devis PDF", COULEURS["accent_blue"], self._generer_pdf)
        btn(actions, "💾 Sauvegarder (.json)", COULEURS["bg_card"], self._sauvegarder_json)
        btn(actions, "📂 Charger un devis", COULEURS["bg_card"], self._charger_json)
        btn(actions, "🔄 Nouveau Devis", COULEURS["text_muted"], self._nouveau_devis)
        
        # Aperçu infos devis
        info = tk.Frame(parent, bg=COULEURS["bg_card"], padx=12, pady=10)
        info.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(info, text="ℹ️ Infos Devis", style="Section.TLabel").pack(anchor="w", pady=(0, 6))
        
        self.info_lines = []
        for _ in range(5):
            lbl = tk.Label(info, text="", bg=COULEURS["bg_card"],
                fg=COULEURS["text_gray"], font=("Georgia", 9), anchor="w")
            lbl.pack(fill=tk.X)
            self.info_lines.append(lbl)
        
        self._update_info_lines()

    # ── HELPERS ──────────────────────────────────
    def _make_card(self, parent, pad=15):
        outer = tk.Frame(parent, bg=COULEURS["bg_dark"], pady=pad//2, padx=pad)
        outer.pack(fill=tk.X)
        card = tk.Frame(outer, bg=COULEURS["bg_card"], padx=15, pady=12,
            highlightbackground=COULEURS["border"], highlightthickness=1)
        card.pack(fill=tk.X)
        return card

    def _section_card(self, parent, title, fields, pad=15):
        card = self._make_card(parent, pad)
        ttk.Label(card, text=title, style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        
        for item in fields:
            label_text, attr_name, default, field_type, *extras = item
            
            row = tk.Frame(card, bg=COULEURS["bg_card"])
            row.pack(fill=tk.X, pady=3)
            
            tk.Label(row, text=label_text, bg=COULEURS["bg_card"],
                fg=COULEURS["text_gray"], font=("Georgia", 9),
                width=22, anchor="w").pack(side=tk.LEFT)
            
            if field_type == "entry":
                w = tk.Entry(row, bg=COULEURS["bg_input"], fg=COULEURS["text_white"],
                    insertbackground=COULEURS["text_white"],
                    font=("Georgia", 10), relief=tk.FLAT, bd=5)
                w.pack(side=tk.LEFT, fill=tk.X, expand=True)
                w.insert(0, default)
                setattr(self, attr_name, w)
            elif field_type == "combo":
                var = default
                values = extras[0] if extras else []
                w = ttk.Combobox(row, textvariable=var, values=values,
                    state="readonly", style="Dark.TCombobox",
                    font=("Georgia", 10))
                w.pack(side=tk.LEFT, fill=tk.X, expand=True)
                setattr(self, attr_name, w)

    def _update_offres(self):
        # Vider le container
        for w in self.options_container.winfo_children():
            w.destroy()
        self.offres_vars.clear()
        
        site_type = self.site_type_var.get()
        offres = TYPES_SITES[site_type]["offres"]
        
        # Header colonnes
        hdr = tk.Frame(self.options_container, bg=COULEURS["bg_card"])
        hdr.pack(fill=tk.X, pady=(0, 4))
        tk.Label(hdr, text="Service / Option", bg=COULEURS["bg_card"],
            fg=COULEURS["text_muted"], font=("Georgia", 9, "bold"),
            width=35, anchor="w").pack(side=tk.LEFT)
        tk.Label(hdr, text="Prix", bg=COULEURS["bg_card"],
            fg=COULEURS["text_muted"], font=("Georgia", 9, "bold"),
            width=12).pack(side=tk.LEFT)
        tk.Label(hdr, text="Inclus", bg=COULEURS["bg_card"],
            fg=COULEURS["text_muted"], font=("Georgia", 9, "bold")).pack(side=tk.LEFT, padx=10)
        
        tk.Frame(self.options_container, bg=COULEURS["border"], height=1).pack(fill=tk.X, pady=4)
        
        for offre_name, info in offres.items():
            var = tk.BooleanVar(value=info["inclus"])
            self.offres_vars[offre_name] = {"var": var, "prix": info["prix"]}
            
            row = tk.Frame(self.options_container,
                bg=COULEURS["bg_input"] if info["inclus"] else COULEURS["bg_card"],
                pady=2)
            row.pack(fill=tk.X, pady=1)
            
            color_text = COULEURS["success"] if info["inclus"] else COULEURS["text_gray"]
            
            cb = ttk.Checkbutton(row, text=offre_name,
                variable=var, style="Dark.TCheckbutton",
                command=self._calculer_total)
            cb.pack(side=tk.LEFT, padx=4)
            
            prix_text = "Inclus" if info["prix"] == 0 else f"+{info['prix']:,}"
            tk.Label(row, text=prix_text,
                bg=COULEURS["bg_input"] if info["inclus"] else COULEURS["bg_card"],
                fg=COULEURS["accent_gold"] if info["prix"] > 0 else COULEURS["success"],
                font=("Georgia", 9), width=12).pack(side=tk.RIGHT, padx=5)
        
        self._calculer_total()

    def _calculer_total(self):
        site_type = self.site_type_var.get()
        base = TYPES_SITES[site_type]["base_prix"]
        
        options_total = 0
        for offre_name, data in self.offres_vars.items():
            if data["var"].get() and data["prix"] > 0:
                options_total += data["prix"]
        
        sous_total = base + options_total
        
        # Délai
        delai = self.delai_var.get()
        multiplicateur = DELAIS.get(delai, 1.0)
        sous_total_delai = sous_total * multiplicateur
        
        # Remise
        try:
            remise_pct = float(self.remise_var.get() or 0)
        except:
            remise_pct = 0
        remise_montant = sous_total_delai * (remise_pct / 100)
        apres_remise = sous_total_delai - remise_montant
        
        # TVA
        tva_montant = 0
        if self.tva_var.get():
            try:
                taux = float(self.tva_taux_var.get() or 0)
                tva_montant = apres_remise * (taux / 100)
            except:
                pass
        
        total_ttc = apres_remise + tva_montant
        
        # Devise
        devise_full = self.devise_var.get()
        devise_code = DEVISES.get(devise_full, "XOF")
        
        self.total_var.set(f"{total_ttc:,.0f} {devise_code}")
        
        # Update récap
        self._update_recap(base, options_total, sous_total_delai,
                          remise_montant, tva_montant, total_ttc, devise_code)
        self._update_info_lines()

    def _update_recap(self, base, options, sous_total, remise, tva, total, devise):
        for w in self.recap_lines_frame.winfo_children():
            w.destroy()
        
        def ligne(label, montant, color=None):
            row = tk.Frame(self.recap_lines_frame, bg=COULEURS["bg_card"])
            row.pack(fill=tk.X, pady=1)
            tk.Label(row, text=label, bg=COULEURS["bg_card"],
                fg=COULEURS["text_gray"], font=("Georgia", 9)).pack(side=tk.LEFT)
            tk.Label(row, text=f"{montant:,.0f} {devise}",
                bg=COULEURS["bg_card"],
                fg=color or COULEURS["text_white"],
                font=("Georgia", 9)).pack(side=tk.RIGHT)
        
        ligne("Base site", base)
        if options > 0:
            ligne("Options", options, COULEURS["accent_light"])
        if remise > 0:
            ligne(f"Remise ({self.remise_var.get()}%)", -remise, COULEURS["success"])
        if tva > 0:
            try:
                taux = self.tva_taux_var.get()
                ligne(f"TVA ({taux}%)", tva, COULEURS["warning"])
            except:
                pass

    def _update_info_lines(self):
        try:
            lines = [
                f"N° {self.numero_devis_entry.get()}",
                f"Type : {self.site_type_var.get().split(' ', 1)[-1]}",
                f"Délai : {self.delai_var.get().split('(')[0].strip()}",
                f"Paiement : {self.paiement_var.get()[:30]}",
                f"Validité : 30 jours",
            ]
        except:
            lines = ["—"] * 5
        
        for i, lbl in enumerate(self.info_lines):
            lbl.config(text=lines[i] if i < len(lines) else "")

    # ── ACTIONS ──────────────────────────────────
    def _get_devis_data(self):
        offres_selectionnees = {k: v["var"].get() for k, v in self.offres_vars.items()}
        
        return {
            "numero": self.numero_devis_entry.get(),
            "date_emission": self.date_emission_entry.get(),
            "date_validite": self.date_validite_entry.get(),
            "vendeur": {
                "nom": self.vendeur_nom_entry.get(),
                "email": self.vendeur_email_entry.get(),
                "tel": self.vendeur_tel_entry.get(),
                "adresse": self.vendeur_adresse_entry.get(),
                "ninea": self.vendeur_ninea_entry.get(),
            },
            "client": {
                "nom": self.client_nom_entry.get(),
                "email": self.client_email_entry.get(),
                "tel": self.client_tel_entry.get(),
                "pays": self.pays_var.get(),
                "adresse": self.client_adresse_entry.get(),
            },
            "devise": DEVISES.get(self.devise_var.get(), "XOF"),
            "site_type": self.site_type_var.get(),
            "projet_titre": self.projet_titre_entry.get(),
            "projet_desc": self.projet_desc_text.get("1.0", tk.END).strip(),
            "delai": self.delai_var.get(),
            "offres": offres_selectionnees,
            "remise_pct": self.remise_var.get(),
            "tva": self.tva_var.get(),
            "tva_taux": self.tva_taux_var.get(),
            "modalite_paiement": self.paiement_var.get(),
            "conditions": self.cg_text.get("1.0", tk.END).strip(),
            "notes": self.notes_text.get("1.0", tk.END).strip(),
            "total": self.total_var.get(),
        }

    def _generer_pdf(self):
        data = self._get_devis_data()
        if not data["client"]["nom"]:
            messagebox.showwarning("Champ manquant", "Veuillez saisir le nom du client.")
            return
        
        # Générer le HTML puis convertir en PDF
        html = self._generer_html(data)
        
        # Choisir le chemin de sauvegarde
        filename = f"Devis_{data['numero']}_{data['client']['nom'].replace(' ', '_')}.pdf"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("HTML", "*.html")],
            initialfile=filename,
            title="Sauvegarder le devis")
        
        if not filepath:
            return
        
        if filepath.endswith(".html"):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            messagebox.showinfo("✅ Succès", f"Devis HTML sauvegardé :\n{filepath}")
            # Ouvrir dans le navigateur
            try:
                subprocess.Popen(["xdg-open", filepath])
            except:
                pass
        else:
            # Essayer de générer un PDF
            pdf_generated = False
            
            # Méthode 1: weasyprint
            try:
                import weasyprint
                html_path = filepath.replace(".pdf", "_temp.html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html)
                weasyprint.HTML(filename=html_path).write_pdf(filepath)
                os.remove(html_path)
                pdf_generated = True
            except ImportError:
                pass
            except Exception as e:
                pass
            
            # Méthode 2: wkhtmltopdf
            if not pdf_generated:
                try:
                    html_path = filepath.replace(".pdf", "_temp.html")
                    with open(html_path, "w", encoding="utf-8") as f:
                        f.write(html)
                    result = subprocess.run(
                        ["wkhtmltopdf", "--quiet", "--enable-local-file-access", html_path, filepath],
                        capture_output=True, timeout=30)
                    os.remove(html_path)
                    if result.returncode == 0:
                        pdf_generated = True
                except:
                    pass
            
            if pdf_generated:
                messagebox.showinfo("✅ Succès", f"Devis PDF généré :\n{filepath}")
                try:
                    subprocess.Popen(["xdg-open", filepath])
                except:
                    pass
            else:
                # Fallback: sauvegarder en HTML
                html_path = filepath.replace(".pdf", ".html")
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(html)
                messagebox.showinfo("📄 Devis généré (HTML)",
                    f"PDF non disponible (installez weasyprint ou wkhtmltopdf)\n\n"
                    f"Devis sauvegardé en HTML :\n{html_path}\n\n"
                    f"💡 Pour activer le PDF :\n"
                    f"  pip install weasyprint\n"
                    f"  ou: sudo apt install wkhtmltopdf")
                try:
                    subprocess.Popen(["xdg-open", html_path])
                except:
                    pass

    def _generer_html(self, d):
        # Calculs
        site_type = d["site_type"]
        base = TYPES_SITES[site_type]["base_prix"]
        offres_info = TYPES_SITES[site_type]["offres"]
        devise = d["devise"]
        
        # Lignes de détail
        lignes_html = ""
        sous_total_options = 0
        
        for offre_name, selectionnee in d["offres"].items():
            if selectionnee:
                info = offres_info.get(offre_name, {"prix": 0})
                prix = info["prix"]
                sous_total_options += prix
                prix_text = "Inclus" if prix == 0 else f"+{prix:,} {devise}"
                row_class = "inclus" if prix == 0 else "option"
                lignes_html += f"""
                <tr class="{row_class}">
                    <td>✓ {offre_name}</td>
                    <td class="montant">{prix_text}</td>
                </tr>"""
        
        sous_total = base + sous_total_options
        
        # Délai
        multiplicateur = DELAIS.get(d["delai"], 1.0)
        sous_total_delai = sous_total * multiplicateur
        
        try:
            remise_pct = float(d["remise_pct"] or 0)
        except:
            remise_pct = 0
        remise_montant = sous_total_delai * (remise_pct / 100)
        apres_remise = sous_total_delai - remise_montant
        
        tva_montant = 0
        if d["tva"]:
            try:
                taux = float(d["tva_taux"] or 0)
                tva_montant = apres_remise * (taux / 100)
            except:
                pass
        
        total_ttc = apres_remise + tva_montant
        
        # Lignes totaux
        totaux_html = f"""
        <tr class="base-row">
            <td>Base {site_type}</td>
            <td class="montant">{base:,} {devise}</td>
        </tr>"""
        
        if sous_total_options > 0:
            totaux_html += f"""
        <tr>
            <td>Total options</td>
            <td class="montant">+{sous_total_options:,} {devise}</td>
        </tr>"""
        
        if multiplicateur != 1.0:
            pct_text = f"+{int((multiplicateur-1)*100)}%" if multiplicateur > 1 else f"{int((multiplicateur-1)*100)}%"
            totaux_html += f"""
        <tr>
            <td>Ajustement délai ({pct_text})</td>
            <td class="montant">{(sous_total_delai - sous_total):+,.0f} {devise}</td>
        </tr>"""
        
        if remise_pct > 0:
            totaux_html += f"""
        <tr class="remise-row">
            <td>Remise commerciale ({remise_pct}%)</td>
            <td class="montant">-{remise_montant:,.0f} {devise}</td>
        </tr>"""
        
        totaux_html += f"""
        <tr class="ht-row">
            <td>Sous-total HT</td>
            <td class="montant">{apres_remise:,.0f} {devise}</td>
        </tr>"""
        
        if tva_montant > 0:
            totaux_html += f"""
        <tr>
            <td>TVA ({d['tva_taux']}%)</td>
            <td class="montant">+{tva_montant:,.0f} {devise}</td>
        </tr>"""
        
        # Conditions HTML
        conditions_html = d["conditions"].replace("\n", "<br>")
        notes_html = d["notes"].replace("\n", "<br>")
        
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Devis {d['numero']} — {d['vendeur']['nom']}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@300;400;600&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Source Sans 3', 'Georgia', serif;
            background: #f8f9fc;
            color: #1a2035;
            font-size: 13px;
            line-height: 1.6;
        }}
        
        .page {{
            max-width: 900px;
            margin: 20px auto;
            background: white;
            box-shadow: 0 4px 40px rgba(0,0,0,0.12);
        }}
        
        /* HEADER */
        .header {{
            background: linear-gradient(135deg, #0D1B2A 0%, #162032 50%, #1a2a4a 100%);
            color: white;
            padding: 40px 50px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        
        .logo-zone h1 {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 28px;
            color: #EEF2FF;
            letter-spacing: 1px;
        }}
        
        .logo-zone .crown {{
            font-size: 36px;
            display: block;
            margin-bottom: 5px;
        }}
        
        .logo-zone .tagline {{
            color: #6B8FF0;
            font-size: 11px;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-top: 3px;
        }}
        
        .header-right {{
            text-align: right;
        }}
        
        .devis-badge {{
            background: #3B63E8;
            color: white;
            padding: 6px 20px;
            font-size: 11px;
            letter-spacing: 3px;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 10px;
            display: inline-block;
        }}
        
        .devis-num {{
            color: #F0B429;
            font-size: 22px;
            font-family: 'Playfair Display', Georgia, serif;
            font-weight: 700;
        }}
        
        .devis-dates {{
            color: #8B9EC7;
            font-size: 11px;
            margin-top: 5px;
            line-height: 1.8;
        }}
        
        /* PARTIES */
        .parties {{
            display: flex;
            gap: 0;
            border-bottom: 3px solid #3B63E8;
        }}
        
        .partie {{
            flex: 1;
            padding: 25px 35px;
        }}
        
        .partie:first-child {{
            background: #f8f9fc;
            border-right: 1px solid #e0e6f0;
        }}
        
        .partie-label {{
            font-size: 9px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #3B63E8;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .partie-nom {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 18px;
            font-weight: 700;
            color: #0D1B2A;
            margin-bottom: 6px;
        }}
        
        .partie-info {{
            color: #4A5A7A;
            font-size: 12px;
            line-height: 1.7;
        }}
        
        /* PROJET */
        .projet-banner {{
            background: linear-gradient(90deg, #0D1B2A, #1a3060);
            color: white;
            padding: 18px 50px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .projet-type {{
            background: #3B63E8;
            color: white;
            padding: 4px 14px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            white-space: nowrap;
        }}
        
        .projet-titre {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 18px;
            font-weight: 700;
        }}
        
        .projet-delai {{
            margin-left: auto;
            text-align: right;
            color: #F0B429;
            font-size: 11px;
        }}
        
        /* SECTION */
        .section {{
            padding: 30px 50px;
            border-bottom: 1px solid #e8edf5;
        }}
        
        .section-title {{
            font-size: 10px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #3B63E8;
            font-weight: 700;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e8edf5;
        }}
        
        /* TABLEAU OFFRES */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead th {{
            background: #0D1B2A;
            color: #8B9EC7;
            font-size: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
            padding: 10px 15px;
            text-align: left;
        }}
        
        thead th.montant, td.montant {{
            text-align: right;
            width: 180px;
        }}
        
        tbody tr td {{
            padding: 9px 15px;
            border-bottom: 1px solid #f0f3f9;
        }}
        
        tr.inclus td {{ background: #f0fff4; color: #166534; }}
        tr.inclus td.montant {{ color: #22C55E; font-weight: 600; }}
        tr.option td {{ color: #1a2035; }}
        tr.option td.montant {{ color: #3B63E8; font-weight: 600; }}
        
        /* TOTAUX */
        .totaux-section {{
            padding: 25px 50px;
            background: #f8f9fc;
        }}
        
        .totaux-table {{
            width: 380px;
            margin-left: auto;
        }}
        
        .totaux-table td {{
            padding: 7px 10px;
            font-size: 12px;
        }}
        
        tr.base-row td {{ color: #4A5A7A; }}
        tr.ht-row td {{ font-weight: 700; border-top: 2px solid #dde3f0; padding-top: 10px; }}
        tr.remise-row td {{ color: #22C55E; }}
        
        .total-final {{
            background: linear-gradient(135deg, #0D1B2A, #1a3060);
            color: white;
            margin: 0 50px;
            padding: 20px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .total-label {{
            font-size: 11px;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #8B9EC7;
        }}
        
        .total-montant {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 28px;
            font-weight: 700;
            color: #F0B429;
        }}
        
        /* PAIEMENT */
        .paiement-badge {{
            display: inline-block;
            background: #EFF6FF;
            color: #3B63E8;
            border: 1px solid #BFDBFE;
            padding: 8px 18px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 8px;
        }}
        
        /* CONDITIONS */
        .conditions-text {{
            font-size: 11px;
            color: #4A5A7A;
            line-height: 1.8;
            background: #f8f9fc;
            padding: 20px;
            border-left: 4px solid #3B63E8;
        }}
        
        .notes-text {{
            font-size: 12px;
            color: #1a2035;
            font-style: italic;
            background: #fffbeb;
            padding: 15px 20px;
            border-left: 4px solid #F0B429;
            margin-top: 15px;
        }}
        
        /* FOOTER */
        .footer {{
            background: #0D1B2A;
            color: #4A5A7A;
            text-align: center;
            padding: 20px;
            font-size: 10px;
            letter-spacing: 1px;
        }}
        
        .footer strong {{ color: #6B8FF0; }}
        
        @media print {{
            body {{ background: white; }}
            .page {{ box-shadow: none; margin: 0; }}
        }}
    </style>
</head>
<body>
<div class="page">

    <!-- HEADER -->
    <div class="header">
        <div class="logo-zone">
            <span class="crown">👑</span>
            <h1>LORD-CRÉATE</h1>
            <div class="tagline">Code With Royalty</div>
        </div>
        <div class="header-right">
            <div class="devis-badge">Devis</div>
            <div class="devis-num">{d['numero']}</div>
            <div class="devis-dates">
                Émis le : <strong>{d['date_emission']}</strong><br>
                Valide jusqu'au : <strong>{d['date_validite']}</strong>
            </div>
        </div>
    </div>

    <!-- PARTIES -->
    <div class="parties">
        <div class="partie">
            <div class="partie-label">Prestataire</div>
            <div class="partie-nom">{d['vendeur']['nom']}</div>
            <div class="partie-info">
                {d['vendeur']['email']}<br>
                {d['vendeur']['tel']}<br>
                {d['vendeur']['adresse']}
                {f'<br>NINEA : {d["vendeur"]["ninea"]}' if d['vendeur']['ninea'] else ''}
            </div>
        </div>
        <div class="partie">
            <div class="partie-label">Client</div>
            <div class="partie-nom">{d['client']['nom'] or '—'}</div>
            <div class="partie-info">
                {d['client']['email'] or ''}<br>
                {d['client']['tel'] or ''}<br>
                {d['client']['adresse'] or ''}<br>
                {d['client']['pays']}
            </div>
        </div>
    </div>

    <!-- PROJET -->
    <div class="projet-banner">
        <div class="projet-type">{site_type}</div>
        <div class="projet-titre">{d['projet_titre']}</div>
        <div class="projet-delai">⏱ {d['delai'].split('(')[0].strip()}</div>
    </div>
    
    {f'<div class="section"><p style="color:#4A5A7A;font-size:12px;">{d["projet_desc"]}</p></div>' if d['projet_desc'] else ''}

    <!-- DÉTAIL OFFRE -->
    <div class="section">
        <div class="section-title">Détail des prestations</div>
        <table>
            <thead>
                <tr>
                    <th>Service / Option inclus(e)</th>
                    <th class="montant">Tarif</th>
                </tr>
            </thead>
            <tbody>
                {lignes_html}
            </tbody>
        </table>
    </div>

    <!-- TOTAUX -->
    <div class="totaux-section">
        <table class="totaux-table">
            {totaux_html}
        </table>
    </div>
    
    <div class="total-final">
        <div>
            <div class="total-label">Montant Total TTC</div>
            <div style="color:#8B9EC7;font-size:11px;margin-top:3px;">Devise : {devise}</div>
        </div>
        <div class="total-montant">{total_ttc:,.0f} {devise}</div>
    </div>

    <!-- PAIEMENT -->
    <div class="section">
        <div class="section-title">Modalités de paiement</div>
        <div class="paiement-badge">💳 {d['modalite_paiement']}</div>
    </div>

    <!-- CONDITIONS -->
    <div class="section">
        <div class="section-title">Conditions Générales</div>
        <div class="conditions-text">{conditions_html}</div>
        {f'<div class="notes-text">{notes_html}</div>' if d['notes'] else ''}
    </div>

    <!-- SIGNATURE -->
    <div class="section">
        <div class="section-title">Signatures</div>
        <div style="display:flex;gap:60px;margin-top:10px;">
            <div style="flex:1;text-align:center;">
                <div style="border-bottom:2px solid #dde3f0;height:60px;margin-bottom:10px;"></div>
                <div style="color:#4A5A7A;font-size:11px;">Signature & tampon Prestataire<br><strong>{d['vendeur']['nom']}</strong></div>
            </div>
            <div style="flex:1;text-align:center;">
                <div style="border-bottom:2px solid #dde3f0;height:60px;margin-bottom:10px;"></div>
                <div style="color:#4A5A7A;font-size:11px;">Signature client (Bon pour accord)<br><strong>{d['client']['nom'] or 'Client'}</strong></div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <div class="footer">
        <strong>LORD-CRÉATE</strong> — Code With Royalty &nbsp;|&nbsp;
        {d['vendeur']['email']} &nbsp;|&nbsp; {d['vendeur']['tel']}<br>
        Devis généré le {datetime.now().strftime("%d/%m/%Y à %H:%M")} — {d['numero']}
    </div>

</div>
</body>
</html>"""

    def _sauvegarder_json(self):
        data = self._get_devis_data()
        filename = f"devis_{data['numero']}.json"
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile=filename)
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("✅ Sauvegardé", f"Devis sauvegardé :\n{filepath}")

    def _charger_json(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")],
            title="Charger un devis")
        if not filepath:
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._remplir_depuis_data(data)
            messagebox.showinfo("✅ Chargé", f"Devis chargé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger : {e}")

    def _remplir_depuis_data(self, d):
        def safe_set(widget, value):
            try:
                if isinstance(widget, tk.Entry):
                    widget.delete(0, tk.END)
                    widget.insert(0, value or "")
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                    widget.insert("1.0", value or "")
                elif isinstance(widget, ttk.Combobox):
                    widget.set(value or "")
            except:
                pass
        
        safe_set(self.numero_devis_entry, d.get("numero", ""))
        safe_set(self.date_emission_entry, d.get("date_emission", ""))
        safe_set(self.date_validite_entry, d.get("date_validite", ""))
        
        v = d.get("vendeur", {})
        safe_set(self.vendeur_nom_entry, v.get("nom", ""))
        safe_set(self.vendeur_email_entry, v.get("email", ""))
        safe_set(self.vendeur_tel_entry, v.get("tel", ""))
        safe_set(self.vendeur_adresse_entry, v.get("adresse", ""))
        safe_set(self.vendeur_ninea_entry, v.get("ninea", ""))
        
        c = d.get("client", {})
        safe_set(self.client_nom_entry, c.get("nom", ""))
        safe_set(self.client_email_entry, c.get("email", ""))
        safe_set(self.client_tel_entry, c.get("tel", ""))
        safe_set(self.client_adresse_entry, c.get("adresse", ""))
        self.pays_var.set(c.get("pays", "Sénégal"))
        
        # Devise
        for full, code in DEVISES.items():
            if code == d.get("devise"):
                self.devise_var.set(full)
                break
        
        self.site_type_var.set(d.get("site_type", list(TYPES_SITES.keys())[0]))
        
        safe_set(self.projet_titre_entry, d.get("projet_titre", ""))
        safe_set(self.projet_desc_text, d.get("projet_desc", ""))
        self.delai_var.set(d.get("delai", list(DELAIS.keys())[2]))
        self.remise_var.set(d.get("remise_pct", "0"))
        self.tva_var.set(d.get("tva", False))
        self.tva_taux_var.set(d.get("tva_taux", "18"))
        self.paiement_var.set(d.get("modalite_paiement", STATUT_PAIEMENT[1]))
        safe_set(self.cg_text, d.get("conditions", ""))
        safe_set(self.notes_text, d.get("notes", ""))
        
        self._update_offres()
        
        # Restaurer offres cochées
        offres_sauvées = d.get("offres", {})
        for nom, var_data in self.offres_vars.items():
            if nom in offres_sauvées:
                var_data["var"].set(offres_sauvées[nom])
        
        self._calculer_total()

    def _nouveau_devis(self):
        if messagebox.askyesno("Nouveau devis", "Effacer le devis actuel et en créer un nouveau ?"):
            self.numero_devis = self._generer_numero()
            self.__init__(self.root)


# ─────────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────────

def main():
    root = tk.Tk()
    
    # Icône si dispo
    try:
        root.iconbitmap("@/usr/share/pixmaps/python3.xbm")
    except:
        pass
    
    app = LordCreateApp(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    w, h = 1200, 800
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
