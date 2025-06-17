import math

############## UTILITAIRES ##############
def nouveau_jeu():
    return [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.']
    ]


def afficher(jeu):
    print("  A B C D")
    print("1", jeu[0][0], jeu[0][1], jeu[0][2], jeu[0][3])
    print("2", jeu[1][0], jeu[1][1], jeu[1][2], jeu[1][3])
    print("3", jeu[2][0], jeu[2][1], jeu[2][2], jeu[2][3])
    print("4", jeu[3][0], jeu[3][1], jeu[3][2], jeu[3][3])
    print("\n")


def copier_plateau(jeu):
    n_jeu=[]
    for ligne in jeu:
        n_ligne = []
        for colonne in ligne :
            n_ligne+=[colonne]
        n_jeu+=[n_ligne]
    return n_jeu


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

def traduire_pos_en_indice(pos):
    colonne=pos[0]
    ligne=pos[1]
    # Colonne B Ligne 3 -> Indice 1 2
    if ligne in ['1', '2', '3', '4'] and colonne in ['A', 'B', 'C', 'D']:
        indice_col = Colonnes.index(colonne)
        indice_lig = Lignes.index(ligne)
        return indice_lig, indice_col
    else:
        return -1, -1


def traduire_indice_en_pos(ligne, colonne):
    if ligne>=0 and ligne<4 and colonne>=0 and colonne<4:
        return Colonnes[colonne]+Lignes[ligne]
    else:
        return ''


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


def coord_roi(jeu, couleur):
    for ligne in range(4): # Pour chaque ligne et chaque colonne
        for colonne in range(4):
            piece=jeu[ligne][colonne]
            if piece[0]==couleur and piece[1:]=='RR': # Si la piece courante est le roi adverse
                return ligne, colonne # on retourne les coords

    return -1, -1 # Si on a pas trouvé, on retourne -1 -1


def coord_piece(jeu, piece):
    for ligne in range(4):
        for colonne in range(4):
            piece_courante=jeu[ligne][colonne]
            if piece_courante==piece:
                return ligne, colonne
    return -1, -1


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


def roi_en_echec(jeu, couleur):
    ligne, colonne = coord_roi(jeu, couleur)
    if ligne==-1 and colonne==-1: # Si coord_roi_adverse renvoie -1 -1 alors False
        return False

    if couleur== 'B': # Si l'adversaire est blanc mes pieces sont noires, sinon elles sont blanches
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


def est_en_mat(jeu, couleur):
    if roi_en_echec(jeu, couleur): # Si le roi est en echec
        allies=positions_pieces(jeu, couleur)
        for allie in allies: # Pour chaque piece allie
            i=allie[0]
            j=allie[1]
            piece=jeu[i][j]
            lesCoups=deplacements_possibles(jeu,piece,i,j)
            for coup in lesCoups: # Pour chaque coup possible de la piece
                nouveauJeu, _=jouer_coup(jeu,piece,coup)
                if not roi_en_echec(nouveauJeu, couleur): # Si le coup joué permet de faire en sorte que le roi ne soit plus en echec, alors il n'y a pas mat
                    return False
        return True
    else: # Sinon (si le roi n'est pas en echec), il n'y a pas mat
        return False


def echec_et_mat(jeu):
    return est_en_mat(jeu,'B') or est_en_mat(jeu,'N')


def est_en_pat(jeu, couleur):
    if not roi_en_echec(jeu,couleur) and not est_en_mat(jeu,couleur) : # Si on est pas, ni en echec, ni en mat
        allies=positions_pieces(jeu, couleur)
        for allie in allies: # Pour chaque piece allie
            i=allie[0]
            j=allie[1]
            piece=jeu[i][j]
            lesCoups=deplacements_possibles(jeu,piece,i,j)
            if len(lesCoups)>0: # Si la piece a des coups possibles
                if piece[1:]!='RR': # Si c'est pas un roi alors on est pas en pat
                    return False
                else: # Si c'est le roi,
                    for coup in lesCoups: # Pour chaque coup possible du roi
                        nouveauJeu, _=jouer_coup(jeu,piece,coup)
                        if not est_en_mat(nouveauJeu,couleur): # Si le coup joué fait en sorte que le roi ne soit pas en echec alors on est pas en pat
                            return False
        return True
    else: # Sinon (si on est en mat), alors on est pas en pat
        return False


def est_pat(jeu):
    return est_en_pat(jeu,'N') or est_en_pat(jeu,'B')


def determiner_tour_placement(pieces_blanches, pieces_noires):
    if len(pieces_blanches) >= len(pieces_noires) : # S'il y a moins de pieces noires alors c'est au tour des blancs
        return 'BLANCS'
    else :
        return 'NOIRS'


def coups_possibles_placements(jeu):
    les_coups_possibles = []
    for ligne in range(4):
        for colonne in range(4):
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


def deplacements_possibles(jeu, piece, ligne_piece, colonne_piece):
    positions=[]
    allies=positions_pieces(jeu, piece[0])
    for lig_dest in range(4):
        for col_dest in range(4):
            if not (lig_dest, col_dest) in allies: # Si la pos de destination n'est pas dans les pos allies
                piece_dest=jeu[lig_dest][col_dest]
                if piece[1:]!='RP' or piece_dest!='.' : # Si la piece n'est pas un pion ou que la piece de destination n'est pas vide
                    if peutAttaquer(jeu,piece[1:], ligne_piece, colonne_piece, lig_dest, col_dest): # Si la piece peut l'atteindre, alors on l'ajoute
                        positions+=[traduire_indice_en_pos(lig_dest,col_dest)]
                else : # Sinon => Si c'est un pion et une case de destination vide
                    if abs(lig_dest-ligne_piece)+abs(col_dest-colonne_piece)==1: # Si peut aller vers avant arriere ou cotes, alors on l'ajoute
                        positions+=[traduire_indice_en_pos(lig_dest, col_dest)]

    return positions


def jouer_coup(jeu, piece, pos):
    ligne, colonne = traduire_pos_en_indice(pos)
    ancienne_ligne, ancienne_colonne = coord_piece(jeu, piece)

    if jeu[ligne][colonne]=='.':
        prise=False
    else:
        prise=True

    nouveauJeu=copier_plateau(jeu)
    nouveauJeu[ligne][colonne]=piece
    nouveauJeu[ancienne_ligne][ancienne_colonne]='.'
    jeu=nouveauJeu

    return jeu, prise


def verifierFinPartie(mode_jeu, jeu, sans_prise):
    if sans_prise>=5: # Si plus de 5 deplacements sans prises, alors fin de partie
        return True

    pos_pieces_blanches=positions_pieces(jeu, 'B')
    pos_pieces_noires=positions_pieces(jeu, 'N')
    if len(pos_pieces_blanches)==0 or len(pos_pieces_noires)==0: # Si un des deux joueurs n'a plus de pieces, alors fin de partie
        return True

    if mode_jeu==3: # Si on est en mode 3
        if echec_et_mat(jeu) or est_pat(jeu): # Si on est en echec et mat ou en pat, alors fin de partie
            return True

    return False


def determiner_victoire(jeu, mode_jeu):
    if mode_jeu==3 and (echec_et_mat(jeu) or est_pat(jeu)):
        if est_en_pat(jeu,'B'):
            return 'NOIRS', 'PAT'
        elif est_en_pat(jeu,'N'):
            return 'BLANCS', 'PAT'
        else:
            blancs_sont_mat=est_en_mat(jeu,'B')
            noirs_sont_mat=est_en_mat(jeu,'N')
            if not blancs_sont_mat and noirs_sont_mat:
                return 'BLANCS', 'ECHEC ET MAT'
            if blancs_sont_mat and not noirs_sont_mat:
                return 'NOIRS', 'ECHEC ET MAT'
            else:
                print("Probleme dans le calcul des scores")
                return

    else:
        score_blancs, score_noirs = calcul_score_plateau(jeu)
        if score_blancs==0 or score_noirs==0:
            typeVictoire='PIECES'
        else:
            typeVictoire='SANS PRISE'
        if score_blancs > score_noirs:
            return 'BLANCS', typeVictoire
        elif score_noirs> score_blancs:

            return 'NOIRS',typeVictoire
        else:
            return 'AUCUN', typeVictoire


def afficher_victoire(victoire, typeVictoire, score_ia, score_humain, couleur_ia, couleur_humain):
    if victoire=='AUCUN':
        print("Match nul par ", typeVictoire, " !")
    if victoire==couleur_ia:
        print("IA (=",couleur_ia,") gagne par ", typeVictoire, " !")
    elif victoire==couleur_humain:
        print("Humain (=",couleur_humain,") gagne par ", typeVictoire, " !")

    print("Score IA :", score_ia, "| Score HUMAIN :", score_humain)


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


def calcul_bonus_position_piece(jeu, couleur_piece, val_piece, ligne, colonne):
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
        elif val_piece == 'RR':  # Reine-Roi : Bien
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
        elif val_piece == 'RR':  # Reine-Roi : Bien si protégé
            if calcul_roi_protege(jeu, couleur_piece)>0:
                bonus_position += 3
            else:
                bonus_position -= 3

    return bonus_position


def calcul_bonus_position(jeu):
    bonus_position_blancs=0
    bonus_position_noirs=0

    for ligne in range(4):
        for colonne in range(4):
            piece = jeu[ligne][colonne]
            if piece != '.' and piece[0] == 'B':  # Si il y a une piece blanche alors
                bonus_position_blancs += calcul_bonus_position_piece(jeu, piece[0], piece[1:], ligne, colonne)
            elif piece != '.' and piece[0] == 'N':  # Sinon, si il y a une piece noire alors
                bonus_position_noirs += calcul_bonus_position_piece(jeu, piece[0], piece[1:], ligne, colonne)

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
        if peutAttaquer(jeu,'RR', ligne_roi, colonne_roi, i, j): # SI le roi peut attaquer la piece allie (si il est a une case de son allie)
            nbAlliesAutour+=1

    if nbAlliesAutour>1 : # Si trop d'allies autour alors malus
        bonusAlliesAutour=-nbAlliesAutour
    else : # Sinon c'est bien
        bonusAlliesAutour=nbAlliesAutour

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
        piece_allie=jeu[i1][j1]
        for pos2 in ennemis:
            i2=pos2[0]
            j2=pos2[1]
            if max(abs(i1-i2), abs(j1-j2)) == 1:
                if piece_allie[1:] == 'RR' or piece_allie[1:] == 'R':
                    penalite += 6
                else:
                    penalite += 3

    return penalite

def calcul_mat(jeu, couleur_adv):
    if est_en_mat(jeu,couleur_adv):
        return 10
    return 0


def calcul_echec_au_roi(jeu, couleur_adv):
    nbEchecAuRoi=0
    for i in range(4):
        for j in range(4):
            piece=jeu[i][j]
            if piece[0]!=couleur_adv:
                ligne_roi, colonne_roi=coord_roi(jeu,piece)
                if peutAttaquer(jeu,piece[1:],i,j,ligne_roi, colonne_roi):
                    nbEchecAuRoi+=1
    return nbEchecAuRoi*2


def calcul_pat(jeu, couleur_adv):
    if est_en_mat(jeu,couleur_adv):
        return 10
    return 0



def calcul_grosses_pieces_en_vie(jeu, couleur_joueur):
    allies = positions_pieces(jeu, couleur_joueur)
    bonus=0
    for allie in allies:
        i = allie[0]
        j = allie[1]
        piece = jeu[i][j]
        cout=cout_piece(piece[1:])
        if cout>=3:
            bonus+=cout

    if bonus!=0:
        return bonus
    else:
        return -3


def calcul_bonus_reine_en_vie(jeu, couleur_joueur):
    allies=positions_pieces(jeu,couleur_joueur)
    for allie in allies:
        i=allie[0]
        j=allie[1]
        piece=jeu[i][j]
        if piece[1:]=='R':
            return 5
    return -5


def calcul_protection_reine(jeu, couleur_joueur):
    allies = positions_pieces(jeu, couleur_joueur)
    score_protection=0
    for allie in allies:
        i1=allie[0]
        j1=allie[1]
        piece = jeu[i1][j1]
        if piece[1:] == 'R':
            for autre_allie in allies:
                if allie != autre_allie:
                    i2=autre_allie[0]
                    j2=autre_allie[1]
                    protecteur=jeu[i2][j2]
                    if peutAttaquer(jeu, protecteur[1:], i2, j2, i1, j1):
                        score_protection+=1

    if score_protection>0:
        return score_protection
    else:
        return -3


def calcul_attaque_reine(jeu, couleur_joueur):
    if couleur_joueur=='B':
        couleur_adv='N'
    else:
        couleur_adv='B'
    ennemis = positions_pieces(jeu, couleur_adv)

    for i in range(4):
        for j in range(4):
            piece = jeu[i][j]
            if piece[0] == couleur_joueur and piece[1:] == 'R':
                bonus = 0
                for pos in ennemis:
                    ligne=pos[0]
                    colonne=pos[1]
                    piece_adv = jeu[ligne][colonne]
                    if peutAttaquer(jeu, 'R', i, j, ligne, colonne):
                        bonus += cout_piece(piece_adv[1:])
                return bonus
    return 0


def calcul_reine_en_danger(jeu, couleur_joueur):
    if couleur_joueur == 'B':
        couleur_adv = 'N'
    else:
        couleur_adv = 'B'
    ennemis = positions_pieces(jeu, couleur_adv)
    malus_attaque=0

    for i in range(4):
        for j in range(4):
            piece = jeu[i][j]
            if piece[0] == couleur_joueur and piece[1:] == 'R':
                for pos in ennemis:
                    ligne=pos[0]
                    colonne=pos[1]
                    piece_ennemie = jeu[ligne][colonne]
                    if peutAttaquer(jeu, piece_ennemie[1:], ligne, colonne, i, j):
                        malus_attaque-=5
    if malus_attaque<0:
        return malus_attaque
    else:
        return 5


############## PHASE DE PLACEMENT ##############
def evaluer_placement(jeu, mode_jeu, couleur_joueur):
    if mode_jeu == 1:
        pond_score = 1.0
        pond_malus = 1.2
        pond_position = 1.0
        pond_attaque = 1.0
        pond_soutien = 0.8
        pond_mobilite = 0.7
        pond_diversite = 0.6
        pond_penalite_proximite = 0.4

    elif mode_jeu == 2:
        pond_score = 1.0
        pond_malus = 1.6
        pond_position = 0.4
        pond_attaque = 0.6
        pond_soutien = 1.4
        pond_mobilite = 0.6
        pond_diversite = 0.7
        pond_penalite_proximite = 0.9

    else:
        pond_score = 1.0
        pond_malus = 1.8
        pond_position = 0.3
        pond_attaque = 0.5
        pond_soutien = 1.6
        pond_mobilite = 0.7
        pond_diversite = 0.8
        pond_penalite_proximite = 1.0

    if couleur_joueur == 'B':
        couleur_adv = 'N'
        score_joueur, score_adv = calcul_score_plateau(jeu)
        malus_joueur, malus_adv = calcul_malus_pieces_posees(jeu)
        bonus_position_joueur, bonus_position_adv = calcul_bonus_position(jeu)
    else:
        couleur_adv = 'B'
        score_adv, score_joueur = calcul_score_plateau(jeu)
        malus_adv, malus_joueur = calcul_malus_pieces_posees(jeu)
        bonus_position_adv, bonus_position_joueur = calcul_bonus_position(jeu)

    bonus_agressif_joueur = bonus_attaque(jeu, couleur_joueur)
    bonus_agressif_adv = bonus_attaque(jeu, couleur_adv)

    bonus_soutien_joueur = bonus_soutien_entre_pieces(jeu, couleur_joueur)
    bonus_soutien_adv = bonus_soutien_entre_pieces(jeu, couleur_adv)

    bonus_mobilite_joueur = score_mobilite(jeu, couleur_joueur)
    bonus_mobilite_adv = score_mobilite(jeu, couleur_adv)

    score_div_joueur = score_diversite_controle(jeu, couleur_joueur)
    score_div_adv = score_diversite_controle(jeu, couleur_adv)

    malus_proximite_joueur = penalite_proximite(jeu, couleur_joueur)
    malus_proximite_adv = penalite_proximite(jeu, couleur_adv)

    score_joueur *= pond_score
    score_adv *= pond_score

    malus_joueur *= pond_malus
    malus_adv *= pond_malus

    bonus_position_joueur *= pond_position
    bonus_position_adv *= pond_position

    bonus_agressif_joueur *= pond_attaque
    bonus_agressif_adv *= pond_attaque

    bonus_soutien_joueur *= pond_soutien
    bonus_soutien_adv *= pond_soutien

    bonus_mobilite_joueur *= pond_mobilite
    bonus_mobilite_adv *= pond_mobilite

    score_div_joueur *= pond_diversite
    score_div_adv *= pond_diversite

    malus_proximite_joueur *= pond_penalite_proximite
    malus_proximite_adv *= pond_penalite_proximite

    eval_joueur = score_joueur - malus_joueur + bonus_position_joueur + bonus_agressif_joueur + bonus_soutien_joueur + bonus_mobilite_joueur + score_div_joueur - malus_proximite_joueur
    eval_adv = score_adv - malus_adv + bonus_position_adv + bonus_agressif_adv + bonus_soutien_adv + bonus_mobilite_adv + score_div_adv - malus_proximite_adv

    if mode_jeu == 3:
        pond_proximite_roi = 1.8
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur)
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv)
        eval_joueur += score_allies_pour_roi_joueur * pond_proximite_roi
        eval_adv += score_allies_pour_roi_adv * pond_proximite_roi

    # print("\nScore_total_joueur : ", eval_joueur) # DEBUG
    # print("Score_total_adv : ", eval_adv) # DEBUG

    return eval_joueur - eval_adv

def valMaxPlacement(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (profondeur==0) or (len(pieces_ia) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_placement(jeu, mode_jeu, couleur_ia), '-f', '-f'
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
            if (mode_jeu!=3) or (len(pieces_ia)<4) or (piece[1:]=="RR"): # Si on est pas en mode 3 OU qu'on a moins de 4 pieces a poser OU qu'on veut poser le Roi, alors on teste
                nouvellesPieces=pieces_ia.copy()
                nouveauJeu = placer_piece_placement(piece, coup, jeu)
                nouvellesPieces.remove(piece)
                if (mode_jeu!=3) or (not roi_en_echec(nouveauJeu, couleur_humain) and not roi_en_echec(nouveauJeu, couleur_ia)): # Si on est pas en mode 3 OU qu'on ne met pas le roi adverse en echec ET que le mien non plus, alors
                    score, _, _ = valMinPlacement(nouveauJeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, nouvellesPieces, alpha, beta, profondeur-1)

                    if score > scoreMax:
                        scoreMax = score
                        coupMax = coup
                        pieceMax = piece

                    if score > beta:
                        return score, coup, piece

                    alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement(jeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, pieces_ia, alpha, beta, profondeur):
    """
        Fonction recursive simulant le coup joué par Humain
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if (profondeur == 0) or (len(pieces_humain) == 0) or (len(lesCoups) == 0):
        # print("pieces_humain=",pieces_humain) # DEBUG
        return evaluer_placement(jeu, mode_jeu, couleur_humain), '-f', '-f'

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
            if (mode_jeu != 3) or (len(pieces_humain) < 4) or (piece[1:] == "RR"):  # Si on est pas en mode 3 OU qu'on a moins de 4 pieces a poser OU qu'on veut poser le Roi, alors on teste
                nouvellesPieces = pieces_humain.copy()
                nouveauJeu = placer_piece_placement(piece, coup, jeu)
                nouvellesPieces.remove(piece)
                if (mode_jeu != 3) or (not roi_en_echec(nouveauJeu, couleur_ia) and not roi_en_echec(nouveauJeu, couleur_humain)):  # Si on est pas en mode 3 OU qu'on ne met pas le roi adverse en echec ET que le mien non plus, alors
                    score, _, _ = valMaxPlacement(nouveauJeu, mode_jeu,couleur_ia, couleur_humain, pieces_ia, nouvellesPieces, alpha, beta, profondeur-1)


                    if score < scoreMin:
                        scoreMin = score
                        coupMin = coup
                        pieceMin = piece

                    if alpha >= score:
                        return score, coup, piece

                    beta = min(beta, score)
    return scoreMin, coupMin, pieceMin


def lancer_tour_placement_ia(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain):
    best_score, best_pos, best_piece = valMaxPlacement(jeu, mode_jeu,couleur_ia,couleur_humain, pieces_ia, pieces_humain, -math.inf, +math.inf, profondeur=2)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece_placement(best_piece, best_pos, jeu)
    pieces_ia.remove(best_piece)
    return jeu


def lancer_tour_placement_humain(jeu, mode_jeu, couleur_adv, ma_couleur, pieces_adv, mes_pieces):
    lesCoups=coups_possibles_placements(jeu)
    piece=''
    pos=''
    estValide=False
    nouveauJeu=copier_plateau(jeu)
    while not estValide :
        message = input("Quelle piece et a quelle position souhaitez vous jouer ? (Exemple de format : 'BR A2' -> Reine Blanche en A2)\n")
        tab=message.split(" ")

        if len(tab)==2 : # Si la taille de la saisie est valide
            piece = tab[0]
            pos = tab[1]
            if(piece in mes_pieces) and (pos in lesCoups) : # Si la piece ET la position sont valides,
                nouveauJeu = placer_piece_placement(piece, pos, jeu)
                if mode_jeu==3: # Si on est en mode 3 alors
                    if not roi_en_echec(nouveauJeu, couleur_adv) and not roi_en_echec(nouveauJeu, ma_couleur): # Si on ne met PAS le roi adverse en echec
                        if len(mes_pieces)!=4 or piece[1:]=="RR": # Si on est pas au premier tour OU que la valeur de la piece est le ROI, alors c'est valide
                            estValide=True
                        else: # Sinon on affiche message d'invalidité de la piece à poser
                            print("Votre Roi doit être placé en premier !")
                    else:
                        print("Vous ne devez pas mettre le roi adverse en echec pendant la phase de placement")
                else: # Sinon (= si on est dans un autre mode ou pas au premier tour du mode 3), alors c'est valide
                    estValide=True
            else: # Sinon on affiche un message d'invalidité de la piece ou position
                print("Piece ou Position invalide !")
        else:
            print("Saisie invalide ! Format : PIECE POS -> Ex : 'BF A2'")

    print("piece : ",piece, "\tpos : ", pos) # Affichage de DEBUG
    jeu=nouveauJeu
    mes_pieces.remove(piece)
    return jeu


def phase_de_placement(jeu,mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia) > 0 or len(pieces_humain) > 0 :
        if couleur_ia=='BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia, pieces_noires=pieces_humain)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_humain, pieces_noires=pieces_ia)

        if tour == couleur_ia :
            print("\n\t*********** TOUR IA ***********\n")
            print("Pieces a placer => ", pieces_ia, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia(jeu, mode_jeu,couleur_ia[0], couleur_humain[0], pieces_ia, pieces_humain)
        else :
            print("\n\t*********** TOUR HUMAIN ***********\n")
            print("Pieces a placer => ", pieces_humain, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_humain(jeu,mode_jeu, couleur_ia[0], couleur_humain[0], pieces_ia, pieces_humain)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu



############## PHASE DE JEU ##############
def lancer_tour_jeu_humain(jeu, mode_jeu, ma_couleur):
    estValide=False
    nouveauJeu=copier_plateau(jeu)
    prise=0
    while not estValide:
        coup = input("Votre tour (Format PIECE POS -> BR A2) : ")
        message = coup.split(" ")
        if len(message)==2: # Si il y a bien 2 elements dans la saisie
            piece=message[0]
            pos=message[1]
            allies=positions_pieces(jeu,ma_couleur)
            coord_lig_piece, coord_col_piece = coord_piece(jeu, piece)
            # coord_lig_dest, coord_col_dest = traduire_pos_en_indice(pos)
            piece=jeu[coord_lig_piece][coord_col_piece]
            lesCoups=deplacements_possibles(jeu,piece,coord_lig_piece,coord_col_piece)
            if (coord_lig_piece, coord_col_piece) in allies:
            # Si les coords de ma pieces sont dans les pos allies => la piece est bien a moi et elle existe
                if pos in lesCoups:
                # Si les coords de la case de destination sont dans les coups possibles pour la piece => La case de destination est valide et n'est pas une de mes pieces, donc soit une piece adverse soit une case vide
                    nouveauJeu, prise=jouer_coup(jeu, piece, pos) # Fait semblant de jouer la piece
                    if mode_jeu!=3 or not roi_en_echec(nouveauJeu, ma_couleur): # Si on est pas en mode 3 ou que le coup n'a pas mis ou laissé mon roi en echec
                        estValide=True # alors c'est valide
                    else :
                        print("Attention à votre ROI !")
                else:
                    print("Coup invalide !")
            else:
                print("Piece invalide !")
        else:
            print("Saisie invalide !")

    jeu=nouveauJeu
    return jeu, prise


def evaluer_jeu(jeu, mode_jeu, couleur_joueur):
    if mode_jeu == 1:
        pond_score = 2.0
        pond_malus = 1.2
        pond_position = 1.0
        pond_attaque = 1.0
        pond_soutien = 0.8
        pond_mobilite = 0.7
        pond_diversite = 0.6

    elif mode_jeu == 2:
        pond_score = 2.0
        pond_malus = 1.6
        pond_position = 0.4
        pond_attaque = 0.6
        pond_soutien = 1.4
        pond_mobilite = 0.6
        pond_diversite = 0.7

    else:
        pond_score = 1.5
        pond_malus = 1.8
        pond_position = 0.3
        pond_attaque = 0.5
        pond_soutien = 1.6
        pond_mobilite = 0.7
        pond_diversite = 0.8

    if couleur_joueur == 'B':
        couleur_adv = 'N'
        score_joueur, score_adv = calcul_score_plateau(jeu)
        malus_joueur, malus_adv = calcul_malus_pieces_posees(jeu)
        bonus_position_joueur, bonus_position_adv = calcul_bonus_position(jeu)
    else:
        couleur_adv = 'B'
        score_adv, score_joueur = calcul_score_plateau(jeu)
        malus_adv, malus_joueur = calcul_malus_pieces_posees(jeu)
        bonus_position_adv, bonus_position_joueur = calcul_bonus_position(jeu)

    bonus_agressif_joueur = bonus_attaque(jeu, couleur_joueur)
    bonus_agressif_adv = bonus_attaque(jeu, couleur_adv)

    bonus_soutien_joueur = bonus_soutien_entre_pieces(jeu, couleur_joueur)
    bonus_soutien_adv = bonus_soutien_entre_pieces(jeu, couleur_adv)

    bonus_mobilite_joueur = score_mobilite(jeu, couleur_joueur)
    bonus_mobilite_adv = score_mobilite(jeu, couleur_adv)

    score_div_joueur = score_diversite_controle(jeu, couleur_joueur)
    score_div_adv = score_diversite_controle(jeu, couleur_adv)

    bonus_ecart_de_score = score_joueur - score_adv

    score_joueur *= pond_score
    score_adv *= pond_score

    malus_joueur *= pond_malus
    malus_adv *= pond_malus

    bonus_position_joueur *= pond_position
    bonus_position_adv *= pond_position

    bonus_agressif_joueur *= pond_attaque
    bonus_agressif_adv *= pond_attaque

    bonus_soutien_joueur *= pond_soutien
    bonus_soutien_adv *= pond_soutien

    bonus_mobilite_joueur *= pond_mobilite
    bonus_mobilite_adv *= pond_mobilite

    score_div_joueur *= pond_diversite
    score_div_adv *= pond_diversite

    eval_joueur = score_joueur - malus_joueur + bonus_position_joueur + bonus_agressif_joueur + bonus_soutien_joueur + bonus_mobilite_joueur + score_div_joueur
    eval_adv = score_adv - malus_adv + bonus_position_adv + bonus_agressif_adv + bonus_soutien_adv + bonus_mobilite_adv + score_div_adv

    if mode_jeu==1 or mode_jeu==2 :
        pond_ecart_de_score = 2.5
        pond_grosses_pieces_en_vie = 2

        bonus_grosses_pieces_en_vie_joueur = calcul_grosses_pieces_en_vie(jeu, couleur_joueur) * pond_grosses_pieces_en_vie
        bonus_grosses_pieces_en_vie_adv = calcul_grosses_pieces_en_vie(jeu, couleur_adv) * pond_grosses_pieces_en_vie

        eval_joueur += bonus_ecart_de_score*pond_ecart_de_score+bonus_grosses_pieces_en_vie_joueur
        eval_adv+=bonus_grosses_pieces_en_vie_adv


        if mode_jeu==1:
            pond_reine_en_vie=3
            pond_protection_reine=3
            pond_attaque_reine=3
            pond_reine_en_danger=4

            bonus_reine_en_vie_joueur=calcul_bonus_reine_en_vie(jeu, couleur_joueur)*pond_reine_en_vie
            bonus_reine_en_vie_adv = calcul_bonus_reine_en_vie(jeu, couleur_adv)*pond_reine_en_vie
            score_protection_reine_joueur=calcul_protection_reine(jeu,couleur_joueur)*pond_protection_reine
            score_protection_rein_adv=calcul_protection_reine(jeu,couleur_adv)*pond_protection_reine
            score_attaque_reine_joueur=calcul_attaque_reine(jeu,couleur_joueur)*pond_attaque_reine
            score_attaque_reine_adv=calcul_attaque_reine(jeu,couleur_adv)*pond_attaque_reine
            malus_reine_en_danger_joueur=calcul_reine_en_danger(jeu,couleur_joueur)*pond_reine_en_danger
            malus_reine_en_danger_adv=calcul_reine_en_danger(jeu,couleur_adv)*pond_reine_en_danger

            eval_joueur+=bonus_reine_en_vie_joueur+score_protection_reine_joueur+score_attaque_reine_joueur-malus_reine_en_danger_joueur
            eval_adv+=bonus_reine_en_vie_adv+score_protection_rein_adv+score_attaque_reine_adv-malus_reine_en_danger_adv

    elif mode_jeu == 3:
        pond_proximite_roi = 1.8
        pond_mat = 3
        pond_echec = 2
        pond_pat = 1.5
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur) * pond_proximite_roi
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv) * pond_proximite_roi
        score_mat_joueur = calcul_mat(jeu, couleur_adv)*pond_mat
        score_mat_adv = calcul_mat(jeu, couleur_joueur)*pond_mat
        score_echec_joueur = calcul_echec_au_roi(jeu, couleur_adv)*pond_echec
        score_echec_adv = calcul_echec_au_roi(jeu, couleur_joueur)*pond_echec
        score_pat_joueur=calcul_pat(jeu, couleur_adv)*pond_pat
        score_pat_adv=calcul_pat(jeu,couleur_joueur)*pond_pat



        eval_joueur += score_allies_pour_roi_joueur+score_mat_joueur+score_echec_joueur+score_pat_joueur
        eval_adv += score_allies_pour_roi_adv+score_mat_adv+score_echec_adv+score_pat_adv

    return eval_joueur - eval_adv


def valMaxJeu(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu(jeu, mode_jeu, couleur_ia), '-f', '-f'
    """
        Algorithme :: PVH
        Hypothèse : score en deçà du minimum
        Vérification : à chaque coup, màj de scoreMax et coupMax si besoin
    """

    scoreMax = -math.inf
    coupMax = -math.inf
    pieceMax='.'
    allies=positions_pieces(jeu,couleur_ia)
    for pos in allies:
        ligne_piece=pos[0]
        colonne_piece=pos[1]
        piece=jeu[ligne_piece][colonne_piece]
        lesCoups=deplacements_possibles(jeu, piece, ligne_piece, colonne_piece)
        for coup in lesCoups:
            nouveauJeu, prise=jouer_coup(jeu, piece, coup)
            if (mode_jeu!=3) or (not roi_en_echec(nouveauJeu, couleur_ia)): # Si on est pas en mode 3 OU qu'on n'a pas mis notre roi en echec, alors on continue
                if prise:
                    sans_prise=0
                else:
                    sans_prise+=1

                score, _, _ = valMinJeu(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score > scoreMax:
                    scoreMax = score
                    coupMax = coup
                    pieceMax = piece

                if score > beta:
                    return score, coup, piece

                alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinJeu(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu(jeu, mode_jeu, couleur_humain), '-f', '-f'
    """
        Algorithme :: PVH
        Hypothèse : score en deçà du minimum
        Vérification : à chaque coup, màj de scoreMax et coupMax si besoin
    """

    scoreMin = +math.inf
    coupMin = +math.inf
    pieceMin='.'
    allies=positions_pieces(jeu,couleur_humain)
    for pos in allies:
        ligne_piece = pos[0]
        colonne_piece = pos[1]
        piece=jeu[ligne_piece][colonne_piece]
        lesCoups=deplacements_possibles(jeu, piece, ligne_piece, colonne_piece)
        for coup in lesCoups:
            nouveauJeu, prise=jouer_coup(jeu, piece, coup)
            if (mode_jeu!=3) or (not roi_en_echec(nouveauJeu, couleur_humain)): # Si on est pas en mode 3 OU qu'on n'a pas mis notre roi en echec, alors on continue
                if prise:
                    sans_prise=0
                else:
                    sans_prise+=1

                score, _, _ = valMaxJeu(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score < scoreMin:
                    scoreMin = score
                    coupMin = coup
                    pieceMin = piece

                if alpha >= score:
                    return score, coup, piece

                beta = min(beta, score)

    return scoreMin, coupMin, pieceMin


def lancer_tour_jeu_ia(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv):
    best_score, best_pos, best_piece = valMaxJeu(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv, -math.inf, +math.inf, profondeur=2)
    if best_pos == '-f' or best_piece == '-f':
        return

    jeu, prise= jouer_coup(jeu,best_piece, best_pos)
    return jeu, prise



def phase_de_jeu(jeu, mode_jeu, couleur_ia, couleur_humain):
    print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        print(f"Tour actuel : ", tour)
        if tour==couleur_humain:
            jeu, prise = lancer_tour_jeu_humain(jeu,mode_jeu,couleur_humain[0])
        else:
            jeu, prise = lancer_tour_jeu_ia(jeu, mode_jeu, sans_prise, couleur_ia[0], couleur_humain[0])

        afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


############## JEU ##############
def jouer():
    # Definit le mode de jeu
    mode_jeu=0
    while mode_jeu!=1 and mode_jeu !=2 and mode_jeu!=3 :
        mode_jeu = int(input("Quel mode de jeu souhaitez vous ? (1=REINE, 2=REINE_PION, 3=REINE_ROI) \n"))

    # Definit qui joue quelle couleur ainsi que leurs pieces en fonction du mode de jeu
    couleur_humain = ''
    while couleur_humain not in ('BLANCS', 'NOIRS'):
        couleur_humain = input("Vous jouez BLANCS ou NOIRS ? ")
    if couleur_humain == 'BLANCS':
        couleur_ia = 'NOIRS'
        pieces_humain, pieces_ia = creer_pieces(mode_jeu)
    else :
        couleur_ia='BLANCS'
        pieces_ia, pieces_humain = creer_pieces(mode_jeu)

    print("\n\t*********** PASSAGE EN JEU ***********\n")
    print("Mode de Jeu choisi -> ","1 : REINE" if mode_jeu == 1 else "2 : REINE_PION" if mode_jeu == 2 else "3 : REINE_ROI")
    print(f"Vous êtes ", couleur_humain, "\t|\tl'IA est ", couleur_ia, "\n")
    print("\nPIECES HUMAIN = ", pieces_humain, "\t|\tPIECES IA = ", pieces_ia, "\n")

    # Definit le plateau de jeu
    jeu = nouveau_jeu()
    afficher(jeu)

    # Demarre la phase de placement
    jeu=phase_de_placement(jeu,mode_jeu,couleur_ia, couleur_humain,pieces_ia.copy(),pieces_humain.copy())
    afficher(jeu)

    jeu=phase_de_jeu(jeu, mode_jeu, couleur_ia, couleur_humain)
    afficher(jeu)

    victoire, typeVictoire=determiner_victoire(jeu, mode_jeu)
    if couleur_humain=='BLANCS':
        score_humain, score_ia=calcul_score_plateau(jeu)
    else:
        score_ia, score_humain=calcul_score_plateau(jeu)
    afficher_victoire(victoire, typeVictoire, score_ia, score_humain, couleur_ia, couleur_humain)

Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']
jouer()
