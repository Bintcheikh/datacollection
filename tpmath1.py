# 1. Fonction de saisie d'une matrice
def saisir_matrix():
    lignes = int(input("Entrez le nombre de lignes : "))
    colonnes = int(input("Entrez le nombre de colonnes : "))

    matrice = []
    for i in range(lignes):
        ligne = []
        for j in range(colonnes):
            val = int(input(f"Element [{i+1}][{j+1}] : "))
            ligne.append(val)
        matrice.append(ligne)

    return matrice


# 2. Fonction de produit de deux matrices
def Produit_matrix(A, B):
    if len(A[0]) != len(B):
        print("Produit impossible : dimensions incompatibles")
        return None

    C = []
    for i in range(len(A)):
        ligne = []
        for j in range(len(B[0])):
            somme = 0
            for k in range(len(B)):
                somme += A[i][k] * B[k][j]   # formule mathématique
            ligne.append(somme)
        C.append(ligne)

    return C


# 3. Fonction de transposée d'une matrice
def Transpose_matrix(M):
    T = []
    for j in range(len(M[0])):
        ligne = []
        for i in range(len(M)):
            ligne.append(M[i][j])
        T.append(ligne)

    return T


# 4. Fonction principale du projet
def Projet_DIT():
    print("Choisissez une option :")
    print("1 : Calculer le transposé d'une matrice")
    print("2 : Calculer le produit de deux matrices")

    choix = int(input("Votre choix : "))

    if choix == 1:
        print("\nSaisie de la matrice")
        M = saisir_matrix()
        T = Transpose_matrix(M)
        print("\nTransposée de la matrice :")
        for ligne in T:
            print(ligne)

    elif choix == 2:
        print("\nSaisie de la première matrice")
        A = saisir_matrix()
        print("\nSaisie de la deuxième matrice")
        B = saisir_matrix()

        P = Produit_matrix(A, B)
        if P:
            print("\nProduit des deux matrices :")
            for ligne in P:
                print(ligne)

    else:
        print("Choix invalide")


# Lancement du programme
Projet_DIT()
