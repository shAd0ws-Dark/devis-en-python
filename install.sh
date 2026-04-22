#!/bin/bash
# ─────────────────────────────────────────────
# LORD-CREATE — Script d'installation Kali Linux
# ─────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BLUE}${BOLD}"
echo "  ██╗      ██████╗ ██████╗ ██████╗      ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗"
echo "  ██║     ██╔═══██╗██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝"
echo "  ██║     ██║   ██║██████╔╝██║  ██║    ██║     ██████╔╝█████╗  ███████║   ██║   █████╗  "
echo "  ██║     ██║   ██║██╔══██╗██║  ██║    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  "
echo "  ███████╗╚██████╔╝██║  ██║██████╔╝    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗"
echo "  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝      ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝"
echo -e "${NC}"
echo -e "  ${YELLOW}👑 Générateur de Devis Professionnel — Installation${NC}"
echo ""

INSTALL_DIR="$HOME/.lord-create"
SCRIPT_NAME="lord_create_devis.py"
SCRIPT_SRC="$(dirname "$0")/$SCRIPT_NAME"

echo -e "${CYAN}[1/5]${NC} Vérification des dépendances Python..."

# Vérifier Python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python3 non trouvé. Installation...${NC}"
    sudo apt-get install -y python3 python3-pip python3-tk
else
    echo -e "${GREEN}✓ Python3 $(python3 --version | cut -d' ' -f2) trouvé${NC}"
fi

# Vérifier tkinter
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}→ Installation de python3-tk...${NC}"
    sudo apt-get install -y python3-tk
fi
echo -e "${GREEN}✓ tkinter disponible${NC}"

echo ""
echo -e "${CYAN}[2/5]${NC} Installation de WeasyPrint pour export PDF..."
pip3 install weasyprint --break-system-packages 2>/dev/null || pip install weasyprint 2>/dev/null
if python3 -c "import weasyprint" 2>/dev/null; then
    echo -e "${GREEN}✓ WeasyPrint installé${NC}"
else
    echo -e "${YELLOW}⚠ WeasyPrint non disponible, fallback HTML activé${NC}"
    echo -e "  ${YELLOW}Pour activer le PDF : pip3 install weasyprint${NC}"
fi

echo ""
echo -e "${CYAN}[3/5]${NC} Création du répertoire d'installation..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/devis"

# Copier le script principal
if [ -f "$SCRIPT_SRC" ]; then
    cp "$SCRIPT_SRC" "$INSTALL_DIR/"
    echo -e "${GREEN}✓ Application copiée dans $INSTALL_DIR${NC}"
else
    echo -e "${RED}✗ Fichier source non trouvé : $SCRIPT_SRC${NC}"
    echo -e "  Assurez-vous que lord_create_devis.py est dans le même dossier."
    exit 1
fi

echo ""
echo -e "${CYAN}[4/5]${NC} Création du lanceur..."

# Créer le script de lancement
cat > "$INSTALL_DIR/launch.sh" << 'EOF'
#!/bin/bash
cd "$HOME/.lord-create"
python3 lord_create_devis.py
EOF
chmod +x "$INSTALL_DIR/launch.sh"

# Créer alias dans .bashrc / .zshrc
ALIAS_CMD='alias lord-create="$HOME/.lord-create/launch.sh"'

for rcfile in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rcfile" ]; then
        if ! grep -q "lord-create" "$rcfile"; then
            echo "" >> "$rcfile"
            echo "# LORD-CREATE Devis Generator" >> "$rcfile"
            echo "$ALIAS_CMD" >> "$rcfile"
            echo -e "${GREEN}✓ Alias ajouté dans $rcfile${NC}"
        fi
    fi
done

# Créer un lanceur .desktop (menu graphique)
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_DIR/lord-create.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=LORD-CREATE Devis
Comment=Générateur de Devis Professionnel pour Sites Web
Exec=python3 $INSTALL_DIR/lord_create_devis.py
Icon=applications-internet
Terminal=false
Categories=Office;Finance;
StartupNotify=true
EOF
chmod +x "$DESKTOP_DIR/lord-create.desktop"
echo -e "${GREEN}✓ Lanceur desktop créé${NC}"

echo ""
echo -e "${CYAN}[5/5]${NC} Installation terminée !"
echo ""
echo -e "${GREEN}${BOLD}════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  ✅ LORD-CREATE installé avec succès !  ${NC}"
echo -e "${GREEN}${BOLD}════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BOLD}Lancer l'application :${NC}"
echo -e "  ${CYAN}→ Terminal :${NC}  lord-create  (après redémarrage terminal)"
echo -e "  ${CYAN}→ Direct :${NC}    python3 $INSTALL_DIR/lord_create_devis.py"
echo -e "  ${CYAN}→ Menu :${NC}      Chercher 'LORD-CREATE' dans le menu apps"
echo ""
echo -e "  ${BOLD}Répertoire des devis :${NC} $INSTALL_DIR/devis/"
echo ""

# Proposer de lancer maintenant
read -p "  Lancer l'application maintenant ? [O/n] " response
if [[ "$response" =~ ^[Nn]$ ]]; then
    echo -e "\n  ${YELLOW}À bientôt ! 👑${NC}\n"
else
    echo -e "\n  ${BLUE}Lancement de LORD-CREATE...${NC}\n"
    python3 "$INSTALL_DIR/lord_create_devis.py"
fi
