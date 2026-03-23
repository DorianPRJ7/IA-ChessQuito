import tkinter as tk
import os
from PIL import Image, ImageTk

# === On importe TES fonctions (aucune logique réécrite) ===
from main_chessQuitto_alpha_beta import (
    creer_pieces, coups_possibles_placements, placer_piece_placement,
    valMaxPlacement, valMaxJeu, jouer_coup, deplacements_possibles,
    roi_en_echec, calcul_score_plateau, determiner_victoire,
    determiner_tour_placement, verifierFinPartie
)

# ----- Constantes plateau -----
COLS, ROWS, N = ['A', 'B', 'C', 'D'], ['1', '2', '3', '4'], 4
TYPE_MAP = {'RR': 'king', 'R': 'queen', 'RP': 'pawn', 'T': 'rook', 'F': 'bishop', 'C': 'knight'}

def new_board():
    return [['.' for _ in range(N)] for __ in range(N)]

def pos_to_str(i, j):  # (ligne, col) -> "B3"
    return f"{COLS[j]}{ROWS[i]}"

def str_to_pos(p):     # "B3" -> (2,1)
    c, r = p[0], p[1]
    return ROWS.index(r), COLS.index(c)

def traduire_mode_en_string(mode_int):
    if mode_int==1 :
        return "Reine"
    elif mode_int==2 :
        return "Reine-Pion"
    elif mode_int==3 :
        return "Reine-Roi"
    else :
        return "Inconnu"

def traduire_mode_en_int(mode_string):
    if mode_string == "Reine" :
        return 1
    elif mode_string == "Reine-Pion" :
        return 2
    elif mode_string == "Reine-Roi" :
        return 3
    else :
        return -1


class ChessQuittoUI(tk.Tk):
    """
    UI minimaliste Canvas-only :
      - Zone gauche : plateau + entêtes A..D / 1..4
      - Panneau droit : infos + barre de pièces à placer
      - Overlays Canvas : menu de départ, fin de partie
    """
    def __init__(self):
        super().__init__()
        self.title("IA ChessQuito")
        self._center_window(520, 320)  # menu compact au démarrage
        self.minsize(520, 320)
        self.configure(bg="#0D1117")

        self.colors = {
            # Fond et panneaux
            "bg": "#D9DDE2",  # fond général clair-gris
            "panel": "#E2E6EB",  # panneau droit légèrement plus clair
            "panel2": "#D3D8DE",  # fond de la zone plateau
            # Textes
            "text": "#22262B",  # texte principal gris foncé
            "muted": "#5F6772",  # texte secondaire
            # Accents / statuts
            "accent": "#4F7DAA",  # bleu-gris désaturé, élégant
            "good": "#4BAE77",
            "warn": "#D05E5E",
            # Échiquier
            "sq_light": "#C7CCD3",  # case claire gris perle
            "sq_dark": "#B3BAC2",  # case foncée gris acier
            "hint": "#B7D0B7",  # surbrillance douce des coups
            "grid": "#AEB5BC",  # filet discret
            # Chips / badges
            "chip_bg": "#CBD1D8",
            "chip_fg": "#1E2329",
            # Boutons
            "btn": "#C5CBD3",
            "btn_active": "#B6BCC5",
            # Rouge coup précédent
            "red_move": "#EBC3BE",
        }

        # ---- Mise en page ----
        self.margin = 16
        self.sidebar_w = 340  # un peu plus large pour garantir aucune superposition

        # Canvas
        self.cv = tk.Canvas(self, bg=self.colors["bg"], highlightthickness=0, bd=0)
        self.cv.pack(fill=tk.BOTH, expand=True)
        self.bind("<Configure>", self._on_resize)

        # Debounce resize + toast system + shortcuts
        self._resize_after = None
        self.toast_text = None
        self._toast_job = None

        # Raccourcis clavier
        self.bind("<Escape>", lambda e: self._cancel_selection())
        self.bind("<r>",      lambda e: self._restart_same_settings())
        self.bind("<m>",      lambda e: self._show_menu())

        # ---- Board metrics (seront recalculés) ----
        self.CELL = 110
        self.TOP_LABEL = 28
        self.LEFT_LABEL = 28
        self.img_cache = {}
        self.stock_btn_imgs = {}

        # ---- Etat partie ----
        self.mode = 3
        self.human_color = 'BLANCS'
        self.ia_color = 'NOIRS'
        self.board = new_board()
        self.placement = True
        self.sans_prise = 0
        self.turn = 'BLANCS'
        self.moves_played = 0

        # Stocks / sélections
        self.stock_h, self.stock_ia = [], []
        self.sel_place_piece = None
        self.sel_from = None
        self.hints = set()
        self.last_move = None

        # Overlays
        self.overlay = None
        # >>> mode par défaut = "1" (fix)
        self.menu_vals = {"mode": tk.StringVar(value="Reine"), "color": tk.StringVar(value="BLANCS")}
        self.end_info = {"title": "", "details": ""}

        # Events
        self.cv.bind("<Button-1>", self._on_click)

        # Démarrage : écran Menu
        self._draw_all()
        self._show_menu()
        # Centrage utilitaire

    def _center_window(self, width, height):
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    # ===================== Dessin global =====================
    def _on_resize(self, _):
        # Debounce: évite de redessiner trop souvent pendant un redimensionnement
        if self._resize_after is not None:
            try:
                self.after_cancel(self._resize_after)
            except Exception:
                pass
        self._resize_after = self.after(40, self._draw_all)

    def _cancel_selection(self):
        self.sel_from = None
        self.sel_place_piece = None
        self.hints.clear()
        self._draw_all()

    def _show_toast(self, text, ms=5000):
        self.toast_text = text
        if self._toast_job is not None:
            try:
                self.after_cancel(self._toast_job)
            except Exception:
                pass
        # auto-clear
        self._toast_job = self.after(ms, self._clear_toast)

    def _clear_toast(self):
        self.toast_text = None
        self._toast_job = None
        self._draw_all()

    def _draw_all(self):
        self.cv.delete("all")
        W = self.cv.winfo_width()
        H = self.cv.winfo_height()
        M = self.margin
        side_x0 = W - self.sidebar_w - M

        # panneaux
        self._rect(M, M, side_x0 - M, H - M, self.colors["panel2"])  # gauche
        self._rect(side_x0, M, W - M, H - M, self.colors["panel"])   # droite

        # Titre
        self._text(M + 10, M + 10, "IA ChessQuito", 18, weight="bold")

        # ---- Calcul d'emprise pour le plateau (sans chevauchement) ----
        # Espace disponible dans la zone gauche
        left_inner_w = (side_x0 - M) - (M)
        left_inner_h = (H - M) - (M) - 40

        # On réserve explicitement l'espace des entêtes (labels) :
        #  - LEFT_LABEL à gauche, TOP_LABEL en haut
        #  - un petit padding interne de 8 px
        avail_w = max(100, left_inner_w - self.LEFT_LABEL - 8)
        avail_h = max(100, left_inner_h - self.TOP_LABEL - 8)

        # Taille cellule bornée pour que N*CELL tienne dans avail_w/avail_h
        self.CELL = max(70, min(avail_w // N, avail_h // N))

        # Dimensions finales du plateau (damier seul, hors entêtes)
        self.BOARD_W = self.CELL * N
        self.BOARD_H = self.CELL * N

        # Position : plateau centré dans le panneau gauche avec marges égales
        left_x0 = M
        left_x1 = side_x0 - M
        left_w  = left_x1 - left_x0
        content_w = self.LEFT_LABEL + self.BOARD_W
        self.board_x0 = left_x0 + max(0, (left_w - content_w) // 2)
        self.board_y0 = M + 40  # sous le titre

        # Dessins
        self._draw_board()
        self._draw_sidebar()

        # Overlays
        if self.overlay == "menu":
            self._draw_menu_overlay()
        elif self.overlay == "end":
            self._draw_end_overlay()

    # ===================== Primitives dessin =====================
    def _rect(self, x0, y0, x1, y1, fill, r=0, outline=None, ow=1):
        self.cv.create_rectangle(x0, y0, x1, y1, fill=fill, outline=outline or fill, width=ow)

    def _text(self, x, y, txt, size=12, fill=None, anchor="nw",
              weight="normal", width=None, justify="left"):
        f = ("SF Pro Text", size, weight)
        return self.cv.create_text(
            x, y, text=txt,
            fill=fill or self.colors["text"],
            anchor=anchor, font=f,
            width=width, justify=justify
        )

    def _pill(self, x, y, txt, pad=(10,4), bg=None, fg=None, center=False):
        bg = bg or self.colors["chip_bg"]
        fg = fg or self.colors["chip_fg"]
        # Mesure du texte pour connaître la largeur totale du pill
        w = self.cv.create_text(0, 0, text=txt, font=("SF Pro Text", 10, "bold"))
        bbox = self.cv.bbox(w)
        self.cv.delete(w)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        total_w = tw + 2*pad[0]
        total_h = th + 2*pad[1]
        # Si center=True, x est interprété comme l'abscisse du centre du pill
        if center:
            x0 = int(x - total_w/2)
        else:
            x0 = x
        y0 = y
        rect = self.cv.create_rectangle(x0, y0, x0 + total_w, y0 + total_h,
                                        fill=bg, outline=bg)
        self.cv.create_text(x0 + pad[0], y0 + pad[1], text=txt, fill=fg,
                            anchor="nw", font=("SF Pro Text", 10, "bold"))
        return rect


    def _material_diff(self):
        """
        Renvoie l'écart matériel du point de vue du joueur humain.
        > 0 : avantage humain, < 0 : avantage IA.
        """
        b, n = calcul_score_plateau(self.board)  # BLANCS = b, NOIRS = n
        if self.human_color == 'BLANCS':
            return b - n
        else:
            return n - b

    def _draw_possession_bar(self, x, y, w, h):
        """Barre BLANCS/NOIRS proportionnelle au matériel actuel."""
        # Scores bruts
        b, n = calcul_score_plateau(self.board)
        total = max(1, b + n)
        frac_b = b / total
        frac_n = n / total

        # Cadre
        self.cv.create_rectangle(x, y, x + w, y + h,
                                 outline=self.colors["grid"], fill=self.colors["panel"])  # fond discret

        # Segment BLANCS (gauche)
        wb = int(w * frac_b)
        if wb > 0:
            self.cv.create_rectangle(x, y, x + wb, y + h, outline="", fill="#FFFFFF")
        # Segment NOIRS (droite)
        wn = w - wb
        if wn > 0:
            self.cv.create_rectangle(x + wb, y, x + w, y + h, outline="", fill="#000000")

        # Légende centrée (pour rester lisible sur fond mixte)
        pct_b = int(round(frac_b * 100))
        pct_n = 100 - pct_b
        txt = f"BLANCS {pct_b}%  |  NOIRS {pct_n}%"
        self.cv.create_text(x + w/2, y + h/2, text=txt,
                            fill="#4F7DAA", anchor="c", font=("SF Pro Text", 10, "bold"))

    def _show_possession_tooltip(self):
        """Affiche un toast avec les scores exacts BLANCS/NOIRS et les pourcentages."""
        b, n = calcul_score_plateau(self.board)
        total = max(1, b + n)
        pct_b = int(round((b / total) * 100))
        pct_n = 100 - pct_b
        self._show_toast(f"BLANCS: {b}  |  NOIRS: {n}   •   {pct_b}% / {pct_n}%")

    # ===================== Plateau =====================
    def _draw_board(self):
        x0 = self.board_x0
        y0 = self.board_y0

        # entêtes colonnes (A..D)
        for j, col in enumerate(COLS):
            cx = x0 + self.LEFT_LABEL + j*self.CELL + self.CELL//2
            cy = y0 + self.TOP_LABEL//2
            self._text(cx, cy, col, 12, self.colors["muted"], anchor="center", weight="bold")

        # entêtes lignes (1..4)
        for i, row in enumerate(ROWS):
            cx = x0 + self.LEFT_LABEL//2
            cy = y0 + self.TOP_LABEL + i*self.CELL + self.CELL//2
            self._text(cx, cy, row, 12, self.colors["muted"], anchor="center", weight="bold")

        # damier + pièces
        for i in range(N):
            for j in range(N):
                sx = x0 + self.LEFT_LABEL + j*self.CELL
                sy = y0 + self.TOP_LABEL + i*self.CELL
                ex, ey = sx + self.CELL, sy + self.CELL
                base = self.colors["hint"] if (i, j) in self.hints else (
                    self.colors["sq_light"] if (i + j) % 2 == 0 else self.colors["sq_dark"]
                )
                self.cv.create_rectangle(sx, sy, ex, ey, fill=base, outline=self.colors["grid"], width=1)
                if self.last_move:
                    (ls_i, ls_j), (ld_i, ld_j) = self.last_move
                    if (i, j) in [(ls_i, ls_j), (ld_i, ld_j)]:
                        self.cv.create_rectangle(
                            sx, sy, ex, ey,
                            fill=self.colors["red_move"],
                            outline=self.colors["grid"], width=1
                        )
                code = self.board[i][j]
                if code != '.':
                    img = self._img(code, self.CELL - 18)
                    if img is not None:
                        self.cv.create_image((sx + ex)//2, (sy + ey)//2, image=img)
                    else:
                        self._text((sx + ex)//2, (sy + ey)//2, code, 16, anchor="center", weight="bold")
                # Surbrillance des coups autorisés et de la sélection
                if (i, j) in self.hints:
                    self.cv.create_rectangle(sx+2, sy+2, ex-2, ey-2, outline=self.colors["good"], width=2)
                if self.sel_from == (i, j):
                    self.cv.create_rectangle(sx+3, sy+3, ex-3, ey-3, outline=self.colors["accent"], width=3)

    def _img(self, code, size):
        try:
            color = "white" if code[0] == 'B' else "black"
            t = TYPE_MAP[code[1:]]
            key = (t, color, size)
            if key in self.img_cache:
                return self.img_cache[key]
            # Préfère PNG (transparence), fallback JPG si absent
            for ext in ("png", "jpg", "jpeg"):
                path = f"assets/pieces/{t}_{color}.{ext}"
                try:
                    im = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
                    tkimg = ImageTk.PhotoImage(im)
                    self.img_cache[key] = tkimg
                    return tkimg
                except Exception:
                    continue
            return None
        except Exception:
            return None

    # ===================== Sidebar =====================
    def _draw_sidebar(self):
        W = self.cv.winfo_width()
        H = self.cv.winfo_height()
        M = self.margin
        x0 = W - self.sidebar_w - M
        y0 = M

        self._text(x0 + 16, y0 + 12, "Partie", 16, weight="bold")
        y = y0 + 44

        self._pill(x0 + 16, y, f"Mode {traduire_mode_en_string(self.mode)}"); y += 32

        self._pill(x0 + 16, y, f"Vous : {self.human_color}"); y += 32
        self._pill(x0 + 16, y, f"IA : {self.ia_color}"); y += 32
        phase = "Placement" if self.placement else "Jeu"
        self._pill(x0 + 16, y, f"Phase : {phase}"); y += 32
        self._pill(x0 + 16, y, f"Tour : {self.turn}"); y += 32

        if phase=="Jeu" :
            self._pill(x0 + 16, y, f"Coup : {self.moves_played}"); y += 36

        # Possession (matériel) : barre blanche/noire
        if phase == "Jeu":
            self._text(x0 + 16, y, "Possession (matériel)", 12, self.colors["muted"]) ; y += 18
            bar_w = self.sidebar_w - 56
            bx = x0 + 16
            by = y
            self._draw_possession_bar(bx, by, bar_w, 16)
            # Rendre la barre cliquable pour afficher les scores exacts
            self._add_click_area(bx, by, bar_w, 16, self._show_possession_tooltip)
            y += 28

        # Toast (message court temporaire)
        if self.toast_text:
            self._pill(x0 + self.sidebar_w // 2, y, self.toast_text,
                       bg=self.colors["btn_active"], fg=self.colors["chip_fg"], center=True)
            y += 40

        if not self.placement:
            self._text(x0 + 16, y, f"Sans prise : {self.sans_prise}/5", 12, self.colors["muted"])
            y += 24

        if self.placement and self._tour_placement() == self.human_color and self.stock_h:
            self._text(x0 + 16, y, "Vos pièces à placer", 13, self.colors["muted"]); y += 10
            y = self._draw_stock_buttons(x0 + 12, y + 6)
        else:
            if self.placement:
                self._text(x0 + 16, y, "Attente du placement IA…", 12, self.colors["muted"]); y += 22

        # ---- Rappel des règles ----
        y += 50
        self._text(x0 + 16, y, "Rappel des règles", 14, self.colors["muted"], weight="bold")
        y += 4

        rules = [
            "Deux phases : placement puis jeu.",
            "Mode Reine-Roi : placer le Roi en premier.",
            "Placement (Reine-Roi) : interdit de poser si cela met en échec un roi (le vôtre ou l’adverse).",
            "Jeu (Reine-Roi) : un coup laissant votre roi en échec est illégal.",
            "Après 5 coups sans prise, le gagnant est celui qui possède la plus grande valeur de pièces.",
            "Interaction : cliquez sur une pièce, les cases autorisées s'affichent en vert, cliquez sur une case autorisée."
        ]

        y += 20
        # largeur de texte disponible dans la sidebar (marges incluses)
        wrap_w = self.sidebar_w - 56  # ≈ marge gauche (16) + puce/offset (12) + marge droite (~28)
        for r in rules:
            tid = self._text(x0 + 28, y, f"• {r}", 11, self.colors["muted"],
                             width=wrap_w, justify="left", anchor="nw")
            bbox = self.cv.bbox(tid)
            # ajoute un petit espace après chaque item
            y = (bbox[3] + 6) if bbox else (y + 18)

        y = max(y + 8, H - 60)
        self._draw_button(x0 + 16, y, 110, 32, "Menu", self._show_menu)
        self._draw_button(x0 + 136, y, 128, 32, "Recommencer", self._restart_same_settings)

    def _draw_stock_buttons(self, x, y):
        pad = 8
        curx = x
        for piece in self.stock_h:
            img = self._img(piece, 40)
            bx, by, bw, bh = curx, y, 48, 48
            bg = self.colors["btn_active"] if self.sel_place_piece == piece else self.colors["btn"]
            self._rect(bx, by, bx + bw, by + bh, bg)
            if img is not None:
                self.cv.create_image(bx + bw//2, by + bh//2, image=img)
                self.stock_btn_imgs[piece] = img
            else:
                self._text(bx + bw//2, by + bh//2, piece, 11, anchor="center", weight="bold")

            self._add_click_area(bx, by, bw, bh, lambda p=piece: self._select_piece_to_place(p))
            curx += bw + pad
        if self.sel_place_piece:
            self._draw_button(curx, y + 8, 90, 32, "Annuler", self._clear_place_selection)
            curx += 100
        return y + 56

    def _draw_button(self, x, y, w, h, label, handler):
        rect_id = self.cv.create_rectangle(x, y, x + w, y + h,
                                           fill=self.colors["btn"], outline=self.colors["btn"])
        text_id = self._text(x + w//2, y + h//2, label, 12, anchor="center", weight="bold")
        # hover states
        def on_enter(_e):
            self.cv.itemconfig(rect_id, fill=self.colors["btn_active"], outline=self.colors["btn_active"])
        def on_leave(_e):
            self.cv.itemconfig(rect_id, fill=self.colors["btn"], outline=self.colors["btn"])
        self.cv.tag_bind(rect_id, "<Enter>", on_enter); self.cv.tag_bind(text_id, "<Enter>", on_enter)
        self.cv.tag_bind(rect_id, "<Leave>", on_leave); self.cv.tag_bind(text_id, "<Leave>", on_leave)

        # trigger
        self._add_click_area(x, y, w, h, handler)

    # ===================== Overlays =====================
    def _show_menu(self):
        self.overlay = "menu"
        self._center_window(520, 320)  # re-centre et remet la fenêtre au format menu
        self.title("IA ChessQuito")
        self._draw_all()

    def _hide_overlay(self):
        self.overlay = None
        self._draw_all()

    def _draw_menu_overlay(self):
        W = self.cv.winfo_width()
        H = self.cv.winfo_height()
        self.cv.create_rectangle(0, 0, W, H, fill="#000000", stipple="gray25", outline="")

        lw, lh = 520, 320
        x0, y0 = (W - lw)//2, (H - lh)//2
        self._rect(x0, y0, x0 + lw, y0 + lh, self.colors["panel"])
        self._text(x0 + 24, y0 + 18, "Nouvelle partie", 18, weight="bold")

        # Mode (>>> sélection visible et MAJ immédiate)
        self._text(x0 + 24, y0 + 64, "Mode :", 12, self.colors["muted"])
        self._draw_menu_radio_group(x0 + 100, y0 + 54, [traduire_mode_en_string(1), traduire_mode_en_string(2), traduire_mode_en_string(3)], self.menu_vals["mode"])

        # Couleur
        self._text(x0 + 24, y0 + 110, "Je joue :", 12, self.colors["muted"])
        self._draw_menu_radio_group(x0 + 100, y0 + 100, ["BLANCS", "NOIRS"], self.menu_vals["color"])

        # Lancer
        self._draw_button(x0 + lw - 140, y0 + lh - 56, 120, 36, "Lancer", self._start_from_menu)

    def _draw_menu_radio_group(self, x, y, options, var):
        """
        Groupe radio horizontal :
          - cercle (10px) + libellé aligné à droite
          - zone de clic = cercle + libellé
          - espacement dynamique selon la largeur du texte
        """
        curx = x
        cy = y + 10

        for label in options:
            selected = (var.get() == label)

            # Cercle externe
            self.cv.create_oval(curx - 10, cy - 10, curx + 10, cy + 10,
                                fill=self.colors["btn"], outline=self.colors["grid"])
            # Pastille si sélectionné
            if selected:
                self.cv.create_oval(curx - 6, cy - 6, curx + 6, cy + 6,
                                    fill=self.colors["accent"], outline=self.colors["accent"])

            # Libellé à droite du cercle
            text_x = curx + 16
            label_fill = self.colors["accent"] if selected else self.colors["text"]
            label_weight = "bold" if selected else "normal"
            self._text(text_x, cy, label, 12, fill=label_fill, anchor="w", weight=label_weight)

            # Mesure de la largeur réelle du libellé pour caler l'espacement et la zone cliquable
            tmp = self.cv.create_text(0, 0, text=label, font=("SF Pro Text", 12))
            bbox = self.cv.bbox(tmp)
            self.cv.delete(tmp)
            tw = (bbox[2] - bbox[0]) if bbox else 40

            # Handler de sélection + redraw immédiat
            def _handler(v=var, val=label):
                v.set(val)
                self._draw_all()

            # Zone de clic couvrant le cercle + le libellé
            click_x = curx - 16
            click_w = (text_x + tw + 6) - click_x  # cercle + espace + texte
            self._add_click_area(click_x, cy - 14, click_w, 28, _handler)

            # Avance pour l'option suivante (texte + marge)
            curx = text_x + tw + 36


    def _show_end(self, title, details):
        self.end_info["title"] = title
        self.end_info["details"] = details
        self.overlay = "end"
        self._center_window(520, 320)
        self._draw_all()

    def _draw_end_overlay(self):
        W = self.cv.winfo_width()
        H = self.cv.winfo_height()
        self.cv.create_rectangle(0, 0, W, H, fill="#000000", stipple="gray25", outline="")
        lw, lh = 520, 240
        x0, y0 = (W - lw)//2, (H - lh)//2
        self._rect(x0, y0, x0 + lw, y0 + lh, self.colors["panel"])
        self._text(x0 + lw//2, y0 + 24, "Fin de partie", 18, anchor="n", weight="bold")
        self._text(x0 + lw//2, y0 + 70, self.end_info["title"], 16, anchor="n", weight="bold")
        self._text(x0 + lw//2, y0 + 130, self.end_info["details"], 12,
                   anchor="n", fill=self.colors["muted"], width=lw - 48, justify="center")
        self._draw_button(x0 + lw//2 - 120, y0 + lh - 56, 100, 36, "Menu", self._show_menu)
        self._draw_button(x0 + lw//2 + 20, y0 + lh - 56, 100, 36, "Rejouer", self._restart_same_settings)

    # ===================== Interaction =====================
    def _add_click_area(self, x, y, w, h, handler):
        rid = self.cv.create_rectangle(x, y, x + w, y + h, outline="", fill="", width=0)
        self.cv.tag_bind(rid, "<Button-1>", lambda e: handler())

    def _on_click(self, ev):
        if self.overlay in ("menu", "end"):
            return
        if self._in_board(ev.x, ev.y):
            i, j = self._coord_to_ij(ev.x, ev.y)
            if i is None:
                return
            if self.placement:
                self._click_place(i, j)
            else:
                self._click_game(i, j)
        self._draw_all()

    def _in_board(self, x, y):
        x0 = self.board_x0 + self.LEFT_LABEL
        y0 = self.board_y0 + self.TOP_LABEL
        x1 = x0 + self.CELL * N
        y1 = y0 + self.CELL * N
        return x0 <= x <= x1 and y0 <= y <= y1

    def _coord_to_ij(self, x, y):
        x0 = self.board_x0 + self.LEFT_LABEL
        y0 = self.board_y0 + self.TOP_LABEL
        j = (x - x0) // self.CELL
        i = (y - y0) // self.CELL
        if 0 <= i < N and 0 <= j < N:
            return int(i), int(j)
        return None, None

    # ===================== Démarrage / reset =====================
    def _start_from_menu(self):
        self._center_window(1080, 720)  # agrandit et centre la fenêtre de jeu
        self.mode = traduire_mode_en_int(self.menu_vals["mode"].get())
        self.human_color = self.menu_vals["color"].get()
        self.ia_color = 'BLANCS' if self.human_color == 'NOIRS' else 'NOIRS'
        # Titre dynamique
        self.title(f"IA ChessQuito — {traduire_mode_en_string(self.mode)} — {self.human_color}")
        self._reset_match()
        self.overlay = None
        self._draw_all()
        self.after(40, self._placement_auto_ia)

    def _restart_same_settings(self):
        self._center_window(1080, 720)
        self.title(f"IA ChessQuito — {traduire_mode_en_string(self.mode)} — {self.human_color}")
        self._reset_match()
        self.overlay = None
        self._draw_all()
        self.after(40, self._placement_auto_ia)

    def _reset_match(self):
        self.board = new_board()
        self.placement = True
        self.sans_prise = 0
        self.moves_played = 0
        self.sel_from = None
        self.sel_place_piece = None
        self.hints.clear()
        self.last_move = None

        b, n = creer_pieces(self.mode)
        self.stock_h, self.stock_ia = (b.copy(), n.copy()) if self.human_color == 'BLANCS' else (n.copy(), b.copy())
        self.turn = 'BLANCS'

    # ===================== Placement =====================
    def _tour_placement(self):
        if self.ia_color == 'BLANCS':
            return determiner_tour_placement(self.stock_ia, self.stock_h)
        else:
            return determiner_tour_placement(self.stock_h, self.stock_ia)

    def _select_piece_to_place(self, piece):
        self.sel_place_piece = piece
        self.hints = self._placement_hints_for(piece)
        self._draw_all()

    def _clear_place_selection(self):
        self.sel_place_piece = None
        self.hints.clear()
        self._draw_all()

    def _placement_hints_for(self, piece):
        hints = set()
        if not self.placement or self._tour_placement() != self.human_color:
            return hints

        # Règle "Roi en premier" en mode 3
        if self.mode == 3 and len(self.stock_h) == 4 and piece[1:] != "RR":
            return hints

        me = 'B' if self.human_color == 'BLANCS' else 'N'
        adv = 'N' if me == 'B' else 'B'

        candidates = coups_possibles_placements(self.board)
        for pos_str in candidates:
            nboard = placer_piece_placement(piece, pos_str, self.board)
            if nboard is None:
                continue
            if self.mode == 3:
                if roi_en_echec(nboard, adv) or roi_en_echec(nboard, me):
                    continue
            li, co = str_to_pos(pos_str)
            hints.add((li, co))
        return hints

    def _click_place(self, i, j):
        if self._tour_placement() != self.human_color:
            return
        if not self.sel_place_piece or (i, j) not in self.hints:
            return

        pos = pos_to_str(i, j)
        nboard = placer_piece_placement(self.sel_place_piece, pos, self.board)
        if nboard is None:
            return

        if self.mode == 3:
            me = 'B' if self.human_color == 'BLANCS' else 'N'
            adv = 'N' if me == 'B' else 'B'
            if roi_en_echec(nboard, adv) or roi_en_echec(nboard, me):
                self._show_toast("Placement illégal : met un roi en échec")
                return

        self.board = nboard
        if self.sel_place_piece in self.stock_h:
            self.stock_h.remove(self.sel_place_piece)
        self.sel_place_piece = None
        self.hints.clear()

        # Fin placement ?
        if not self.stock_h and not self.stock_ia:
            self._end_placement_to_game()
        else:
            self.after(30, self._placement_auto_ia)

    def _placement_auto_ia(self):
        if not self.placement or not self.stock_ia:
            return
        moved = False
        while self.placement and self.stock_ia and self._tour_placement() == self.ia_color:
            if not self._ia_place_once():
                break
            moved = True
            if not self.stock_h and not self.stock_ia:
                break

        if not self.stock_h and not self.stock_ia:
            self._end_placement_to_game()
        elif moved:
            self._draw_all()

    def _ia_place_once(self):
        import math
        ia = 'B' if self.ia_color == 'BLANCS' else 'N'
        hu = 'B' if self.human_color == 'BLANCS' else 'N'

        score, best_pos, best_piece = valMaxPlacement(
            self.board, self.mode, ia, hu,
            self.stock_ia, self.stock_h,
            -math.inf, math.inf, profondeur=4
        )
        if best_pos in ('-f', None) or best_piece in ('-f', None):
            return False

        nboard = placer_piece_placement(best_piece, best_pos, self.board)
        if nboard is None:
            return False

        if self.mode == 3:
            if roi_en_echec(nboard, ia) or roi_en_echec(nboard, hu):
                return False

        self.board = nboard
        if best_piece in self.stock_ia:
            self.stock_ia.remove(best_piece)
        return True

    def _end_placement_to_game(self):
        self.placement = False
        self.sans_prise = 0
        self.turn = 'BLANCS'
        self.sel_from = None
        self.sel_place_piece = None
        self.hints.clear()
        self._draw_all()
        if self.ia_color == 'BLANCS':
            self.after(50, self._ia_move)

    # ===================== Jeu =====================
    def _click_game(self, i, j):
        if (self.turn == 'BLANCS' and self.human_color != 'BLANCS') or \
           (self.turn == 'NOIRS'  and self.human_color != 'NOIRS'):
            return

        me = 'B' if self.human_color == 'BLANCS' else 'N'
        piece = self.board[i][j]

        if self.sel_from is None:
            if piece == '.' or piece[0] != me:
                return
            self.sel_from = (i, j)
            self.hints = self._legal_moves(i, j)
            self._draw_all()
            return

        src_i, src_j = self.sel_from
        src_piece = self.board[src_i][src_j]
        dest_str = pos_to_str(i, j)

        if dest_str not in {pos_to_str(*p) for p in self.hints}:
            self._show_toast("Case non autorisée")
            self.sel_from = None
            self.hints.clear()
            self._draw_all()
            return

        nboard, prise = jouer_coup(self.board, src_piece, dest_str)
        if self.mode == 3 and roi_en_echec(nboard, me):
            self._show_toast("Coup illégal : roi en échec")
            self.sel_from = None
            self.hints.clear()
            self._draw_all()
            return

        self.last_move = (self.sel_from, (i, j))
        self.board = nboard
        self.sans_prise = 0 if prise else (self.sans_prise + 1)
        self.moves_played += 1
        self.sel_from = None
        self.hints.clear()
        self.turn = 'NOIRS' if self.turn == 'BLANCS' else 'BLANCS'

        self._draw_all()
        if self._check_end_via_engine():
            return

        if (self.turn == 'BLANCS' and self.ia_color == 'BLANCS') or \
           (self.turn == 'NOIRS'  and self.ia_color == 'NOIRS'):
            self.after(50, self._ia_move)

    def _legal_moves(self, i, j):
        piece = self.board[i][j]
        dests = deplacements_possibles(self.board, piece, i, j)
        res = set()
        me = 'B' if self.human_color == 'BLANCS' else 'N'
        for d in dests:
            li, co = str_to_pos(d)
            if self.mode == 3:
                nboard, _ = jouer_coup(self.board, piece, d)
                if piece[0] == me and roi_en_echec(nboard, me):
                    continue
            res.add((li, co))
        return res

    def _ia_move(self):
        if (self.turn == 'BLANCS' and self.ia_color != 'BLANCS') or \
           (self.turn == 'NOIRS'  and self.ia_color != 'NOIRS'):
            return

        import math
        ia = 'B' if self.ia_color == 'BLANCS' else 'N'
        hu = 'B' if self.human_color == 'BLANCS' else 'N'

        score, best_pos, best_piece = valMaxJeu(
            self.board, self.mode, self.sans_prise, ia, hu,
            -math.inf, math.inf, profondeur=4
        )
        if best_pos in ('-f', None) or best_piece in ('-f', None):
            return

        # source IA
        src_i = src_j = -1
        for x in range(N):
            for y in range(N):
                if self.board[x][y] == best_piece:
                    src_i, src_j = x, y
                    break
            if src_i != -1:
                break

        li, co = str_to_pos(best_pos)
        prise = (self.board[li][co] != '.')
        self.last_move = ((src_i, src_j), (li, co))
        self.board[li][co] = self.board[src_i][src_j]
        self.board[src_i][src_j] = '.'
        self.sans_prise = 0 if prise else (self.sans_prise + 1)
        self.moves_played += 1
        self.turn = 'NOIRS' if self.turn == 'BLANCS' else 'BLANCS'

        self._draw_all()
        self._check_end_via_engine()

    # ===================== Fin via moteur =====================
    def _check_end_via_engine(self):
        next_color_char = self.turn[0]  # 'B' ou 'N'
        if verifierFinPartie(self.mode, self.board, self.sans_prise, next_color_char):
            v, typeV = determiner_victoire(self.board, self.mode)
            b, n = calcul_score_plateau(self.board)
            title = "Match nul" if v == 'AUCUN' else f"Vainqueur : {v}   •   Type de Victoire : {typeV}"
            details = f"Scores\nBLANCS = {b}   •   NOIRS = {n}"
            self._show_end(title, details)
            return True
        return False


if __name__ == "__main__":
    app = ChessQuittoUI()
    app.mainloop()