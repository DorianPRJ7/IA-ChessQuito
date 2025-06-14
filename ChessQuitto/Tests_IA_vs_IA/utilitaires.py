import sys

############## UTILITAIRES ##############
def activer_logs_dans_fichier(nom_fichier):
    sys.stdout = open(nom_fichier, "w", encoding="utf-8")


def reset_terminal():
    sys.stdout.close()
    sys.stdout = sys.__stdout__


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
    # Colonne B Ligne 3 -> Indice 1 2
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


def peutAttaquer(jeu, val_piece, ligne_piece, colonne_piece, ligne_cible, colonne_cible):
    # Ignore la case si elle est identique à la position d'origine
    if ligne_piece == ligne_cible and colonne_piece == colonne_cible:
        return False

    if ligne_cible < 0 or ligne_cible >= 4 or colonne_cible < 0 or colonne_cible >= 4:
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
        if (dist_ligne, dist_col) in mouvements:
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
        if peutAttaquer(jeu, 'F', ligne_piece, colonne_piece, ligne_cible, colonne_cible):  # Test en diagonales
            return True

        if peutAttaquer(jeu, 'T', ligne_piece, colonne_piece, ligne_cible, colonne_cible):  # Test en ligne/colonne
            return True

        return False

    return False


def coord_roi(jeu, couleur):
    for ligne in range(4): # Pour chaque ligne et chaque colonne
        for colonne in range(4):
            piece=jeu[ligne][colonne]
            if piece[0]==couleur and piece[1:]=='RR': # Si la piece courante est le roi adverse
                return ligne, colonne # on retourne les coords

    return -1, -1 # Si on a pas trouvé, on retourne -1 -1


def roi_adverse_en_echec(jeu, couleur_adv, pieces_adv):
    if len(pieces_adv)==4: # Si le roi adverse n'est pas encore placé alors False
        return False

    ligne, colonne = coord_roi(jeu, couleur_adv)
    if ligne==-1 and colonne==-1: # Si coord_roi_adverse renvoie -1 -1 alors False
        return False

    if couleur_adv=='B': # Si l'adversaire est blanc mes pieces sont noires, sinon elles sont blanches
        mes_pieces=positions_pieces(jeu, 'N')
    else:
        mes_pieces=positions_pieces(jeu, 'B')
    for piece in mes_pieces:
        i=piece[0]
        j=piece[1]
        la_piece=jeu[i][j]
        if peutAttaquer(jeu, la_piece[1:], i, j, ligne, colonne):
            return True

    return False # Si aucune piece ne peut attaquer le roi alors False

def piece_est_au_centre(ligne, colonne):
    if (ligne==1 or ligne==2) and (colonne==1 or colonne==2):
        return True
    return False

def piece_est_dans_coin(ligne, colonne):
    if (ligne==0 or ligne==3) and (colonne==0 or colonne==3):
        return True
    return False

def piece_est_sur_le_cote(ligne, colonne):
    if (ligne==0 or ligne==3) and (colonne==1 or colonne==2):
        return True
    if (ligne==1 or colonne==2) and (colonne==0 or colonne==3):
        return True
    return False

def positions_pieces(jeu, couleur):
    positions = []
    for i in range(4):
        for j in range(4):
            piece=jeu[i][j]
            if (piece!='.') and (piece[0]==couleur):
                positions+=[(i,j)]
    return positions


def piece_est_menacee(jeu, ligne, colonne, couleur):
    if couleur=='B':
        ennemis = positions_pieces(jeu, 'N')
    else:
        ennemis = positions_pieces(jeu, 'B')

    for pos in ennemis:
        i=pos[0]
        j=pos[1]
        piece=jeu[i][j]
        if(piece!='.') and (piece[0]!=couleur):
            if peutAttaquer(jeu, piece[1:], i, j, ligne, colonne):
                return True

    return False


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

    if jeu[ligne][colonne] != '.': # Si la position n'est pas dispo
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


def calcul_malus_piece(jeu, couleur_piece_verif, val_piece_verif, ligne, colonne):
    malus_piece=0
    cout_malus=cout_piece(val_piece_verif)

    for i in range(4):
        for j in range(4):
            piece=jeu[i][j]
            if piece!='.' and piece[0]!=couleur_piece_verif: # Si il y a une piece
                # ET que sa couleur est différente de celle de la piece pour laquelle on verifie le malus, alors
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
                malus_blancs+= calcul_malus_piece(jeu, piece[0], piece[1:], ligne, colonne)
            elif piece!='.' and piece[0]=='N': # Sinon, si il y a une piece noire alors
                malus_noirs += calcul_malus_piece(jeu, piece[0], piece[1:], ligne, colonne)

    return malus_blancs, malus_noirs


def calcul_bonus_position_piece(val_piece, ligne, colonne):
    bonus_position=0
    if piece_est_au_centre(ligne, colonne): # Si la piece est au centre,
        if val_piece == 'C':  # Si c'est un Cavalier => bien au centre
            bonus_position += 3
        elif val_piece == 'T':  # Si c'est une Tour => pas bien au centre
            bonus_position -= 1
        elif val_piece == 'F':  # Si c'est un Fou => bien au centre
            bonus_position += 1
        elif val_piece in ['R', 'RP']:  # Si c'est une Reine ou une Reine-Pion => bon au centre
            bonus_position += 2
        elif val_piece == 'RR':  # Si c'est une Reine-Roi => mauvais au centre
            bonus_position -= 3

    elif piece_est_sur_le_cote(ligne, colonne): # Sinon si c'est sur le coté
        if val_piece == 'C':  # Si c'est un Cavalier => pas ouf sur les côtés
            bonus_position -= 1.5
        elif val_piece == 'T':  # Si c'est une Tour => bien sur les côtés
            bonus_position += 2
        elif val_piece == 'F':  # Si c'est un Fou => bien sur les cotés
            bonus_position += 1.5
        elif val_piece=='RP': # Si c'est une Reine-Pion => Moyen sur les cotés
            bonus_position += 1.5
        elif val_piece =='R':  # Si c'est une Reine => Bien sur les cotés
            bonus_position += 2
        elif val_piece == 'RR':  # Reine-Roi : Bien mais que dans les coins
            bonus_position +=3

    elif piece_est_dans_coin(ligne, colonne):
        if val_piece == 'C':  # Si c'est un Cavalier => Pas mauvais dans les coins
            bonus_position += 2
        elif val_piece == 'T':  # Si c'est une Tour => Bon dans les coins
            bonus_position += 2
        elif val_piece == 'F':  # Si c'est un Fou => Pas ouf dans les coins
            bonus_position += 0.5
        elif val_piece=='RP': # Si c'est une Reine-Pion => Pas ouf dans les coins
            bonus_position += 0.5
        elif val_piece =='R':  # Si c'est une Reine => Bien sur les cotés
            bonus_position += 1
        elif val_piece == 'RR':  # Reine-Roi : Bien mais que dans les coins
            bonus_position += 3

    return bonus_position


def calcul_bonus_position(jeu):
    bonus_position_blancs=0
    bonus_position_noirs=0

    for ligne in range(4):
        for colonne in range(4):
            piece = jeu[ligne][colonne]
            if piece != '.' and piece[0] == 'B':  # Si il y a une piece blanche alors
                bonus_position_blancs += calcul_bonus_position_piece(piece[1:], ligne, colonne)
            elif piece != '.' and piece[0] == 'N':  # Sinon, si il y a une piece noire alors
                bonus_position_noirs += calcul_bonus_position_piece(piece[1:], ligne, colonne)

    return bonus_position_blancs, bonus_position_noirs


def calcul_bonus_attaque(jeu, ennemis,couleur_piece , val_piece, ligne, colonne):
    bonus=0
    for ennemi in ennemis:
            i=ennemi[0]
            j=ennemi[1]
            piece=jeu[i][j]
            if peutAttaquer(jeu, val_piece, ligne, colonne, i, j):
                if not piece_est_menacee(jeu,ligne, colonne, couleur_piece):
                    bonus += cout_piece(piece[1:])
                else:
                    bonus += cout_piece(piece[1:])
    return bonus


def bonus_attaque(jeu, couleur):
    bonus = 0
    allies = positions_pieces(jeu, couleur)
    if couleur == 'B':
        ennemis = positions_pieces(jeu, 'N')
    else:
        ennemis = positions_pieces(jeu, 'B')

    for pos in allies:
            i=pos[0]
            j=pos[1]
            piece = jeu[i][j]
            bonus+=calcul_bonus_attaque(jeu, ennemis, couleur, piece[1:], i, j)
    return bonus


def bonus_soutien_entre_pieces(jeu, ma_couleur):
    bonus = 0
    allies = positions_pieces(jeu, ma_couleur)
    for coord1 in allies:
        ligne1 = coord1[0]
        colonne1 = coord1[1]
        piece1 = jeu[ligne1][colonne1]
        for coord2 in allies:
            ligne2 = coord2[0]
            colonne2 = coord2[1]
            piece2 = jeu[ligne2][colonne2]
            if piece1!=piece2:
                if peutAttaquer(jeu, piece1[1:], ligne1, colonne1, ligne2, colonne2):
                    if piece2[1:]!='RR' and piece2[1:]!='R':
                        bonus += cout_piece(piece2[1:])
                    else:
                        bonus += cout_piece(piece2[1:])
    return bonus


def mobilite_piece(jeu,couleur_piece, val_piece, ligne, colonne):
    deplacements = 0
    for i in range(4):
        for j in range(4):
            piece=jeu[i][j]
            if peutAttaquer(jeu, val_piece, ligne, colonne, i, j):
                if piece == '.' or piece[0] != couleur_piece:
                    deplacements += 1
    return deplacements


def score_mobilite(jeu, couleur):
    score=0
    pieces=positions_pieces(jeu, couleur)
    for piece in pieces:
        i=piece[0]
        j=piece[1]
        la_piece=jeu[i][j]
        score += mobilite_piece(jeu, la_piece[0], la_piece[1:], i, j)
    return score


def cases_controlees_par(jeu, couleur):
    cases= []
    pieces=positions_pieces(jeu, couleur)
    for piece in pieces:
        i=piece[0]
        j=piece[1]
        piece1 = jeu[i][j]
        for ligne in range(4):
            for colonne in range(4):
                piece2=jeu[ligne][colonne]
                if peutAttaquer(jeu, piece1[1:], i, j, ligne, colonne):
                    if piece2== '.' or piece2[0]!=couleur:
                        cases+= [(ligne,colonne)]
    return cases


def score_diversite_controle(jeu, couleur):
    cases = cases_controlees_par(jeu, couleur)
    return len(cases)


def calcul_roi_protege(jeu,couleur):
    nbAlliesAutour=0
    ligne_roi, colonne_roi=coord_roi(jeu,couleur)
    allies=positions_pieces(jeu, couleur)

    for pos in allies:
        i=pos[0]
        j=pos[1]
        if peutAttaquer(jeu,'RR', ligne_roi, colonne_roi, i, j):
            nbAlliesAutour+=1

    if nbAlliesAutour>2 : # Si trop d'allies autour alors malus
        bonusAlliesAutour=-2
    else : # Sinon c'est bien
        bonusAlliesAutour=2*nbAlliesAutour

    return bonusAlliesAutour


def penalite_proximite(jeu, couleur):
    penalite = 0
    if(couleur=='B'):
        ennemis = positions_pieces(jeu, 'N')
    else:
        ennemis = positions_pieces(jeu, 'B')
    allies  = positions_pieces(jeu, couleur)
    for pos1 in allies:
        i1=pos1[0]
        j1=pos1[1]
        for pos2 in ennemis:
            i2=pos2[0]
            j2=pos2[1]
            if max(abs(i1-i2), abs(j1-j2)) == 1:
                penalite += 3

    return penalite

Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']