import numpy as np
import pygame

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

# Initialiser le plateau de jeu avec des zéros pour représenter les cases vides, j'ai mis des dimensions de 10,10
#pour éviter le "out of bands" quand un pion en bordure peut manger un pion
plateau = np.zeros((10, 10), dtype=int)

# Placer les pions sur le plateau, les rouges en haut du plateau et bleus en bas
for i in range(1, 8, 2):
    for j in range(0, 3, 2):
        plateau[j][i] = 1 # Le "1" représente les pions rouges

for i in range(0, 8, 2):
    for j in range(1, 8, 7):
        plateau[j][i] = 1 

for i in range(0, 8, 2):
    for j in range(0, 3, 2):
        plateau[7-j][i] = 2 # Le "2" représente les pions bleus

for i in range(1, 8, 2):
    for j in range(6, 8, 2):
        plateau[j][i] = 2

pygame.init()
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Dames")

def dessiner_plateau():
    for i in range(8):
        for j in range(8):
            couleur_case = blanc if (i + j) % 2 == 0 else noir
            pygame.draw.rect(fenetre, couleur_case, (j * taille_case, i * taille_case, taille_case, taille_case))

def dessiner_pions():
    for i in range(8):
        for j in range(8):
            if plateau[i, j] == 1:
                pygame.draw.circle(fenetre, rouge, (j * taille_case + taille_case // 2, i * taille_case + taille_case // 2), taille_case // 2 - 5)
            elif plateau[i, j] == 2:
                pygame.draw.circle(fenetre, bleu, (j * taille_case + taille_case // 2, i * taille_case + taille_case // 2), taille_case // 2 - 5)

def deplacements_valides(pion): # Fonction qui détermine les positions où le pion peut être déplacé
    deplacements = []
    if pion.couleur == 1:
        if pion.ligne >= 0:
            if plateau[pion.ligne + 1, pion.colonne + 1] == 0:
                deplacements.append((pion.ligne + 1, pion.colonne + 1))
            if plateau[pion.ligne + 1, pion.colonne - 1] == 0:
                deplacements.append((pion.ligne + 1, pion.colonne - 1))
    elif pion.couleur == 2:
        if pion.ligne <= 7:
            if plateau[pion.ligne - 1, pion.colonne + 1] == 0:
                deplacements.append((pion.ligne - 1, pion.colonne + 1))
            if plateau[pion.ligne - 1, pion.colonne - 1] == 0:
                deplacements.append((pion.ligne - 1, pion.colonne - 1))
    return deplacements

def manger_un_pion(pion):  # Fonction qui détermine les positions où le pion peut en manger un adverse
    deplacements_pour_manger = []
    if pion.couleur == 1:
        if pion.ligne >= 0:
            if plateau[pion.ligne + 1, pion.colonne + 1] == 2 and plateau[pion.ligne + 2, pion.colonne + 2] == 0:
                deplacements_pour_manger.append((pion.ligne + 2, pion.colonne + 2))
            if plateau[pion.ligne + 1, pion.colonne - 1] == 2 and plateau[pion.ligne + 2, pion.colonne - 2] == 0:
                deplacements_pour_manger.append((pion.ligne + 2, pion.colonne - 2))
    if pion.couleur == 2:
        if pion.ligne <= 7:
            if plateau[pion.ligne - 1, pion.colonne + 1] == 1 and plateau[pion.ligne - 2, pion.colonne + 2] == 0:
                deplacements_pour_manger.append((pion.ligne - 2, pion.colonne + 2))
            if plateau[pion.ligne - 1, pion.colonne - 1] == 1 and plateau[pion.ligne - 2, pion.colonne - 2] == 0:
                deplacements_pour_manger.append((pion.ligne - 2, pion.colonne - 2))
    return deplacements_pour_manger

pion_selectionne = None

en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            ligne, colonne = y // taille_case, x // taille_case

            if pion_selectionne is None and plateau[ligne, colonne] != 0:
                pion_selectionne = Pion(plateau[ligne, colonne], ligne, colonne)
            elif pion_selectionne is not None :
                if pion_selectionne.ligne == ligne and pion_selectionne.colonne == colonne:
                    pion_selectionne = None             
                else :
                    dest_ligne, dest_colonne = ligne, colonne
                    if (dest_ligne, dest_colonne) in deplacements_valides(pion_selectionne):
                        plateau[dest_ligne, dest_colonne] = plateau[pion_selectionne.ligne, pion_selectionne.colonne]
                        plateau[pion_selectionne.ligne, pion_selectionne.colonne] = 0
                        pion_selectionne = None
                    elif (dest_ligne, dest_colonne) in manger_un_pion(pion_selectionne):
                        plateau[dest_ligne, dest_colonne] = plateau[pion_selectionne.ligne, pion_selectionne.colonne]
                        plateau[pion_selectionne.ligne, pion_selectionne.colonne] = 0
                        if plateau[dest_ligne, dest_colonne] == plateau[pion_selectionne.ligne + 2, pion_selectionne.colonne + 2]:
                            plateau[pion_selectionne.ligne + 1, pion_selectionne.colonne + 1] = 0
                        if plateau[dest_ligne, dest_colonne] == plateau[pion_selectionne.ligne + 2, pion_selectionne.colonne - 2]:
                            plateau[pion_selectionne.ligne + 1, pion_selectionne.colonne - 1] = 0
                        if plateau[dest_ligne, dest_colonne] == plateau[pion_selectionne.ligne - 2, pion_selectionne.colonne + 2]:
                            plateau[pion_selectionne.ligne - 1, pion_selectionne.colonne + 1] = 0
                        if plateau[dest_ligne, dest_colonne] == plateau[pion_selectionne.ligne - 2, pion_selectionne.colonne - 2]:
                            plateau[pion_selectionne.ligne - 1, pion_selectionne.colonne - 1] = 0
                        pion_selectionne = None
                   
            
    fenetre.fill(blanc)
    dessiner_plateau()
    dessiner_pions()
    
    if pion_selectionne is not None:
        for deplacement in deplacements_valides(pion_selectionne):
            if pion_selectionne.couleur == 1:
                pygame.draw.circle(fenetre, rouge, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)            
            if pion_selectionne.couleur == 2:
                pygame.draw.circle(fenetre, bleu, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)
        for deplacement in manger_un_pion(pion_selectionne):
            if pion_selectionne.couleur == 1:
                pygame.draw.circle(fenetre, rouge, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)
            if pion_selectionne.couleur == 2:
                pygame.draw.circle(fenetre, bleu, (deplacement[1] * taille_case + taille_case // 2, deplacement[0] * taille_case + taille_case // 2), taille_case // 4)
    
    
    pygame.display.flip()

pygame.quit()