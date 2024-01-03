import pygame

# Initialisation de Pygame
pygame.init()

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 128, 255)
VERT = (0, 128, 0)

# Taille de la fenêtre
largeur_fenetre = 400
hauteur_fenetre = 400

# Taille d'une case du plateau
taille_case = largeur_fenetre // 8

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu de Dames")

# Classe Piece
class Piece:
    def __init__(self, couleur, x, y):
        self.couleur = couleur
        self.x = x
        self.y = y

# Initialisation du plateau
plateau = [[None] * 8 for _ in range(8)]

# Placement initial des pièces (exemples)
for i in range(0, 8, 2):
    for j in range(3):
        plateau[j][i] = Piece(BLEU, j, i)
        plateau[7-j][i] = Piece(VERT, j, i)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Remplace sys.exit()

    # Dessin du plateau
    fenetre.fill(BLANC)

    for ligne in range(8):
        for colonne in range(8):
            couleur_case = BLANC if (ligne + colonne) % 2 == 0 else NOIR
            pygame.draw.rect(fenetre, couleur_case, (colonne * taille_case, ligne * taille_case, taille_case, taille_case))

            piece = plateau[ligne][colonne]
            if piece:
                couleur_piece = piece.couleur
                pygame.draw.circle(fenetre, couleur_piece, (colonne * taille_case + taille_case // 2, ligne * taille_case + taille_case // 2), taille_case // 2 - 5)

    pygame.display.flip()
    pygame.time.delay(10)