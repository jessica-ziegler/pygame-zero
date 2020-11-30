# Write your code here :-)
import random

WIDTH = 500
HEIGHT = 500


muster_zuckerstange = { "bild": "christmas-ball", "geschwindigkeitVon": 1, "geschwindigkeitBis": 2 }
muster_schneeflocke = { "bild": "schneeflocke", "geschwindigkeitVon": 1, "geschwindigkeitBis": 5 }
muster_truthahn = { "bild": "christmas-ball2", "geschwindigkeitVon": 4, "geschwindigkeitBis": 4 }
muster_santa = { "bild": "zuckerstange", "geschwindigkeitVon": 4, "geschwindigkeitBis": 4 }
muster_bonbon = { "bild": "bonbon", "geschwindigkeitVon": 4, "geschwindigkeitBis": 4 }
muster_powerup = { "bild": "truthahn", "geschwindigkeitVon": 8, "geschwindigkeitBis": 8 }

started = False
himmel = []
lives = []

players = []
projectiles = []
powerups = []


def create_santas():
    for i in range(1,5+1):
        santa = Actor("santa-claus")
        santa.top = 5
        santa.left = WIDTH - (5 + santa.width * i)
        lives.append(santa)
        santa.draw()

def print_score():
    global score
    global started

    if started == False:
        if (len(lives) == 0):
            create_santas()
            score = len(lives) * 500 - 1
        started = True

    if score >= 0:
        if (score % 500 == 0) and len(lives) > 0:
            lives.pop(len(lives)-1)
        score -= 1
    else:
        screen.draw.text("Das Spiel ist vorbei.",
                         (WIDTH / 2 -150, HEIGHT / 2 - 20),
                         fontname="bangers",
                         color="gold",
                         fontsize=40)

    screen.draw.text("Highscore: " + str(score+1),
                         (5, 5),
                         fontname="bangers",
                         color="gold",
                         fontsize=40)



def erschaffe_flugobjekt(muster):
    flugobjekt = Actor(muster["bild"])
    flugobjekt.left = random.randint(0, WIDTH)
    flugobjekt.top = -42
    flugobjekt.speed = random.randint(muster["geschwindigkeitVon"],muster["geschwindigkeitBis"])
    flugobjekt.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(flugobjekt)
    flugobjekt.draw()

def erschaffe_zuckerstange():
    erschaffe_flugobjekt(muster_zuckerstange)

def erschaffe_schneeflocke():
    erschaffe_flugobjekt(muster_schneeflocke)

def erschaffe_truthahn():
    erschaffe_flugobjekt(muster_truthahn)

def erschaffe_santa():
    erschaffe_flugobjekt(muster_santa)

def erschaffe_bonbon():
    erschaffe_flugobjekt(muster_bonbon)

def erschaffe_powerup():
    muster = muster_powerup
    flugobjekt = Actor(muster["bild"])
    flugobjekt.left = players[0].left
    flugobjekt.top = -42
    flugobjekt.speed = random.randint(muster["geschwindigkeitVon"],muster["geschwindigkeitBis"])
    flugobjekt.imUhrzeigersinn = (random.randint(0,1) == 1)
    himmel.append(flugobjekt)
    powerups.append(flugobjekt)
    flugobjekt.draw()


def male_gegenstand(flugobjekt):
    flugobjekt.top = -40
    flugobjekt.left = random.randint(0, WIDTH)
    flugobjekt.draw()

def plane_flugobjekte(anzahl, malfunktion):
    for i in range(1, anzahl):
        clock.schedule(malfunktion, random.randint(0,100))

def draw():
    global score
    alien = Actor('alien')
    alien.bottom = HEIGHT
    alien.left = WIDTH / 2 - alien.width / 2
    players.append(alien)

    hat = Actor('santa-hat')
    hat.bottom = alien.bottom - alien.height + 10
    hat.left = alien.left + alien.width / 2 - 40
    players.append(hat)

    if len(himmel) == 0:
        plane_flugobjekte(random.randint(300,500), erschaffe_schneeflocke)
        plane_flugobjekte(random.randint(200,200), erschaffe_zuckerstange)
        plane_flugobjekte(random.randint(300,300), erschaffe_truthahn)
        plane_flugobjekte(random.randint(50,50), erschaffe_santa)
        plane_flugobjekte(random.randint(200,200), erschaffe_bonbon)
        plane_flugobjekte(random.randint(50,50), erschaffe_powerup)

    print_score()
    for life in lives:
        life.draw()

    for player in players:
        player.draw()

    if score > 0:
        for up in powerups:
            if up.colliderect(players[0]):
                score += 500
                powerups.remove(up)

def fliege(flugobjekt):
    # Drehung
    if flugobjekt.imUhrzeigersinn:
        flugobjekt.angle += 1
    else:
        flugobjekt.angle -= 1

    # Bewegung
    flugobjekt.top += flugobjekt.speed

def update():
    screen.fill((0,0,0))
    for flugobjekt in himmel:
        fliege(flugobjekt)
        flugobjekt.draw()

    for flugobjekt in himmel:
        if flugobjekt.y > HEIGHT:
            himmel.remove(flugobjekt)
            del flugobjekt

    for p in projectiles:
        p.x += p.speed
        p.angle -= 3
        p.draw()

def shoot(alien):
    global score

    if score <= 0:
        return

    p = Actor('gift')
    p.x = alien.x + 42
    p.y = alien.y - 30
    p.speed = 8
    if score >= 200:
        score -= 200
    else:
        score = 0
    projectiles.append(p)

def on_key_down(key):
    if keys.UP == key:
        shoot(players[0])
