import math
from utilitaires import *

def evaluer_placement3(jeu, mode_jeu, couleur_joueur):
    if couleur_joueur == 'B':
        couleur_adv = 'N'
    else:
        couleur_adv = 'B'

    pond_score=1.0
    pond_malus=1.1
    pond_position=0.8
    pond_attaque=0.7
    pond_soutien=1.2
    pond_mobilite=0.6
    pond_diversite=0.5
    pond_penalite_proximite=0.6
    pond_proximite_roi=1.6


    score_joueur, score_adv=calcul_score_plateau(jeu)
    score_joueur*=pond_score
    score_adv*=pond_score

    malus_joueur, malus_adv=calcul_malus_pieces_posees(jeu)
    malus_joueur*=pond_malus
    malus_adv*=pond_malus

    bonus_position_joueur, bonus_position_adv=calcul_bonus_position(jeu)
    bonus_position_joueur*=pond_position
    bonus_position_adv*=pond_position

    bonus_agressif_joueur=bonus_attaque(jeu, couleur_joueur)
    bonus_agressif_adv=bonus_attaque(jeu, couleur_adv)
    bonus_agressif_joueur*=pond_attaque
    bonus_agressif_adv*=pond_attaque

    bonus_soutien_joueur=bonus_soutien_entre_pieces(jeu, couleur_joueur)
    bonus_soutien_adv=bonus_soutien_entre_pieces(jeu, couleur_adv)
    bonus_soutien_joueur*=pond_soutien
    bonus_soutien_adv*=pond_soutien

    bonus_mobilite_joueur=score_mobilite(jeu, couleur_joueur)
    bonus_mobilite_adv=score_mobilite(jeu, couleur_adv)
    bonus_mobilite_joueur*=pond_mobilite
    bonus_mobilite_adv*=pond_mobilite

    score_div_joueur=score_diversite_controle(jeu, couleur_joueur)
    score_div_adv=score_diversite_controle(jeu, couleur_adv)
    score_div_joueur*=pond_diversite
    score_div_adv*=pond_diversite

    malus_proximite_joueur=penalite_proximite(jeu, couleur_joueur)
    malus_proximite_adv=penalite_proximite(jeu, couleur_adv)
    malus_proximite_joueur*=pond_penalite_proximite
    malus_proximite_adv*=pond_penalite_proximite

    eval_joueur=score_joueur - malus_joueur + bonus_position_joueur + bonus_agressif_joueur + bonus_soutien_joueur + bonus_mobilite_joueur + score_div_joueur - malus_proximite_joueur
    eval_adv=score_adv - malus_adv + bonus_position_adv + bonus_agressif_adv + bonus_soutien_adv + bonus_mobilite_adv + score_div_adv - malus_proximite_adv

    # DEBUG
    print("Plateau testé: \n")
    afficher(jeu)
    print("\nScore_joueur : ", score_joueur, " ; Malus_joueur : ", malus_joueur, " ; Bonus_position_joueur : ", bonus_position_joueur)
    print("Bonus_agressif_joueur : ", bonus_agressif_joueur, " ; Bonus_soutien_joueur : ", bonus_soutien_joueur, " ; Bonus_mobilite_joueur : ", bonus_mobilite_joueur)
    print("Score_div_joueur : ", score_div_joueur, " ; malus_proximite_joueur : ", malus_proximite_joueur)

    print("\n Score_adv : ", score_adv, " ; Malus_adv : ", malus_adv, " ; Bonus_position_adv : ", bonus_position_adv)
    print("Bonus_agressif_adv : ", bonus_agressif_adv, " ; Bonus_soutien_adv : ", bonus_soutien_adv," ; Bonus_mobilite_adv : ", bonus_mobilite_adv)
    print("Score_div_adv : ", score_div_adv, " ; malus_proximite_adv : ", malus_proximite_adv)

    # DEBUG

    if mode_jeu==3 :
        score_allies_pour_roi_joueur = calcul_roi_protege(jeu, couleur_joueur)
        score_allies_pour_roi_adv = calcul_roi_protege(jeu, couleur_adv)
        eval_joueur+=score_allies_pour_roi_joueur*pond_proximite_roi
        eval_adv+=score_allies_pour_roi_adv*pond_proximite_roi

        # DEBUG
        print("\nScore_allies_pour_roi_joueur : ", score_allies_pour_roi_joueur)
        print("Score_allies_pour_roi_adv : ", score_allies_pour_roi_adv)
        # DEBUG

    print("\nScore_total_joueur : ", eval_joueur)
    print("Score_total_adv : ", eval_adv)

    return eval_joueur - eval_adv

def valMaxPlacement3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2, alpha, beta, profondeur):
    """
        Fonction recursive appelée par Machine
    """
    lesCoups = coups_possibles_placements(jeu)
    if (profondeur==0) or (len(pieces_ia1) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia1=", pieces_ia1) # DEBUG
        return evaluer_placement3(jeu, mode_jeu, couleur_ia1), '-f', '-f'
    """
        Algorithme :: PVH
        Hypothèse : score en deçà du minimum
        Vérification : à chaque coup, màj de scoreMax et coupMax si besoin
    """

    scoreMax = -math.inf
    coupMax = -math.inf
    pieceMax='.'
    for coup in lesCoups:
        for piece in pieces_ia1:
            if (mode_jeu!=3) or (len(pieces_ia1)<4) or (piece[1:]=="RR"): # Si on est pas en mode 3 OU qu'on a moins de 4 pieces a poser OU qu'on veut poser le Roi, alors on teste
                nouvellesPieces=pieces_ia1.copy()
                nouveauJeu = placer_piece_placement(piece, coup, jeu)
                nouvellesPieces.remove(piece)
                if (mode_jeu!=3) or (not roi_adverse_en_echec(nouveauJeu, couleur_ia2,pieces_ia2) and not roi_adverse_en_echec(nouveauJeu, couleur_ia1, nouvellesPieces)): # Si on est pas en mode 3 OU qu'on ne met pas le roi adverse en echec ET que le mien non plus, alors
                    score, _, _ = valMinPlacement3(nouveauJeu, mode_jeu, couleur_ia2, couleur_ia1, pieces_ia2, nouvellesPieces, alpha, beta, profondeur-1)
                    # DEBUG
                    # print("COUP MAX testé : ", coup, "\t Piece MAX testée : ", piece)
                    # print("\nPlateau MAX : ")
                    # afficher(nouveauJeu)
                    # print("Score MAX : ", score)
                    # DEBUG

                    if score > scoreMax:
                        scoreMax = score
                        coupMax = coup
                        pieceMax = piece

                    if score > beta:
                        return score, coup, piece

                    alpha = max(alpha, score)

    return scoreMax, coupMax, pieceMax


def valMinPlacement3(jeu, mode_jeu, couleur_ia2, couleur_ia1, pieces_ia2, pieces_ia1, alpha, beta, profondeur):
    """
        Fonction recursive simulant le coup joué par ia2
        Puisque M cherche à maximiser son score pour gagner
    """

    lesCoups = coups_possibles_placements(jeu)
    if (profondeur == 0) or (len(pieces_ia2) == 0) or (len(lesCoups) == 0):
        # print("pieces_ia2=",pieces_ia2) # DEBUG
        return evaluer_placement3(jeu, mode_jeu, couleur_ia2), '-f', '-f'

    """
      Algorithme :: PVH
      Hypothèse : score en deçà du minimum
      Vérification : à chaque coup, màj de scoreMin et coupMin si besoin
    """
    scoreMin = +math.inf
    coupMin = +math.inf
    pieceMin = '.'

    for coup in lesCoups:
        for piece in pieces_ia2:
            if (mode_jeu != 3) or (len(pieces_ia2) < 4) or (piece[1:] == "RR"):  # Si on est pas en mode 3 OU qu'on a moins de 4 pieces a poser OU qu'on veut poser le Roi, alors on teste
                nouvellesPieces = pieces_ia2.copy()
                nouveauJeu = placer_piece_placement(piece, coup, jeu)
                nouvellesPieces.remove(piece)
                if (mode_jeu != 3) or (not roi_adverse_en_echec(nouveauJeu, couleur_ia1,pieces_ia1)  and not roi_adverse_en_echec(nouveauJeu, couleur_ia2, nouvellesPieces)):  # Si on est pas en mode 3 OU qu'on ne met pas le roi adverse en echec ET que le mien non plus, alors
                    score, _, _ = valMaxPlacement3(nouveauJeu, mode_jeu,couleur_ia1, couleur_ia2, pieces_ia1, nouvellesPieces, alpha, beta, profondeur-1)

                    # DEBUG
                    # print("COUP MIN testé : ", coup, "\t Piece MIN testée : ",piece)
                    # print("\nPlateau MIN : ")
                    # afficher(nouveauJeu)
                    # print("Score MIN : ", score)
                    # DEBUG

                    if score < scoreMin:
                        scoreMin = score
                        coupMin = coup
                        pieceMin = piece

                    if alpha >= score:
                        return score, coup, piece

                    beta = min(beta, score)
    return scoreMin, coupMin, pieceMin


def lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    best_score, best_pos, best_piece = valMaxPlacement3(jeu, mode_jeu,couleur_ia1,couleur_ia2, pieces_ia1, pieces_ia2, -math.inf, +math.inf, profondeur=3)
    if best_pos == '-f' or best_piece == '-f':
        return
    jeu = placer_piece_placement(best_piece, best_pos, jeu)
    pieces_ia1.remove(best_piece)
    return jeu