import math

def nouveau_jeu():
    return [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.']
    ]


def traduire_position(pos):
    colonne=pos[0]
    ligne=pos[1]
    # Colonne B Ligne 3 -> Indice 1 2,
    indice_col = Colonnes.index(colonne)
    indice_lig = Lignes.index(ligne)
    return indice_lig, indice_col

############## PLACEMENT DES PIECES ##############
def determiner_tour_placement(pieces_blanches, pieces_noires):
    if len(pieces_blanches) >= len(pieces_noires) : # S'il y a moins de pieces noires alors c'est au tour des blancs
        return 'BLANCS'
    else :
        return 'NOIRS'


def copier_plateau(jeu):
    n_jeu=[]
    for ligne in jeu:
        n_ligne = []
        for colonne in ligne :
            n_ligne+=[colonne]
        n_jeu+=[n_ligne]
    return n_jeu


def placer_piece(piece,pos,jeu):
    ligne, colonne = traduire_position(pos)

    if jeu[ligne][colonne] != '.': # Si la position n'est pas dispo
        print("Choisissez une autre position, case occupée !\n")
        return None
    # Sinon, on place la piece
    n_jeu=copier_plateau(jeu)
    n_jeu[ligne][colonne] = piece
    return n_jeu

def coup_piece(piece):
    if piece=='R' or piece=='RR':
        return 5
    elif piece=='T' :
        return 4
    elif piece=='C' or piece=='F':
        return 3
    elif piece=='RP':
        return 2
    else :
        return 0


def traduire_indice_en_pos(ligne, colonne):
    pos=Colonnes[colonne]+Lignes[ligne]
    return pos


def coups_possibles_placements(jeu):
    les_coups_possibles = []
    for ligne in range(len(jeu)):
        for colonne in range(len(jeu[ligne])):
            case=jeu[ligne][colonne]
            if case == '.' :
                les_coups_possibles+=[traduire_indice_en_pos(ligne,colonne)]
    return les_coups_possibles


def valMaxPlacement(jeu, pieces, alpha, beta):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (len(pieces) == 0) or (len(lesCoups) == 0):
        return 0, '-f', '-f'
    """
        Algorithme :: PVH
        Hypothèse : score en deçà du minimum
        Vérification : à chaque coup, màj de scoreMax et coupMax si besoin
    """

    scoreMax = -math.inf
    coupMax = -math.inf
    pieceMax='.'

    for coup in lesCoups:
        for piece in pieces:
            nouvellesPieces=pieces.copy()
            nouveauJeu = placer_piece(piece, coup, jeu)
            nouvellesPieces.remove(piece)
            score, _, _ = valMinPlacement(nouveauJeu, nouvellesPieces, alpha, beta)
            if (score > scoreMax):
                scoreMax = score
                coupMax = coup
                pieceMax = piece

            if (score > beta):
                return score, coup, piece

            alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement(jeu, pieces, alpha, beta):
    """
        Fonction recursive simulant le coup joué par Humain
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if(len(pieces)==0) or (len(lesCoups)==0):
        return 0, '-f', '-f'

    """
      Algorithme :: PVH
      Hypothèse : score en deçà du minimum
      Vérification : à chaque coup, màj de scoreMin et coupMin si besoin
    """
    scoreMin = +math.inf
    coupMin = +math.inf
    pieceMin = '.'

    for coup in lesCoups:
        for piece in pieces:
            nouvellesPieces = pieces.copy()
            nouveauJeu = placer_piece(piece, coup, jeu)
            nouvellesPieces.remove(piece)
            score, _, _ = valMaxPlacement(nouveauJeu, nouvellesPieces, alpha, beta)
            if (score < scoreMin):
                scoreMin = score
                coupMin = coup
                pieceMin = piece

            if alpha >= score:
                return score, coup, piece

            beta = min(beta, score)
    return scoreMin, coupMin, pieceMin

def lancer_tour_placement_ia(jeu,pieces):
    best_score, best_pos, best_piece = valMaxPlacement(jeu, pieces, -math.inf, +math.inf)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece(best_piece,  best_pos, jeu)
    pieces.remove(best_piece)
    return jeu


def lancer_tour_placement_humain(jeu,pieces):
    lesCouts=coups_possibles_placements(jeu)
    piece=''
    pos=''
    while (piece not in pieces) or (pos not in lesCouts) :
        message = input("Quelle piece et a quelle position souhaitez vous jouer ? ")
        tab=message.split(" ")
        piece=tab[0]
        pos=tab[1]

    print("piece : ",piece, "\tpos : ", pos) # Affichage de DEBUG
    jeu = placer_piece(piece, pos, jeu)
    pieces.remove(piece)
    return jeu


def phase_de_placement(jeu, joueur_ia, pieces_blanches, pieces_noires):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_blanches) > 0 or len(pieces_noires) > 0 :
        tour=determiner_tour_placement(pieces_blanches, pieces_noires)
        if tour == 'BLANCS' :
            pieces=pieces_blanches
        else :
            pieces=pieces_noires

        if tour == joueur_ia :
            print("\n\t*********** TOUR IA ***********\n")
            print("Pieces a placer => ", pieces, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia(jeu,pieces)
        else :
            print("\n\t*********** TOUR HUMAIN ***********\n")
            print("Pieces a placer => ", pieces, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_humain(jeu,pieces)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


def creer_pieces(mode_jeu):
    pieces_blanches = []
    pieces_noires = []
    if mode_jeu == 1 :
        pieces_blanches += ['BR']
        pieces_noires += ['NR']
    elif mode_jeu == 2 :
        pieces_blanches += ['BRP']
        pieces_noires += ['NRP']
    else :
        pieces_blanches += ['BRR']
        pieces_noires += ['NRR']

    pieces_blanches += ['BT', 'BF', 'BC']
    pieces_noires += ['NT', 'NF', 'NC']
    return pieces_blanches, pieces_noires

def afficher(jeu):
    print("  A B C D")
    print("1", jeu[0][0], jeu[0][1], jeu[0][2], jeu[0][3])
    print("2", jeu[1][0], jeu[1][1], jeu[1][2], jeu[1][3])
    print("3", jeu[2][0], jeu[2][1], jeu[2][2], jeu[2][3])
    print("4", jeu[3][0], jeu[3][1], jeu[3][2], jeu[3][3])
    print("\n")


def jouer():
    # Definit le mode de jeu
    mode_jeu=0
    while mode_jeu!=1 and mode_jeu !=2 and mode_jeu!=3 :
        mode_jeu = int(input("Quel mode de jeu souhaitez vous ? (1=REINE, 2=REINE_PION, 3=REINE_ROI) \n"))

    # Definit qui joue quelle couleur
    joueur_humain = ''
    while joueur_humain not in ('BLANCS', 'NOIRS'):
        joueur_humain = input("Vous jouez BLANCS ou NOIRS ? ")
    if joueur_humain == 'BLANCS':
        joueur_ia = 'NOIRS'
    else :
        joueur_ia='BLANCS'


    print("\n\t*********** PASSAGE EN JEU ***********\n")
    print("Mode de Jeu choisi -> ","1 : REINE" if mode_jeu == 1 else "2 : REINE_PION" if mode_jeu == 2 else "3 : REINE_ROI")
    print(f"Vous êtes ", joueur_humain, ", l'IA est ", joueur_ia, "\n")

    # Definit les pieces en fonction du mode de jeu
    pieces_blanches, pieces_noires = creer_pieces(mode_jeu)
    print("\nPIECES BLANCHES = ", pieces_blanches,"\nPIECES NOIRES = ", pieces_noires, "\n")

    # Definit le plateau de jeu
    jeu = nouveau_jeu()
    afficher(jeu)

    # Demarre la phase de placement
    jeu=phase_de_placement(jeu,joueur_ia,pieces_blanches.copy(),pieces_noires.copy())
    afficher(jeu)
    print("\nPIECES BLANCHES = ", pieces_blanches,"\nPIECES NOIRES = ", pieces_noires, "\n")

Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']
jouer()