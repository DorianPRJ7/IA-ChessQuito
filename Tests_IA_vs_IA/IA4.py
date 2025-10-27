import math
from utilitaires import *

def evaluer_placement4(jeu, mode_jeu, couleur_joueur):
    if mode_jeu == 1:
        pond_score = 1.0
        pond_malus = 1.3
        pond_position = 1.0
        pond_attaque = 0.8
        pond_soutien = 1.2
        pond_mobilite = 0.8
        pond_diversite = 0.8
        pond_penalite_proximite = 0.6

    elif mode_jeu == 2:
        pond_score = 1.0
        pond_malus = 1.7
        pond_position = 0.5
        pond_attaque = 0.6
        pond_soutien = 1.5
        pond_mobilite = 0.7
        pond_diversite = 0.7
        pond_penalite_proximite = 1.0

    else:
        pond_score = 1.0
        pond_malus = 1.9
        pond_position = 0.4
        pond_attaque = 0.5
        pond_soutien = 1.6
        pond_mobilite = 0.7
        pond_diversite = 0.8
        pond_penalite_proximite = 1.1


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
        pond_proximite_roi = 1.9
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur)
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv)
        eval_joueur+=score_allies_pour_roi_joueur*pond_proximite_roi
        eval_adv+=score_allies_pour_roi_adv*pond_proximite_roi

    # print("\nScore_total_joueur : ", eval_joueur) # DEBUG
    # print("Score_total_adv : ", eval_adv) # DEBUG

    return eval_joueur - eval_adv

def valMaxPlacement4(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (profondeur==0) or (len(pieces_ia) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_placement4(jeu, mode_jeu, couleur_ia), '-f', '-f'
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
                    score, _, _ = valMinPlacement4(nouveauJeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, nouvellesPieces, alpha, beta, profondeur-1)

                    if score > scoreMax:
                        scoreMax = score
                        coupMax = coup
                        pieceMax = piece

                    if score > beta:
                        return score, coup, piece

                    alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement4(jeu, mode_jeu, couleur_humain, couleur_ia, pieces_humain, pieces_ia, alpha, beta, profondeur):
    """
        Fonction recursive simulant le coup joué par Humain
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if (profondeur == 0) or (len(pieces_humain) == 0) or (len(lesCoups) == 0):
        # print("pieces_humain=",pieces_humain) # DEBUG
        return evaluer_placement4(jeu, mode_jeu, couleur_humain), '-f', '-f'

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
                    score, _, _ = valMaxPlacement4(nouveauJeu, mode_jeu,couleur_ia, couleur_humain, pieces_ia, nouvellesPieces, alpha, beta, profondeur-1)


                    if score < scoreMin:
                        scoreMin = score
                        coupMin = coup
                        pieceMin = piece

                    if alpha >= score:
                        return score, coup, piece

                    beta = min(beta, score)
    return scoreMin, coupMin, pieceMin


def lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia, couleur_humain, pieces_ia, pieces_humain):
    best_score, best_pos, best_piece = valMaxPlacement4(jeu, mode_jeu,couleur_ia,couleur_humain, pieces_ia, pieces_humain, -math.inf, +math.inf, profondeur=3)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece_placement(best_piece, best_pos, jeu)
    pieces_ia.remove(best_piece)
    return jeu


############## PHASE DE JEU ##############
def evaluer_jeu4(jeu, mode_jeu, couleur_joueur):
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

    if mode_jeu == 1 or mode_jeu == 2:
        pond_ecart_de_score = 2
        pond_grosses_pieces_en_vie = 2

        bonus_grosses_pieces_en_vie_joueur = calcul_grosses_pieces_en_vie(jeu,
                                                                          couleur_joueur) * pond_grosses_pieces_en_vie
        bonus_grosses_pieces_en_vie_adv = calcul_grosses_pieces_en_vie(jeu, couleur_adv) * pond_grosses_pieces_en_vie

        eval_joueur += bonus_ecart_de_score * pond_ecart_de_score + bonus_grosses_pieces_en_vie_joueur
        eval_adv += bonus_grosses_pieces_en_vie_adv

        if mode_jeu == 1:
            pond_reine_en_vie = 1.5
            pond_protection_reine = 1.5
            pond_attaque_reine = 1.5
            pond_reine_en_danger = 3

            bonus_reine_en_vie_joueur = calcul_bonus_reine_en_vie(jeu, couleur_joueur) * pond_reine_en_vie
            bonus_reine_en_vie_adv = calcul_bonus_reine_en_vie(jeu, couleur_adv) * pond_reine_en_vie
            score_protection_reine_joueur = calcul_protection_reine(jeu, couleur_joueur) * pond_protection_reine
            score_protection_rein_adv = calcul_protection_reine(jeu, couleur_adv) * pond_protection_reine
            score_attaque_reine_joueur = calcul_attaque_reine(jeu, couleur_joueur) * pond_attaque_reine
            score_attaque_reine_adv = calcul_attaque_reine(jeu, couleur_adv) * pond_attaque_reine
            malus_reine_en_danger_joueur = calcul_reine_en_danger(jeu, couleur_joueur) * pond_reine_en_danger
            malus_reine_en_danger_adv = calcul_reine_en_danger(jeu, couleur_adv) * pond_reine_en_danger

            eval_joueur += bonus_reine_en_vie_joueur + score_protection_reine_joueur + score_attaque_reine_joueur - malus_reine_en_danger_joueur
            eval_adv += bonus_reine_en_vie_adv + score_protection_rein_adv + score_attaque_reine_adv - malus_reine_en_danger_adv

    elif mode_jeu == 3:
        pond_proximite_roi = 1.8
        pond_mat = 3
        pond_echec = 2
        pond_pat = 1.5
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur) * pond_proximite_roi
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv) * pond_proximite_roi
        score_mat_joueur = calcul_mat(jeu, couleur_adv) * pond_mat
        score_mat_adv = calcul_mat(jeu, couleur_joueur) * pond_mat
        score_echec_joueur = calcul_echec_au_roi(jeu, couleur_adv) * pond_echec
        score_echec_adv = calcul_echec_au_roi(jeu, couleur_joueur) * pond_echec
        score_pat_joueur = calcul_pat(jeu, couleur_adv) * pond_pat
        score_pat_adv = calcul_pat(jeu, couleur_joueur) * pond_pat

        eval_joueur += score_allies_pour_roi_joueur + score_mat_joueur + score_echec_joueur + score_pat_joueur
        eval_adv += score_allies_pour_roi_adv + score_mat_adv + score_echec_adv + score_pat_adv

    return eval_joueur - eval_adv


def valMaxJeu4(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu4(jeu, mode_jeu, couleur_ia), '-f', '-f'
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

                score, _, _ = valMinJeu4(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score > scoreMax:
                    scoreMax = score
                    coupMax = coup
                    pieceMax = piece

                if score > beta:
                    return score, coup, piece

                alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinJeu4(jeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    if (profondeur==0) or (verifierFinPartie(mode_jeu,jeu,sans_prise)):
        # print("pieces_ia=", pieces_ia) # DEBUG
        return evaluer_jeu4(jeu, mode_jeu, couleur_humain), '-f', '-f'
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

                score, _, _ = valMaxJeu4(nouveauJeu, mode_jeu, sans_prise, couleur_ia, couleur_humain, alpha, beta, profondeur-1)

                if score < scoreMin:
                    scoreMin = score
                    coupMin = coup
                    pieceMin = piece

                if alpha >= score:
                    return score, coup, piece

                beta = min(beta, score)

    return scoreMin, coupMin, pieceMin


def lancer_tour_jeu_ia4(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv):
    best_score, best_pos, best_piece = valMaxJeu4(jeu, mode_jeu, sans_prise, couleur_ia, couleur_adv, -math.inf, +math.inf, profondeur=3)
    if best_pos == '-f' or best_piece == '-f':
        return

    jeu, prise= jouer_coup(jeu,best_piece, best_pos)
    return jeu, prise