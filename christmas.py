import random

WIDTH = 500
HEIGHT = 500

# Enthält alle fallenden Schneeflocken
himmel = []

# Enthält alle fallenden Powerups
powerups = []

# Enthält Bomben (Ostereier)
bomben = []

# Aktueller Highscore
highscore = 0
leben = 5
lebensanzeige = []

for i in range(1,leben+1):
    santa = Actor("santa-claus")
    santa.top = 5
    santa.left = WIDTH - (5 + santa.width * i)
    lebensanzeige.append(santa)

# Spieler
spieler = Actor('alien')
spieler.bottom = HEIGHT
spieler.left = WIDTH / 2 - spieler.width / 2

def highscore_anzeigen():
    global highscore

    screen.draw.text("Highscore: " + str(highscore),
                        (5, 5),
                         fontname="bangers",
                         color="gold",
                         fontsize=40)

    if leben <= 0:
        screen.draw.text("Das Spiel ist vorbei.",
                 (WIDTH / 2 -150, HEIGHT / 2 - 20),
                 fontname="bangers",
                 color="gold",
                 fontsize=40)

def erschaffe_osterei():
    osterei = Actor("osterei")
    osterei.left = random.randint(0, WIDTH)
    osterei.top = -42
    osterei.geschwindigkeit = random.randint(15,20)
    osterei.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(osterei)
    bomben.append(osterei)
    osterei.draw()

def erschaffe_truthahn():
    truthahn = Actor("truthahn")
    truthahn.left = random.randint(0, WIDTH)
    truthahn.top = -42
    truthahn.geschwindigkeit = random.randint(1,5)
    truthahn.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(truthahn)
    powerups.append(truthahn)
    truthahn.draw()

# Erzeuge eine Weihnachtskugel mit zufälliger Geschwindigkeit, Drehrichtung und Startposition
def erschaffe_weihnachtskugel():
    # wähle Farbe der kugel zufällig
    kugelfarbe = ""

    if (random.randint(0,1) == 1):
        kugelfarbe = "weihnachtskugel-rot"
    else:
        kugelfarbe = "weihnachtskugel-gruen"

    # Erzeuge die Kugel
    weihnachtskugel = Actor(kugelfarbe)
    weihnachtskugel.left = random.randint(0, WIDTH)
    weihnachtskugel.top = -42
    weihnachtskugel.geschwindigkeit = random.randint(1,2)
    weihnachtskugel.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(weihnachtskugel)
    weihnachtskugel.draw()

# Erzeuge eine Schneeflocke mit zufälliger Geschwindigkeit, Drehrichtung und Startposition
def erschaffe_schneeflocke():
    schneeflocke = Actor("schneeflocke")
    schneeflocke.left = random.randint(0, WIDTH)
    schneeflocke.top = -42
    schneeflocke.geschwindigkeit = random.randint(1,5)
    schneeflocke.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(schneeflocke)
    schneeflocke.draw()

# Erzeuge eine Zuckerstange mit zufälliger Geschwindigkeit, Drehrichtung und Startposition
def erschaffe_zuckerstange():
    zuckerstange = Actor("zuckerstange")
    zuckerstange.left = random.randint(0, WIDTH)
    zuckerstange.top = -42
    zuckerstange.geschwindigkeit = random.randint(4,4)
    zuckerstange.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(zuckerstange)
    zuckerstange.draw()

# Stoße die Erzeugung aller Schneeflocken an
def erschaffe_schneeregen():
    anzahl_flocken = random.randint(300,500)
    anzahl_zuckerstangen = 200
    anzahl_weihnachtskugeln = 200
    anzahl_powerups = 50
    anzahl_ostereier = 50

    for i in range(1, anzahl_flocken):
        clock.schedule(erschaffe_schneeflocke, random.randint(0,100))

    for i in range(1, anzahl_zuckerstangen):
        clock.schedule(erschaffe_zuckerstange, random.randint(0,100))

    for i in range(1, anzahl_weihnachtskugeln):
        clock.schedule(erschaffe_weihnachtskugel, random.randint(0,100))

    for i in range(1, anzahl_powerups):
        clock.schedule(erschaffe_truthahn, random.randint(0,100))

    for i in range(1, anzahl_ostereier):
        clock.schedule(erschaffe_osterei, random.randint(0,100))

def falle(himmelsobjekt):
    # Drehung
    if himmelsobjekt.imUhrzeigersinn:
        himmelsobjekt.angle += 1
    else:
        himmelsobjekt.angle -= 1

    # Bewegung
    himmelsobjekt.top += himmelsobjekt.geschwindigkeit
    himmelsobjekt.draw()

def on_key_down(key):
    if (keys.LEFT == key):
        spieler.left -= 50
        spieler.left %= WIDTH
    elif (keys.RIGHT == key):
        spieler.left += 15
        spieler.left %= WIDTH

def powerup_essen(power_up):
    global powerups
    global himmel
    global highscore

    sounds.crunch.play()
    powerups.remove(power_up)
    himmel.remove(power_up)
    del power_up

    highscore += 500


def bombe_explodieren(bombe):
    global bomben
    global himmel
    global leben

    sounds.eiquetschen2.play()
    leben -= 1
    lebensanzeige.remove(lebensanzeige[len(lebensanzeige)-1])

    himmel.remove(bombe)
    bomben.remove(bombe)

    del bombe


def draw():
    # Sobald am Himmel keine Schneeflocken mehr sind, erschaffe neuen Schneeregen
    if len(himmel) == 0:
        erschaffe_schneeregen()

def update():
    global leben
    screen.clear()

    # Bomben explodieren lassen
    if leben > 0:
        for bombe in bomben:
            if spieler.colliderect(bombe):
                bombe_explodieren(bombe)

    # Powerups essen
    if leben > 0:
        for power_up in powerups:
            if spieler.colliderect(power_up):
                powerup_essen(power_up)


    # Alle Objekte fallen lassen
    for item in himmel:
        falle(item)

        if item.y > HEIGHT:
            himmel.remove(item)
            if item in powerups:
                powerups.remove(item)

            if item in bomben:
                bomben.remove(item)
            del item

    highscore_anzeigen()
    spieler.draw()

    for santa in lebensanzeige:
        santa.draw()
