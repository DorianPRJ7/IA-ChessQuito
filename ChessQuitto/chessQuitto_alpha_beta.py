def nouveau_jeu():
    return [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.']
    ]


def traduire_position(colonne, ligne):
    # Colonne B Ligne 3 -> Indice 1 2,
    indice_col = Colonnes.index(colonne)
    indice_lig = Lignes.index(ligne)
    return indice_col, indice_lig


def afficher(jeu):
    print("  A B C D")
    print("1", jeu[0][0], jeu[0][1], jeu[0][2], jeu[0][3])
    print("2", jeu[1][0], jeu[1][1], jeu[1][2], jeu[1][3])
    print("3", jeu[2][0], jeu[2][1], jeu[2][2], jeu[2][3])
    print("4", jeu[3][0], jeu[3][1], jeu[3][2], jeu[3][3])


def jouer():
    jeu = nouveau_jeu()
    afficher(jeu)


Colonnes = ['A', 'B', 'C', 'D']
Lignes = ['1', '2', '3', '4']
jouer()