from IA1 import *
from IA2 import *
from IA3 import *
from IA4 import *
from utilitaires import *

############## PLACEMENT ##############
def phase_de_placement_IA1_vs_IA2(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        if couleur_ia1 == 'BLANCS':
            tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)
        else:
            tour=determiner_tour_placement(pieces_blanches=pieces_ia2, pieces_noires=pieces_ia1)

        if tour == couleur_ia1:
            print("\n\t*********** TOUR",ia1,"***********\n")
            print("Pieces a placer => ", pieces_ia1, "\n")
            afficher(jeu)
            if ia1=='IA1' :
                jeu=lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            print("\n\t*********** TOUR",ia2,"***********\n")
            print("Pieces a placer => ", pieces_ia2, "\n")
            afficher(jeu)
            if ia2 == 'IA1':
                jeu = lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia2[0],couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia2[0],couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu

def phase_de_placement_IA1_vs_IA3(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)

        if tour == couleur_ia1:
            # print("\n\t*********** TOUR IA1 ***********\n")
            # print("Pieces a placer => ", pieces_ia1, "\n")
            # afficher(jeu)
            if ia1=='IA1' :
                jeu=lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            # print("\n\t*********** TOUR IA2 ***********\n")
            # print("Pieces a placer => ", pieces_ia2, "\n")
            # afficher(jeu)
            if ia2 == 'IA1':
                jeu = lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


def phase_de_placement_IA1_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)

        if tour == couleur_ia1:
            # print("\n\t*********** TOUR IA1 ***********\n")
            # print("Pieces a placer => ", pieces_ia1, "\n")
            # afficher(jeu)
            if ia1=='IA1' :
                jeu=lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            # print("\n\t*********** TOUR IA2 ***********\n")
            # print("Pieces a placer => ", pieces_ia2, "\n")
            # afficher(jeu)
            if ia2 == 'IA1':
                jeu = lancer_tour_placement_ia1(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


def phase_de_placement_IA2_vs_IA3(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)

        if tour == couleur_ia1:
            # print("\n\t*********** TOUR IA1 ***********\n")
            # print("Pieces a placer => ", pieces_ia1, "\n")
            # afficher(jeu)
            if ia1=='IA2' :
                jeu=lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            # print("\n\t*********** TOUR IA2 ***********\n")
            # print("Pieces a placer => ", pieces_ia2, "\n")
            # afficher(jeu)
            if ia2 == 'IA2':
                jeu = lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu

def phase_de_placement_IA2_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)

        if tour == couleur_ia1:
            # print("\n\t*********** TOUR IA1 ***********\n")
            # print("Pieces a placer => ", pieces_ia1, "\n")
            # afficher(jeu)
            if ia1=='IA2' :
                jeu=lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            # print("\n\t*********** TOUR IA2 ***********\n")
            # print("Pieces a placer => ", pieces_ia2, "\n")
            # afficher(jeu)
            if ia2 == 'IA2':
                jeu = lancer_tour_placement_ia2(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


def phase_de_placement_IA3_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1, pieces_ia2):
    # print("\n\t*********** DEBUT DE PHASE DE PLACEMENT ***********\n")

    while len(pieces_ia1) > 0 or len(pieces_ia2) > 0 :
        tour=determiner_tour_placement(pieces_blanches=pieces_ia1, pieces_noires=pieces_ia2)

        if tour == couleur_ia1:
            # print("\n\t*********** TOUR IA1 ***********\n")
            # print("Pieces a placer => ", pieces_ia1, "\n")
            # afficher(jeu)
            if ia1=='IA3' :
                jeu=lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)
            else:
                jeu=lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia1[0], couleur_ia2[0], pieces_ia1, pieces_ia2)

        else :
            # print("\n\t*********** TOUR IA2 ***********\n")
            # print("Pieces a placer => ", pieces_ia2, "\n")
            # afficher(jeu)
            if ia2 == 'IA3':
                jeu = lancer_tour_placement_ia3(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
            else:
                jeu = lancer_tour_placement_ia4(jeu, mode_jeu, couleur_ia2[0], couleur_ia1[0], pieces_ia2, pieces_ia1)
        # Affiche l'etat du jeu
        # print("\n\t*********** FIN DU TOUR ***********\n")
        # afficher(jeu)

    # print("\n\t*********** FIN DE PHASE DE PLACEMENT ***********\n")
    return jeu


############## PHASE DE JEU ##############
def phase_de_jeu_IA1_vs_IA2(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA2':
                jeu, prise = lancer_tour_jeu_ia2(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA2':
                jeu, prise = lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


def phase_de_jeu_IA1_vs_IA3(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA3':
                jeu, prise = lancer_tour_jeu_ia3(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA3':
                jeu, prise = lancer_tour_jeu_ia3(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu

def phase_de_jeu_IA1_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia1(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


def phase_de_jeu_IA2_vs_IA3(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA3':
                jeu, prise = lancer_tour_jeu_ia3(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA3':
                jeu, prise = lancer_tour_jeu_ia3(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


def phase_de_jeu_IA2_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia2(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


def phase_de_jeu_IA3_vs_IA4(ia1,ia2,jeu, mode_jeu, couleur_ia1, couleur_ia2):
    # print("\n\t*********** DÉBUT DE PHASE DE JEU ***********\n")
    # afficher(jeu)
    tour = 'BLANCS'
    sans_prise = 0
    estTermine=False
    while not estTermine:
        # print(f"Tour actuel : ", tour)
        if tour==couleur_ia2:
            if ia2=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu,mode_jeu,sans_prise, couleur_ia2[0], couleur_ia1[0])
            else:
                jeu, prise = lancer_tour_jeu_ia3(jeu, mode_jeu, sans_prise, couleur_ia2[0], couleur_ia1[0])
        else:
            if ia1=='IA4':
                jeu, prise = lancer_tour_jeu_ia4(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])
            else:
                jeu, prise = lancer_tour_jeu_ia3(jeu, mode_jeu, sans_prise, couleur_ia1[0], couleur_ia2[0])

        # afficher(jeu)

        if prise:
            sans_prise = 0
        else:
            sans_prise += 1

        if tour=='BLANCS':
            tour='NOIRS'
        else:
            tour='BLANCS'

        estTermine=verifierFinPartie(mode_jeu, jeu, sans_prise)

    # print("\n\t*********** FIN DE PARTIE ***********\n")
    return jeu


############## JEU ##############
def jouer(IA1, IA2, mode_jeu, couleur_ia1, couleur_ia2):
    nom_fichier ="log"+IA1+"_"+couleur_ia1+"_vs_"+IA2+"_"+couleur_ia2+"_mode"+str(mode_jeu)+".txt"
    activer_logs_dans_fichier(nom_fichier)

    print("\n\t*********** MODE", mode_jeu,":,",IA1,":", couleur_ia1, "-",IA2,":", couleur_ia2,"***********\n")

    # Definit qui joue quelle couleur ainsi que leurs pieces en fonction du mode de jeu
    if couleur_ia1 == 'BLANCS' :
        pieces_ia1, pieces_ia2 = creer_pieces(mode_jeu)
    else:
        pieces_ia2, pieces_ia1 = creer_pieces(mode_jeu)

    # print("\n\t*********** DEBUT DU JEU ***********\n")
    print("Mode de Jeu -> ","1 : REINE" if mode_jeu == 1 else "2 : REINE_PION" if mode_jeu == 2 else "3 : REINE_ROI")
    print(f"L'",IA1,"est", couleur_ia1, "\t|\tl'",IA2 ,"est", couleur_ia2, "\n")
    # print("\nPIECES IA1 = ", pieces_ia1, "\t|\tPIECES IA2 = ", pieces_ia2, "\n")

    # Definit le plateau de jeu
    jeu = nouveau_jeu()
    ## afficher(jeu)

    # Demarre la phase de placement
    if (IA1=='IA1' or IA1=='IA2') and (IA2=='IA1' or IA2=='IA2'):
        print(IA1,IA2)
        jeu=phase_de_placement_IA1_vs_IA2(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA2 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA1_vs_IA2(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA2 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    elif (IA1=='IA1' or IA1=='IA3') and (IA2=='IA1' or IA2=='IA3'):

        jeu=phase_de_placement_IA1_vs_IA3(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA3 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA1_vs_IA3(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA3 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    elif (IA1=='IA1' or IA1=='IA4') and (IA2=='IA1' or IA2=='IA4'):

        jeu=phase_de_placement_IA1_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA1_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA1 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    elif (IA1=='IA2' or IA1=='IA3') and (IA2=='IA2' or IA2=='IA3'):

        jeu=phase_de_placement_IA2_vs_IA3(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA2 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA3 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA2_vs_IA3(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA2 : ", evaluer_placement1(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA3 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    elif (IA1=='IA2' or IA1=='IA4') and (IA2=='IA2' or IA2=='IA4'):

        jeu=phase_de_placement_IA2_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA2 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA2_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA2 : ", evaluer_placement2(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    elif (IA1=='IA3' or IA1=='IA4') and (IA2=='IA3' or IA2=='IA4'):

        jeu=phase_de_placement_IA3_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2, pieces_ia1.copy(), pieces_ia2.copy())
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE PLACEMENT ***********\n")
        # print("Score Final IA3 : ", evaluer_placement3(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau fin de placement :\n")
        afficher(jeu)

        jeu=phase_de_jeu_IA3_vs_IA4(IA1, IA2, jeu, mode_jeu, couleur_ia1, couleur_ia2)
        # print("\t*********** EVALUATION DU PLATEAU EN FIN DE PHASE DE JEU ***********\n")
        # print("Score Final IA3 : ", evaluer_placement3(jeu, mode_jeu, couleur_ia1))
        # print("Score Final IA4 : ", evaluer_placement4(jeu, mode_jeu, couleur_ia2))
        print("Plateau final :\n")
        afficher(jeu)

    victoire, typeVictoire=determiner_victoire(jeu,mode_jeu)
    if couleur_ia1=='BLANCS':
        score_ia1,score_ia2=calcul_score_plateau(jeu)
    else:
        score_ia1,score_ia2=calcul_score_plateau(jeu)

    reset_terminal()

    return victoire, typeVictoire, score_ia1, score_ia2


def afficher_tab_score(nbPhase,tab_score):
    nomFichier="resultats_des_matchs_phase"+str(nbPhase)+".txt"
    activer_logs_dans_fichier(nomFichier)

    for i in range(len(tab_score)):
        nbMatch=i+1
        ligne=tab_score[i]
        ia1=ligne[0]
        ia2=ligne[1]
        mode=ligne[2]
        victoire=ligne[3]
        typeVictoire=ligne[4]
        score_ia1=ligne[5]
        score_ia2=ligne[6]


        print("MATCH",nbMatch,"=> BLANCS :", ia1, ", NOIRS :", ia2, ", MODE :",mode)

        print("\tRESULTAT => Victoire par", typeVictoire,"de", ia1 if victoire=="BLANCS" else ia2 if victoire=='NOIRS' else victoire)
        print("SCORES PIECES RESTANTES => ", ia1, ":", score_ia1, ",", ia2, score_ia2)

    reset_terminal()


def determine_classement(tab_score):
    classement = {
        "IA1": [0.0, 0, 0],  # NomIA : [score, nbMatchs, nbVictoires]
        "IA2": [0.0, 0, 0],
        "IA3": [0.0, 0, 0],
        "IA4": [0.0, 0, 0]
    }

    for ligne in tab_score:
        ia_blancs, ia_noirs, mode, victoire, type_victoire, score_blancs, score_noirs = ligne
        case_ia_blanche=classement[ia_blancs]
        case_ia_noire=classement[ia_noirs]
        # Ajout des scores
        case_ia_blanche[0]+=score_blancs
        case_ia_noire[0]+=score_noirs

        case_ia_blanche[1]+=1
        case_ia_noire[1]+=1

        if victoire == "BLANCS":
            case_ia_blanche[2]+=1
        elif victoire == "NOIRS":
            case_ia_noire[2]+=1

    for ia in classement:
        score_total, nbMatchs, nbVictoires = classement[ia]
        if nbMatchs>0:
            score_moyen = score_total / nbMatchs
        else:
            score_moyen = 0
        classement[ia][0]=score_moyen

    return classement


def calcul_classement(classement):
    classement_ia = []

    pond_victoire = 0.5
    pond_score = 0.5

    for ia in classement:
        score_moyen, nbMatchs, nbVictoires = classement[ia]
        if nbMatchs>0:
            score_total=pond_victoire * (nbVictoires / nbMatchs) + pond_score * score_moyen
        else:
            score_total=0
        classement_ia+=[(ia,score_total)]


    return classement_ia

def faire_jouer_matchs():
# PHASE 1
    tab_score_phase1=[]
    for ia1 in IAS: # Pour chaque IA
        for ia2 in IAS: # Pour chaque IA différente de la première
            if ia1!=ia2:
                print("IA blancs =", ia1, "| IA noirs =", ia2)
                for mode in MODES: # Pour chaque mode
                    victoire, type_victoire, score_ia1, score_ia2=jouer(ia1, ia2, mode, "BLANCS", "NOIRS")
                    tab_score_phase1+=[(ia1, ia2, mode, victoire, type_victoire, score_ia1, score_ia2)]

    afficher_tab_score(1,tab_score_phase1)
    classement_ia_phase1=determine_classement(tab_score_phase1)
    classement_total_phase1=calcul_classement(classement_ia_phase1)
    print(classement_ia_phase1)
    classement_total_phase1=sorted(classement_total_phase1, key=lambda case: case[1], reverse=True)
    print(classement_total_phase1)

# PHASE 2
    tab_score_phase2=[]
    for mode in MODES: # Pour chaque mode
        for i in range(len(classement_total_phase1)):
            if i==0: # Match Meilleur de phase 1 Blanc vs Pire de phase 1 Noir
                ia1=classement_total_phase1[0][0]
                ia2=classement_total_phase1[3][0]
            elif i==1: # Match Moyen de phase 1 Blanc vs Moyen de phase 1 Noir
                ia1=classement_total_phase1[1][0]
                ia2=classement_total_phase1[2][0]
            elif i==2: # Match Moyen de phase 1 Noir vs Moyen de phase 1 Blanc
                ia1=classement_total_phase1[2][0]
                ia2=classement_total_phase1[1][0]
            else : # Match Meilleur de phase 1 Noir vs Pire de phase 1 Blanc
                ia1=classement_total_phase1[3][0]
                ia2=classement_total_phase1[0][0]
            print("IA blancs =", ia1, "| IA noirs =", ia2)
            victoire, type_victoire, score_ia1, score_ia2=jouer(ia1, ia2, mode, 'BLANCS','NOIRS' )
            tab_score_phase2+=[(ia1, ia2, mode, victoire, type_victoire, score_ia1, score_ia2)]

    afficher_tab_score(2, tab_score_phase2)
    classement_ia_phase2=determine_classement(tab_score_phase2)
    classement_total_phase2=calcul_classement(classement_ia_phase2)
    classement_total_phase2=sorted(classement_total_phase2, key=lambda x: x[1], reverse=True)
    print(classement_ia_phase2)
    print(classement_total_phase2)

    # Gagnants de phase 2
    finalistes=[classement_total_phase2[0][0], classement_total_phase2[1][0]]
    perdants=[classement_total_phase2[2][0], classement_total_phase2[3][0]]

    print(finalistes)
    print(perdants)
    # FINALE
    tab_score_finale = []
    for mode in MODES:
        ia1=finalistes[0]
        ia2=finalistes[1]

        print("IA blancs =", ia1, "| IA noirs =", ia2)
        victoire, type_victoire, score_ia1, score_ia2 = jouer(ia1, ia2, mode, 'BLANCS', 'NOIRS')
        tab_score_finale+=[(ia1, ia2, mode, victoire, type_victoire, score_ia1, score_ia2)]

        print("IA blancs =", ia2, "| IA noirs =", ia1)
        victoire, type_victoire, score_ia2, score_ia1 = jouer(ia2, ia1, mode, 'BLANCS', 'NOIRS')
        tab_score_finale+=[(ia2, ia1, mode, victoire, type_victoire, score_ia2, score_ia1)]

    afficher_tab_score(3, tab_score_finale)
    classement_ia_finale=determine_classement(tab_score_finale)
    classement_total_finale=calcul_classement(classement_ia_finale)
    classement_total_finale = sorted(classement_total_finale, key=lambda x: x[1], reverse=True)
    print(classement_ia_finale)
    print(classement_total_finale)


    # FINALE DES PERDANTS
    tab_score_perdants = []
    for mode in MODES:
        ia1=perdants[0]
        ia2=perdants[1]
        print("IA blancs =", ia1, "| IA noirs =", ia2)

        victoire, type_victoire, score_ia1, score_ia2 = jouer(ia1, ia2, mode, 'BLANCS', 'NOIRS')
        tab_score_perdants+=[(ia1, ia2, mode, victoire, type_victoire, score_ia1, score_ia2)]

        print("IA blancs =", ia2, "| IA noirs =", ia1)
        victoire, type_victoire, score_ia1, score_ia2 = jouer(ia2, ia1, mode, 'BLANCS', 'NOIRS')
        tab_score_perdants+=[(ia2, ia1, mode, victoire, type_victoire, score_ia1, score_ia2)]


    afficher_tab_score(4, tab_score_perdants)
    classement_ia_perdants = determine_classement(tab_score_perdants)
    classement_total_perdants =calcul_classement(classement_ia_perdants )
    classement_total_perdants = sorted(classement_total_perdants , key=lambda x: x[1], reverse=True)
    print(classement_ia_perdants)
    print(classement_total_perdants)


    # IA1 VS IA2
    # jouer("IA1", "IA2", 1, "BLANCS", "NOIRS")
    # jouer("IA1", "IA2", 1, "NOIRS", "BLANCS")
    # jouer("IA1", "IA2", 2, "BLANCS", "NOIRS")
    # jouer("IA1", "IA2", 2, "NOIRS", "BLANCS")
    # jouer("IA1", "IA2", 3, "BLANCS", "NOIRS")
    # jouer("IA1", "IA2", 3, "NOIRS", "BLANCS")

    # IA1 VS IA3
    # jouer("IA1", "IA3", 1, "BLANCS", "NOIRS")
    # jouer("IA1", "IA3", 1, "NOIRS", "BLANCS")
    # jouer("IA1", "IA3", 2, "BLANCS", "NOIRS")
    # jouer("IA1", "IA3", 2, "NOIRS", "BLANCS")
    # jouer("IA1", "IA3", 3, "BLANCS", "NOIRS")
    # jouer("IA1", "IA3", 3, "NOIRS", "BLANCS")

    # IA1 VS IA4
    # jouer("IA1", "IA4", 1, "BLANCS", "NOIRS")
    # jouer("IA1", "IA4", 1, "NOIRS", "BLANCS")
    # jouer("IA1", "IA4", 2, "BLANCS", "NOIRS")
    # jouer("IA1", "IA4", 2, "NOIRS", "BLANCS")
    # jouer("IA1", "IA4", 3, "BLANCS", "NOIRS")
    # jouer("IA1", "IA4", 3, "NOIRS", "BLANCS")

    # IA2 VS IA3
    # jouer("IA2", "IA3", 1, "BLANCS", "NOIRS")
    # jouer("IA2", "IA3", 1, "NOIRS", "BLANCS")
    # jouer("IA2", "IA3", 2, "BLANCS", "NOIRS")
    # jouer("IA2", "IA3", 2, "NOIRS", "BLANCS")
    # jouer("IA2", "IA3", 3, "BLANCS", "NOIRS")
    # jouer("IA2", "IA3", 3, "NOIRS", "BLANCS")

    # IA2 VS IA4
    # jouer("IA2", "IA4", 1, "BLANCS", "NOIRS")
    # jouer("IA2", "IA4", 1, "NOIRS", "BLANCS")
    # jouer("IA2", "IA4", 2, "BLANCS", "NOIRS")
    # jouer("IA2", "IA4", 2, "NOIRS", "BLANCS")
    # jouer("IA2", "IA4", 3, "BLANCS", "NOIRS")
    # jouer("IA2", "IA4", 3, "NOIRS", "BLANCS")

    # IA3 VS IA4
    # jouer("IA3", "IA4", 1, "BLANCS", "NOIRS")
    # jouer("IA3", "IA4", 1, "NOIRS", "BLANCS")
    # jouer("IA3", "IA4", 2, "BLANCS", "NOIRS")
    # jouer("IA3", "IA4", 2, "NOIRS", "BLANCS")
    # jouer("IA3", "IA4", 3, "BLANCS", "NOIRS")
    # jouer("IA3", "IA4", 3, "NOIRS", "BLANCS")


Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']
IAS = ['IA1','IA2','IA3','IA4']
MODES = [1,2,3]

faire_jouer_matchs()