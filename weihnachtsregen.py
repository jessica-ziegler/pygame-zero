import random

WIDTH = 500
HEIGHT = 500

# Enthält alle fallenden Schneeflocken
himmel = []

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
    anzahl_zuckerstangen = random.randint(200, 200)
    anzahl_weihnachtskugeln = random.randint(200, 200)

    for i in range(1, anzahl_flocken):
        clock.schedule(erschaffe_schneeflocke, random.randint(0,100))

    for i in range(1, anzahl_zuckerstangen):
        clock.schedule(erschaffe_zuckerstange, random.randint(0,100))

    for i in range(1, anzahl_weihnachtskugeln):
        clock.schedule(erschaffe_weihnachtskugel, random.randint(0,100))



def falle(himmelsobjekt):
    # Drehung
    if himmelsobjekt.imUhrzeigersinn:
        himmelsobjekt.angle += 1
    else:
        himmelsobjekt.angle -= 1

    # Bewegung
    himmelsobjekt.top += himmelsobjekt.geschwindigkeit
    himmelsobjekt.draw()

def draw():
    # Sobald am Himmel keine Schneeflocken mehr sind, erschaffe neuen Schneeregen
    if len(himmel) == 0:
        erschaffe_schneeregen()

def update():
    screen.clear()

    # Lasse jede Schneeflocke weiter fallen
    # Zerstöre alle Schneeflocken am unteren Bildschirmrand
    for schneeflocke in himmel:
        falle(schneeflocke)

        if schneeflocke.y > HEIGHT:
            himmel.remove(schneeflocke)
            del schneeflocke
