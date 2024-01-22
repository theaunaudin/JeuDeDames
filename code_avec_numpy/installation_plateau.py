import numpy as np
import pygame

# Définition des constantes
largeur = 400
hauteur = 400
taille_case = largeur // 8
blanc = (255, 255, 255)
noir = (0, 0, 0)
rouge = (255, 0, 0)
bleu = (0, 128, 255)

class Pion:
    def __init__(self, couleur, ligne, colonne):
        self.couleur = couleur
        self.ligne = ligne
        self.colonne = colonne

# Initialiser le plateau de jeu avec des zéros pour représenter les cases vides
plateau = np.zeros((8, 8), dtype=int)

# Placer les pions sur le plateau
for i in range(1, 8, 2):
    for j in range(0, 3, 2):
        plateau[j][i] = 1

for i in range(0, 8, 2):
    for j in range(1, 8, 7):
        plateau[j][i] = 1

for i in range(0, 8, 2):
    for j in range(0, 3, 2):
        plateau[7-j][i] = 2

for i in range(1, 8, 2):
    for j in range(6, 8, 2):
        plateau[j][i] = 2

# Initialiser Pygame
pygame.init()
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Dames")

# Fonction pour dessiner le plateau
def dessiner_plateau():
    for i in range(8):
        for j in range(8):
            couleur_case = blanc if (i + j) % 2 == 0 else noir
            pygame.draw.rect(fenetre, couleur_case, (j * taille_case, i * taille_case, taille_case, taille_case))

# Fonction pour dessiner les pions
def dessiner_pions():
    for i in range(8):
        for j in range(8):
            if plateau[i, j] == 1:
                pygame.draw.circle(fenetre, rouge, (j * taille_case + taille_case // 2, i * taille_case + taille_case // 2), taille_case // 2 - 5)
            elif plateau[i, j] == 2:
                pygame.draw.circle(fenetre, bleu, (j * taille_case + taille_case // 2, i * taille_case + taille_case // 2), taille_case // 2 - 5)

def deplacements_valides(pion):
    deplacements = []
    # Exemple simple : autoriser le déplacement vers le haut pour tous les pions
    if pion.couleur == 1:  # Pions rouges
        if pion.ligne > 0:
            deplacements.append((pion.ligne + 1, pion.colonne + 1))
            deplacements.append((pion.ligne + 1, pion.colonne - 1))
    elif pion.couleur == 2:  # Pions bleus
        if pion.ligne < 7:
            deplacements.append((pion.ligne - 1, pion.colonne + 1))
            deplacements.append((pion.ligne - 1, pion.colonne - 1))
    return deplacements

pion_selectionne = None

# Boucle principale
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Gestion du clic de la souris
            x, y = event.pos
            ligne, colonne = y // taille_case, x // taille_case

            if pion_selectionne is None and plateau[ligne, colonne] != 0:
                # Si aucun pion n'est sélectionné et la case contient un pion, le sélectionner
                pion_selectionne = Pion(plateau[ligne, colonne], ligne, colonne)
            elif pion_selectionne is not None:
                # Si un pion est déjà sélectionné, déplacer le pion vers la case cliquée
                dest_ligne, dest_colonne = ligne, colonne
                if (dest_ligne, dest_colonne) in deplacements_valides(pion_selectionne):
                    plateau[dest_ligne, dest_colonne] = plateau[pion_selectionne.ligne, pion_selectionne.colonne]
                    plateau[pion_selectionne.ligne, pion_selectionne.colonne] = 0
                pion_selectionne = None

    fenetre.fill(blanc)
    dessiner_plateau()
    dessiner_pions()
    
    # Dessiner des cercles bleus autour des cases valides pour le déplacement
    if pion_selectionne is not None:
        for deplacement in deplacements_valides(pion_selectionne):
            if pion_selectionne.couleur == 1:
                pygame.draw.circle(fenetre, rouge, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)
            if pion_selectionne.couleur == 2:
                pygame.draw.circle(fenetre, bleu, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)

    pygame.display.flip()

pygame.quit()