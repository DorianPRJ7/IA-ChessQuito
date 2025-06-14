from IA1 import *
from IA2 import *
from IA3 import *
from utilitaires import *

############## PLACEMENT ##############
def phase_de_placement_IA1_vs_IA2(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        if couleur_ia1== 'BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_ia2, pieces_noires=pieces_ia1)

        if tour == couleur_ia1 :
            print("\n\t*********** TOUR IA1 ***********\n")
            print("Pieces a placer => ", pieces_ia1, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
        else :
            print("\n\t*********** TOUR IA2 ***********\n")
            print("Pieces a placer => ", pieces_ia2, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu

def phase_de_placement_IA1_vs_IA3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        if couleur_ia1== 'BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_ia2, pieces_noires=pieces_ia1)

        if tour == couleur_ia1 :
            print("\n\t*********** TOUR IA1 ***********\n")
            print("Pieces a placer => ", pieces_ia1, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
        else :
            print("\n\t*********** TOUR IA3 ***********\n")
            print("Pieces a placer => ", pieces_ia2, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu

def phase_de_placement_IA2_vs_IA3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        if couleur_ia1== 'BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_ia2, pieces_noires=pieces_ia1)

        if tour == couleur_ia1 :
            print("\n\t*********** TOUR IA2 ***********\n")
            print("Pieces a placer => ", pieces_ia1, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
        else :
            print("\n\t*********** TOUR IA3 ***********\n")
            print("Pieces a placer => ", pieces_ia2, "\n")
            afficher(jeu)
            jeu=lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)

        # Affiche l'etat du jeu
        print("\n\t*********** FIN DU TOUR ***********\n")
        afficher(jeu)

    print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


############## JEU ##############
def jouer(IA1, IA2, mode_jeu, couleur_ia1, couleur_ia2):
    nom_fichier ="log"+IA1+"_"+couleur_ia1+"_vs_"+IA2+"_"+couleur_ia2+"_mode"+str(mode_jeu)+".txt"
    activer_logs_dans_fichier(nom_fichier)

    print("\n\t*********** MODE ", mode_jeu," : IA1 : ", couleur_ia1, ", IA2 : ", couleur_ia2," ***********\n")

    # Definit qui joue quelle couleur ainsi que leurs pieces en fonction du mode de jeu
    if couleur_ia1 == 'BLANCS' :
        pieces_ia1, pieces_ia2 = creer_pieces(mode_jeu)
    else:
        pieces_ia2, pieces_ia1 = creer_pieces(mode_jeu)

    print("\n\t*********** DEBUT DES PLACEMENTS ***********\n")
    print("Mode de Jeu -> ","1 : REINE" if mode_jeu == 1 else "2 : REINE_PION" if mode_jeu == 2 else "3 : REINE_ROI")
    print(f"L'IA1 est ", couleur_ia1, "\t|\tl'IA2 est ", couleur_ia2, "\n")
    print("\nPIECES IA1 = ", pieces_ia1, "\t|\tPIECES IA2 = ", pieces_ia2, "\n")

    # Definit le plateau de jeu
    jeu = nouveau_jeu()
    afficher(jeu)

    # Demarre la phase de placement
    if IA1=='IA1' and IA2=='IA2':
        jeu=phase_de_placement_IA1_vs_IA2(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
    elif IA1=='IA1' and IA2=='IA3':
        jeu=phase_de_placement_IA1_vs_IA3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
    elif IA1=='IA2' and IA2=='IA3':
        jeu=phase_de_placement_IA2_vs_IA3(jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())

    print("\n\t*********** FIN DES PLACEMENTS ***********\n")
    print("\t*********** EVALUATION DU PLATEAU FINAL ***********\n")
    print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
    print("Score Final IA2 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
    print("Plateau final :\n")
    afficher(jeu)

    reset_terminal()


Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']

# IA1 VS IA2
jouer("IA1","IA2",1, "BLANCS", "NOIRS")
jouer("IA1","IA2",1, "NOIRS", "BLANCS")
jouer("IA1","IA2",2, "BLANCS", "NOIRS")
jouer("IA1","IA2",2, "NOIRS", "BLANCS")
jouer("IA1","IA2",3, "BLANCS", "NOIRS")
jouer("IA1","IA2",3, "NOIRS", "BLANCS")

# IA1 VS IA3
jouer("IA1","IA3",1, "BLANCS", "NOIRS")
jouer("IA1","IA3",1, "NOIRS", "BLANCS")
jouer("IA1","IA3",2, "BLANCS", "NOIRS")
jouer("IA1","IA3",2, "NOIRS", "BLANCS")
jouer("IA1","IA3",3, "BLANCS", "NOIRS")
jouer("IA1","IA3",3, "NOIRS", "BLANCS")

#IA2 VS IA3
jouer("IA2","IA3",1, "BLANCS", "NOIRS")
jouer("IA2","IA3",1, "NOIRS", "BLANCS")
jouer("IA2","IA3",2, "BLANCS", "NOIRS")
jouer("IA2","IA3",2, "NOIRS", "BLANCS")
jouer("IA2","IA3",3, "BLANCS", "NOIRS")
jouer("IA2","IA3",3, "NOIRS", "BLANCS")