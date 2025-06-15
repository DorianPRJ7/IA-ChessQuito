import math
from utilitaires import *

def evaluer_placement2(jeu, mode_jeu, couleur_joueur):
    pond_score=1.0
    pond_malus=1.0
    pond_position=0.8
    pond_attaque=0.9
    pond_soutien=0.7
    pond_mobilite=0.3
    pond_diversite=0.3
    pond_penalite_proximite=0.5
    pond_proximite_roi=1.3


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


    bonus_agressif_joueur=bonus_attaque(jeu, couleur_joueur)
    bonus_agressif_adv=bonus_attaque(jeu, couleur_adv)

    bonus_soutien_joueur=bonus_soutien_entre_pieces(jeu, couleur_joueur)
    bonus_soutien_adv=bonus_soutien_entre_pieces(jeu, couleur_adv)

    bonus_mobilite_joueur=score_mobilite(jeu, couleur_joueur)
    bonus_mobilite_adv=score_mobilite(jeu, couleur_adv)

    score_div_joueur=score_diversite_controle(jeu, couleur_joueur)
    score_div_adv=score_diversite_controle(jeu, couleur_adv)

    malus_proximite_joueur=penalite_proximite(jeu, couleur_joueur)
    malus_proximite_adv=penalite_proximite(jeu, couleur_adv)

    score_joueur *= pond_score
    score_adv *= pond_score

    malus_joueur *= pond_malus
    malus_adv *= pond_malus

    bonus_position_joueur *= pond_position
    bonus_position_adv *= pond_position

    bonus_agressif_joueur *= pond_attaque
    bonus_agressif_adv *= pond_attaque

    bonus_soutien_joueur*=pond_soutien
    bonus_soutien_adv*=pond_soutien

    bonus_mobilite_joueur*=pond_mobilite
    bonus_mobilite_adv*=pond_mobilite

    score_div_joueur*=pond_diversite
    score_div_adv*=pond_diversite

    malus_proximite_joueur*=pond_penalite_proximite
    malus_proximite_adv*=pond_penalite_proximite

    eval_joueur=score_joueur - malus_joueur + bonus_position_joueur + bonus_agressif_joueur + bonus_soutien_joueur + bonus_mobilite_joueur + score_div_joueur - malus_proximite_joueur
    eval_adv=score_adv - malus_adv + bonus_position_adv + bonus_agressif_adv + bonus_soutien_adv + bonus_mobilite_adv + score_div_adv - malus_proximite_adv

    if mode_jeu==3 :
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur)
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv)
        eval_joueur+=score_allies_pour_roi_joueur*pond_proximite_roi
        eval_adv+=score_allies_pour_roi_adv*pond_proximite_roi

    # print("\nScore_total_joueur : ", eval_joueur) # DEBUG
    # print("Score_total_adv : ", eval_adv) # DEBUG

    return eval_joueur - eval_adv

def valMaxPlacement2(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (profondeur==0) or (len(pieces_ia) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_placement2(jeu, mode_jeu, couleur_ia), '-f', '-f'
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
                    score, _, _ = valMinPlacement2(nouveauJeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, nouvellesPieces, alpha, beta, profondeur-1)

                    if score > scoreMax:
                        scoreMax = score
                        coupMax = coup
                        pieceMax = piece

                    if score > beta:
                        return score, coup, piece

                    alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement2(jeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, pieces_ia, alpha, beta, profondeur):
    """
        Fonction recursive simulant le coup joué par Humain
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if (profondeur == 0) or (len(pieces_humain) == 0) or (len(lesCoups) == 0):
        # print("pieces_humain=",pieces_humain) # DEBUG
        return evaluer_placement2(jeu, mode_jeu, couleur_humain), '-f', '-f'

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
                    score, _, _ = valMaxPlacement2(nouveauJeu, mode_jeu,couleur_ia, couleur_humain, pieces_ia, nouvellesPieces, alpha, beta, profondeur-1)


                    if score < scoreMin:
                        scoreMin = score
                        coupMin = coup
                        pieceMin = piece

                    if alpha >= score:
                        return score, coup, piece

                    beta = min(beta, score)
    return scoreMin, coupMin, pieceMin


def lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain):
    best_score, best_pos, best_piece = valMaxPlacement2(jeu, mode_jeu,couleur_ia,couleur_humain, pieces_ia, pieces_humain, -math.inf, +math.inf, profondeur=3)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece_placement(best_piece, best_pos, jeu)
    pieces_ia.remove(best_piece)
    return jeu


############## PHASE DE JEU ##############
def evaluer_jeu2(jeu, mode_jeu, couleur_joueur):
    pond_score=1.0
    pond_malus=1.0
    pond_position=0.8

    if couleur_joueur == 'B':
        score_joueur, score_adv = calcul_score_plateau(jeu)
        malus_joueur, malus_adv = calcul_malus_pieces_posees(jeu)
        bonus_position_joueur, bonus_position_adv = calcul_bonus_position(jeu)
    else:
        score_adv, score_joueur = calcul_score_plateau(jeu)
        malus_adv, malus_joueur = calcul_malus_pieces_posees(jeu)
        bonus_position_adv, bonus_position_joueur = calcul_bonus_position(jeu)

    score_joueur *= pond_score
    score_adv *= pond_score

    malus_joueur *= pond_malus
    malus_adv *= pond_malus

    bonus_position_joueur *= pond_position
    bonus_position_adv *= pond_position

    eval_joueur = score_joueur - malus_joueur + bonus_position_joueur
    eval_adv = score_adv - malus_adv + bonus_position_adv

    return eval_joueur - eval_adv


def valMaxJeu2(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu2(jeu, mode_jeu, couleur_ia), '-f', '-f'
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

                score, _, _ = valMinJeu2(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score > scoreMax:
                    scoreMax = score
                    coupMax = coup
                    pieceMax = piece

                if score > beta:
                    return score, coup, piece

                alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinJeu2(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu2(jeu, mode_jeu, couleur_humain), '-f', '-f'
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

                score, _, _ = valMaxJeu2(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score < scoreMin:
                    scoreMin = score
                    coupMin = coup
                    pieceMin = piece

                if alpha >= score:
                    return score, coup, piece

                beta = min(beta, score)

    return scoreMin, coupMin, pieceMin


def lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv):
    best_score, best_pos, best_piece = valMaxJeu2(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv, -math.inf, +math.inf, profondeur=3)
    if best_pos == '-f' or best_piece == '-f':
        return

    jeu, prise= jouer_coup(jeu,best_piece, best_pos)
    return jeu, prise