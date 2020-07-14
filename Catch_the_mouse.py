'''
Ein Spiel, in dem der Spieler die Katze ist und alle Mäuse fangen muss bevor diese den Käse aufgefressen haben.
Sind alle Mäuse gefangen, erscheinen neue Mäuse. Sobald der ganze Käse aufgefressen worden ist, ist das Spiel vorbei.
'''
import pygame
import random

pygame.init()

# -------------------Konstanten ----------

# Definiert unterschiedliche RGB Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 165, 0)
GRAY = (207, 207, 207)


# -------------------Klassen ---------------------

class Cat(pygame.sprite.Sprite):
    '''Erstellt das Objekt Cat, Cat stellt die Figur des Spielers da.'''

    def __init__(self):
        '''Konstruktor erstellt image von Cat'''
        pygame.sprite.Sprite.__init__(self)
        ''' Erbt von der Klasse Sprite '''

        # Größe der Spielerfigur
        width = 40
        height = 40

        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)

        self.image = pygame.image.load('cat.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        # Fügt Cat zur Spirit Liste player und all Spirits hinzu
        player_list.add(self)
        all_sprites_list.add(self)


class Chees(pygame.sprite.Sprite):
    ''' Klasse erstellt ein Käsestück.'''

    def __init__(self):
        ''' Konstruktor erstellt Image von Käsestück'''
        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface([5, 5])
        # self.image.fill(YELLOW)

        # Zufällige Größe des Käsestückes
        size = (random.randrange(10, 30))

        self.image = pygame.image.load('chees.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()

    def drawALot(self):
        '''Methode erstellt mehrere Käsestücke'''

        # Erstellt die Anzahl von cheessPiece Käsestücken, und legt zufällige x und y Postionen fest.
        for i in range(cheessPiece):
            chees = Chees()
            chees.rect.x = random.randrange(50, screen_width - 50)
            chees.rect.y = random.randrange(50, screen_height - 50)
            chees_list.add(chees)
            all_sprites_list.add(chees)


class Mouse(pygame.sprite.Sprite):
    ''' Klasse erstellt eine Maus.
        Speed: legt die Geschwindigkeit, der Maus fest.'''

    def __init__(self, speed):
        '''Konstruktor erstellt image der Maus.'''
        pygame.sprite.Sprite.__init__(self)

        # self.image = pygame.Surface([10, 10])
        # self.image.fill(RED)

        self.image = pygame.image.load('mouse.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = ((random.randrange(10)), (random.randrange(20)))
        self.speed_x_position = speed
        self.speed_y_position = speed

    def update(self):
        """ Wird jede Frame aufgerufen, verändert die Position der Maus und prüft ob diese mit dem Rand zusammengestoßen ist."""
        self.rect.x += self.speed_x_position
        self.rect.y += self.speed_y_position

        # Prüft ob die Maus, mit dem Rand zusammengestoßen ist, wenn ja wird die Richtung geändert.
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.speed_x_position *= -1
        if self.rect.bottom >= screen_height or self.rect.top <= 0:
            self.speed_y_position *= -1

    def change(self):
        ''' Methode ändert die Richtung der Maus.'''
        self.speed_y_position = self.speed_x_position * (-1)
        self.speed_x_position = self.speed_x_position * (-1)

    def draw(self, piece, minSpeed, maxSpeed):
        '''Methode erstellt mehrere Mäuse.'''

        # Erstellt die Anzahl von piece Mäusen, und legt zufällige x und y Postionen fest.
        for i in range(piece):
            mouse = Mouse(random.randrange(minSpeed, maxSpeed))
            mouse.rect.x = random.randrange(20, screen_width - 20)
            mouse.rect.y = random.randrange(10, 20)

            # Ändert bei jeder zweiten Maus die Richtung
            if i % 2 == 0:
                mouse.change()

            mouse_list.add(mouse)
            all_sprites_list.add(mouse)


# ---------Variabeln-----------------

# Legt Fenstergröße und Fensterbezeichnung fest.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Catch the Mouse")

# Mauszeiger ist nicht sichtbar
pygame.mouse.set_visible(0)

# Legt Schrifart fest
font = pygame.font.SysFont("arial", 20)
# läd Informationen zur Schrift
sound = pygame.mixer.Sound("sound\isnt-it.ogg")

loop = True
clock = pygame.time.Clock()

# Information über Käse, Maus und Spielerlevel
cheessPiece = 50
cheessEaten = 0
mousePiece = 0
mouseMinSpeed = 3
mouseMaxSpeed = 4
mouseChange = 100
level = 0

# Sprites-Listen mit Spieler(Katze), Käse, und Mäusen
chees_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
mouse_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# Erstellt die Objekte, Käse, Mouse und Spieler
chees = Chees()
chees.drawALot()
mouse = Mouse(random.randrange(mouseMinSpeed, mouseMaxSpeed))
player = Cat()

# -------- Hauptprogramm -----------
while loop:
    # überprüft ob ein Event ausgelöst wurde.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Beendet die Schleife
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Beendet die Schleife
                loop = False
            elif event.key == pygame.K_t:
                # Startet das Spiel erneut.
                chees.drawALot()
                level = 0
                mouseMaxSpeed = 4

    screen.fill(GRAY)

    # Ermittelt die Position des Mauszeigers und stellt Spielerfigur an dieser Stelle da.
    pos = pygame.mouse.get_pos()
    player.rect.x = pos[0]
    player.rect.y = pos[1]

    # überprüft ob noch Mäuse auf dem Spielfeld sind. Wenn nicht werden neue erstellt, pro Level wird eine Maus hinzugefügt.
    # Das Level wird erhöht und es wird ein Sound abgespielt.
    if mouse_list.__len__() == 0:
        mouse.draw(mousePiece, mouseMinSpeed, mouseMaxSpeed)
        mousePiece += 1
        mouseMaxSpeed += 1
        sound.play()
        level += 1

    # Löscht ein Sprite, aus der Gruppe Käse, sobald es mit einer Maus zusammenstößt. 
    pygame.sprite.groupcollide(mouse_list, chees_list, False, True)

    # überprüft ob noch Käsestücke vorhanden sind.
    # Falls nicht, wird die update Funktion nicht mehr ausgeführt, (die Mäuse bewegen sich nicht mehr).
    if chees_list.__len__() == 0:
        # Mäuse werden nicht mehr gelöscht.
        pygame.sprite.spritecollide(player, mouse_list, False)

        # Gibt Infotext aus
        levelInfo = font.render(u'Level: ' + str(level) + ' erreicht', True, (0, 128, 0))
        info = font.render(u'Zum Beenden, die Taste ESC drücken, möchten Sie erneut spielen t drücken.', True,
                           (0, 128, 0))
        screen.blit(levelInfo, (300, 200))
        screen.blit(info, (10, 400))
    else:
        # Sobald, der Spieler eine Maus berührt wird diese gelöscht.
        pygame.sprite.spritecollide(player, mouse_list, True)

        # Infotext mit Level und verbliebenden Käsestücken
        textLevel = font.render(u'Level: ' + str(level), True, (0, 128, 0))
        text = font.render(u'' + ' Käsestücke: ' + str(chees_list.__len__()) + ' ', True, (0, 128, 0))
        screen.blit(textLevel, (screen_width / 2.5, 5))
        screen.blit(text, (screen_width / 3, 25))

        # Sprite Methoden update werden ausgeführt
        all_sprites_list.update()

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
