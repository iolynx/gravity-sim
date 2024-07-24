import pygame
import math
from particle import Particle

pygame.init()

WIDTH = 1200
HEIGHT = 750

UWIDTH = 1600
UHEIGHT = 1600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
sun = (255, 228, 132)
#sun = (209, 64, 9)
bluePlanet = (5, 76, 89)
brownPlanet = (86, 64, 13)

G = 5.7 * 10**(-1)
SUNMASS, SUNRAD = 210, 14
EARTHMASS, EARTHRAD = 6, 4
cameraX, cameraY = 0, 0

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((UWIDTH, UHEIGHT))
alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
pygame.display.set_caption("Gravity")
clock = pygame.time.Clock()



# --------------------------------------------------INISTANCE VARIABLES-----------------------------------------------


particles = []
tick = 1200
mousePressed, mouseReleased = False, False
rightPressed, rightReleased = False, False
crashed = False
selectedType = "earth"
selectableTypes = ["earth", "sun"]
font = pygame.font.SysFont("SF Pro Display", 12)


def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def paused(pause):
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

    pygame.display.update()

    screen.fill(black)
    for p in particles:
        p.draw()

    clock.tick(tick)

# -----------------------------------------------------GAMELOOP--------------------------------------------------------


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = True
                paused(pause)
            elif event.key == pygame.K_r:
                particles = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                if selectedType == "sun":
                    selectedType = "earth"
                else:
                    selectedType = "sun"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mousePressed == False:
                    xFirst, yFirst = pygame.mouse.get_pos()
                mousePressed = True
                mouseReleased = False
                x, y = pygame.mouse.get_pos()
            elif event.button == 3:
                if rightPressed == False:
                    xFirstRight, yFirstRight = pygame.mouse.get_pos()
                    xFirstRight -= cameraX
                    yFirstRight -= cameraY
                rightPressed = True
                rightReleased = False
                xR, yR = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mousePressed = False
                mouseReleased = True
            elif event.button == 3:
                rightPressed = False
                rightReleased = True

    alpha_surf.fill((255, 255, 255, 250), special_flags=pygame.BLEND_RGBA_MULT)

    pygame.display.update()
    screen.fill(black)
    display.fill(black)

    # Fnet calculation & Collision detection
    for p in particles:
        p.draw()
        p.drawTrail(alpha_surf)
        for p2 in particles:
            if p2 != p:
                p.updateForces(p2)
                if dist(p, p2) < p.radius:
                    if p.mass >= p2.mass:
                        p.mass += p2.mass
                        p.xVel = (p.mass*p.xVel + p2.mass*p2.xVel) / \
                            (p.mass + p2.mass)
                        p.yVel = (p.mass*p.yVel + p2.mass*p2.yVel) / \
                            (p.mass + p2.mass)
                        particles.remove(p2)
        p.updatePos()

        if p.x > UWIDTH + 100 or p.y > UHEIGHT + 100 or p.x < -100 or p.y < -100:
            particles.remove(p)

    # checking for mouseInput
    if mousePressed:
        x, y = pygame.mouse.get_pos()
        xDist = xFirst - x
        yDist = yFirst - y
        pygame.draw.circle(screen, white, (xFirst - cameraX,
                           yFirst - cameraY), selectedRad, selectedRad)
        pygame.draw.line(screen, white, (xFirst - cameraX,
                         yFirst - cameraY), (x - cameraX, y - cameraY), 1)

    elif rightPressed:
        pygame.draw.circle(screen, white, (0, 0), 5, 5)
        xR, yR = pygame.mouse.get_pos()
        cameraX = xR - xFirstRight
        cameraY = yR - yFirstRight

    if mouseReleased and not mousePressed:
        particles.append(Particle(xFirst - cameraX, yFirst - cameraY, (xFirst - x) /
                         100, (yFirst - y)/100, selectedMass, selectedRad, selectedColor, screen))
        mouseReleased = False

    # blitting screen to display
    screen.blit(alpha_surf, (0, 0))
    display.blit(screen, (cameraX, cameraY))

    if selectedType == "sun":
        selectedMass, selectedRad, selectedColor = SUNMASS, SUNRAD, sun
        pygame.draw.circle(display, sun, (42, 720), selectedRad, selectedRad)
    elif selectedType == "earth":
        selectedMass, selectedRad, selectedColor = EARTHMASS, EARTHRAD, brownPlanet
        pygame.draw.circle(display, bluePlanet, (42, 725),
                           selectedRad, selectedRad)

    pygame.draw.rect(display, white, (3, 695 - selectedRad,
                     25 + 28*2, 55 + selectedRad), width=1)
    text = font.render('SPAWN : ' + selectedType.upper(), True, white, black)
    display.blit(text, (4, 700 - selectedRad))
    text = font.render(str(pygame.mouse.get_pos()), True, white, black)
    display.blit(text, (1100, 700))

    # showing L and R labels
    if mousePressed:
        text = font.render("L", True, white, black)
        display.blit(text, (1080, 700))
    if rightPressed:
        text = font.render("R", True, white, black)
        display.blit(text, (1090, 700))

    clock.tick(tick)

print("Number of particles at the end of the simulation = ", len(particles))
