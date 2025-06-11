import math

############## UTILITAIRES ##############
def nouveau_jeu():
    return [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.']
    ]


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


def traduire_pos_en_indice(pos):
    colonne=pos[0]
    ligne=pos[1]
    # Colonne B Ligne 3 -> Indist_lignece 1 2,
    indice_col = Colonnes.index(colonne)
    indice_lig = Lignes.index(ligne)
    return indice_lig, indice_col


def traduire_indice_en_pos(ligne, colonne):
    pos=Colonnes[colonne]+Lignes[ligne]
    return pos


def copier_plateau(jeu):
    n_jeu=[]
    for ligne in jeu:
        n_ligne = []
        for colonne in ligne :
            n_ligne+=[colonne]
        n_jeu+=[n_ligne]
    return n_jeu


def cout_piece(val_piece):
    if val_piece=='R' or val_piece=='RR':
        return 5
    elif val_piece=='T' :
        return 4
    elif val_piece=='C':
        return 3
    elif val_piece=='F':
        return 2
    elif val_piece=='RP':
        return 1
    else :
        return 0



############## PHASE DE PLACEMENT ##############
def determiner_tour_placement(pieces_blanches, pieces_noires):
    if len(pieces_blanches) >= len(pieces_noires) : # S'il y a moins de pieces noires alors c'est au tour des blancs
        return 'BLANCS'
    else :
        return 'NOIRS'


def coups_possibles_placements(jeu):
    les_coups_possibles = []
    for ligne in range(len(jeu)):
        for colonne in range(len(jeu[ligne])):
            case=jeu[ligne][colonne]
            if case == '.' :
                les_coups_possibles+=[traduire_indice_en_pos(ligne,colonne)]
    return les_coups_possibles


def placer_piece_placement(piece, pos, jeu):
    ligne, colonne = traduire_pos_en_indice(pos)

    if jeu[ligne][colonne] != '.': # Si la position n'est pas dist_lignespo
        print("Choisissez une autre position, case occupée !\n")
        return None
    # Sinon, on place la piece
    n_jeu=copier_plateau(jeu)
    n_jeu[ligne][colonne] = piece
    return n_jeu


def calcul_score_plateau(jeu):
    score_blancs=0
    score_noirs=0

    for ligne in jeu:
        for piece in ligne:
            if piece != '.':
                couleur = piece[0]
                valeur = piece[1:]
                if couleur == 'B':
                    score_blancs += cout_piece(valeur)
                else:
                    score_noirs += cout_piece(valeur)

    return score_blancs, score_noirs


def peutAttaquer(jeu, val_piece,ligne_piece,colonne_piece, ligne_cible, colonne_cible):
    # Ignore la case si elle est identique à la position d'origine
    if ligne_piece==ligne_cible and colonne_piece==colonne_cible:
        return False

    if ligne_cible<0 or ligne_cible>=4 or colonne_cible<0 or colonne_cible>=4:
        return False

    dist_ligne = ligne_cible - ligne_piece
    dist_col = colonne_cible - colonne_piece

    # Reine-Roi
    if val_piece == 'RR':
        return abs(dist_ligne) <= 1 and abs(dist_col) <= 1

    # Reine-Pion
    if val_piece == 'RP':
        return abs(dist_ligne) == 1 and abs(dist_col) == 1

    # Cavalier
    if val_piece == 'C':
        mouvements = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                      (-2, -1), (-1, -2), (1, -2), (2, -1)]
        if(dist_ligne, dist_col) in mouvements :
            return True
        return False

    # Fou
    if val_piece == 'F':
        if abs(dist_ligne) == abs(dist_col):
            if dist_ligne > 0:
                nbCases_ligne = 1
            else:
                nbCases_ligne = -1

            if dist_col > 0:
                nbCases_colonne = 1
            else:
                nbCases_colonne = -1
            
            for i in range(1, abs(dist_ligne)):
                if jeu[ligne_piece + i * nbCases_ligne][colonne_piece + i * nbCases_colonne] != '.':
                    return False
            return True

    # Tour
    if val_piece == 'T':
        # vers le haut
        if dist_col == 0 and dist_ligne < 0:
            for i in range(1, abs(dist_ligne)):
                if jeu[ligne_piece - i][colonne_piece] != '.':
                    return False
            return True
        # Vers le bas
        if dist_col == 0 and dist_ligne > 0:
            for i in range(1, dist_ligne):
                if jeu[ligne_piece + i][colonne_piece] != '.':
                    return False
            return True
        # Vers la gauche
        if dist_ligne == 0 and dist_col < 0:
            for i in range(1, abs(dist_col)):
                if jeu[ligne_piece][colonne_piece - i] != '.':
                    return False
            return True
        # Vers la droite
        if dist_ligne == 0 and dist_col > 0:
            for i in range(1, dist_col):
                if jeu[ligne_piece][colonne_piece + i] != '.':
                    return False
            return True

    # Reine
    if val_piece == 'R':
        if peutAttaquer(jeu,'F', ligne_piece, colonne_piece, ligne_cible, colonne_cible): # Test en dist_ligneagonales
            return True

        if peutAttaquer(jeu, 'T', ligne_piece, colonne_piece, ligne_cible, colonne_cible): # Test en ligne/colonne
            return True

        return False

    return False


def calcul_malus_piece(jeu, couleur_piece_verif, val_piece_verif, ligne, colonne):
    malus_piece=0
    cout_malus=cout_piece(val_piece_verif)
    for i in range(4):
        for j in range(4):
            piece=jeu[i][j]
            if piece!='.' and piece[0]!=couleur_piece_verif: # Si il y a une piece
                # ET que sa couleur est dist_lignefférente de celle de la piece pour laquelle on verifie le malus, alors
                if peutAttaquer(jeu, piece[1:],i,j,ligne, colonne):
                    malus_piece+=cout_malus

    return malus_piece


def calcul_malus_pieces_posees(jeu):
    malus_blancs=0
    malus_noirs=0

    for ligne in range(4):
        for colonne in range(4):
            piece=jeu[ligne][colonne]
            if piece!='.' and piece[0]=='B': # Si il y a une piece blanche alors
                malus_blancs+=calcul_malus_piece(jeu, piece[0], piece[1:], ligne, colonne)
            elif piece!='.' and piece[0]=='N': # Sinon, si il y a une piece noire alors
                malus_noirs += calcul_malus_piece(jeu, piece[0], piece[1:], ligne, colonne)

    return malus_blancs, malus_noirs


def evaluer_placement(jeu, pieces_joueur):
    if len(pieces_joueur)==0 :
        return 0

    couleur_joueur=(pieces_joueur[0])[0] # le premier caractere de la premiere piece restante
    # print(couleur_joueur) # DEBUG

    if couleur_joueur=='B':
        score_joueur, score_adv = calcul_score_plateau(jeu)
        malus_joueur, malus_adv = calcul_malus_pieces_posees(jeu)
    else:
        score_adv, score_joueur=calcul_score_plateau(jeu)
        malus_adv, malus_joueur = calcul_malus_pieces_posees(jeu)

    return score_joueur-malus_joueur-score_adv+malus_adv


def valMaxPlacement(jeu, pieces_ia, pieces_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (profondeur==0) or (len(pieces_ia) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_placement(jeu,pieces_ia), '-f', '-f'
    """
        Algorithme :: PVH
        Hypothèse : score en deçà du minimum
        Vérification : à chaque coup, màj de scoreMax et coupMax si besoin
    """

    scoreMax = -math.inf
    coupMax = -math.inf
    pieceMax='.'

    for coup in lesCoups:
        for piece in pieces_ia:
            nouvellesPieces=pieces_ia.copy()
            nouveauJeu = placer_piece_placement(piece, coup, jeu)
            nouvellesPieces.remove(piece)
            score, _, _ = valMinPlacement(nouveauJeu, pieces_humain, nouvellesPieces, alpha, beta, profondeur-1)
            if score > scoreMax:
                scoreMax = score
                coupMax = coup
                pieceMax = piece

            if score > beta:
                return score, coup, piece

            alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement(jeu, pieces_humain, pieces_ia, alpha, beta, profondeur):
    """
        Fonction recursive simulant le coup joué par Humain
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if (profondeur == 0) or (len(pieces_humain) == 0) or (len(lesCoups) == 0):
        # print("pieces_humain=",pieces_humain) # DEBUG
        return evaluer_placement(jeu, pieces_humain), '-f', '-f'

    """
      Algorithme :: PVH
      Hypothèse : score en deçà du minimum
      Vérification : à chaque coup, màj de scoreMin et coupMin si besoin
    """
    scoreMin = +math.inf
    coupMin = +math.inf
    pieceMin = '.'

    for coup in lesCoups:
        for piece in pieces_humain:
            nouvellesPieces = pieces_humain.copy()
            nouveauJeu = placer_piece_placement(piece, coup, jeu)
            nouvellesPieces.remove(piece)
            score, _, _ = valMaxPlacement(nouveauJeu, pieces_ia, nouvellesPieces, alpha, beta, profondeur-1)
            if (score < scoreMin):
                scoreMin = score
                coupMin = coup
                pieceMin = piece

            if alpha >= score:
                return score, coup, piece

            beta = min(beta, score)
    return scoreMin, coupMin, pieceMin


def lancer_tour_placement_ia(jeu,pieces_ia, pieces_humain):
    best_score, best_pos, best_piece = valMaxPlacement(jeu, pieces_ia, pieces_humain, -math.inf, +math.inf, profondeur=4)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece_placement(best_piece, best_pos, jeu)
    pieces_ia.remove(best_piece)
    return jeu


def lancer_tour_placement_humain(jeu,mode_jeu,pieces):
    lesCoups=coups_possibles_placements(jeu)
    piece=''
    pos=''
    estValide=False
    while not estValide :
        message = input("Quelle piece et a quelle position souhaitez vous jouer ? (Exemple de format : 'BR A2' -> Reine Blanche en A2)\n")
        tab=message.split(" ")

        if len(tab)==2 : # Si la taille de la saisie est valide
            piece = tab[0]
            pos = tab[1]
            if(piece in pieces) and (pos in lesCoups) : # Si la piece ET la position sont valides,
                if mode_jeu==3 and len(pieces)==4: # Si on est en mode 3 ET qu'on est au premier tour
                    if piece[1:]=="RR": # Si la valeur de la piece est le ROI, alors c'est valide
                        estValide=True
                    else: # Sinon on affiche message d'invalidité de la piece à poser
                        print("Votre Roi doit être placé en premier !")
                else: # Sinon (= si on est dans un autre mode ou pas au premier tour du mode 3), alors c'est valide
                    estValide=True
            else: # Sinon on affiche un message d'invalidité de la piece ou position
                print("Piece ou Position invalide !")
        else:
            print("Saisie invalide ! Format : PIECE POS -> Ex : 'BF A2'")

    print("piece : ",piece, "\tpos : ", pos) # Affichage de DEBUG
    jeu = placer_piece_placement(piece, pos, jeu)
    pieces.remove(piece)
    return jeu


def phase_de_placement(jeu,mode_jeu, joueur_ia, pieces_ia, pieces_humain):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia) > 0 or len(pieces_humain) > 0 :
        if joueur_ia=='BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia, pieces_noires=pieces_humain)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_humain, pieces_noires=pieces_ia)

        if tour == joueur_ia :
            print("\n\t*********** TOUR IA ***********\n")
            print("Pieces a placer => ", pieces_ia, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia(jeu,pieces_ia, pieces_humain)
        else :
            print("\n\t*********** TOUR HUMAIN ***********\n")
            print("Pieces a placer => ", pieces_humain, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_humain(jeu,mode_jeu,pieces_humain)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu



############## PHASE DE JEU ##############
# TODO


############## JEU ##############
def jouer():
    # Definit le mode de jeu
    mode_jeu=0
    while mode_jeu!=1 and mode_jeu !=2 and mode_jeu!=3 :
        mode_jeu = int(input("Quel mode de jeu souhaitez vous ? (1=REINE, 2=REINE_PION, 3=REINE_ROI) \n"))

    # Definit qui joue quelle couleur ainsi que leurs pieces en fonction du mode de jeu
    joueur_humain = ''
    while joueur_humain not in ('BLANCS', 'NOIRS'):
        joueur_humain = input("Vous jouez BLANCS ou NOIRS ? ")
    if joueur_humain == 'BLANCS':
        joueur_ia = 'NOIRS'
        pieces_humain, pieces_ia = creer_pieces(mode_jeu)
    else :
        joueur_ia='BLANCS'
        pieces_ia, pieces_humain = creer_pieces(mode_jeu)

    print("\n\t*********** PASSAGE EN JEU ***********\n")
    print("Mode de Jeu choisi -> ","1 : REINE" if mode_jeu == 1 else "2 : REINE_PION" if mode_jeu == 2 else "3 : REINE_ROI")
    print(f"Vous êtes ", joueur_humain, "\t|\tl'IA est ", joueur_ia, "\n")
    print("\nPIECES HUMAIN = ", pieces_humain, "\t|\tPIECES IA = ", pieces_ia, "\n")

    # Definit le plateau de jeu
    jeu = nouveau_jeu()
    afficher(jeu)

    # Demarre la phase de placement
    jeu=phase_de_placement(jeu,mode_jeu,joueur_ia,pieces_ia.copy(),pieces_humain.copy())
    afficher(jeu)

Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']
jouer()
