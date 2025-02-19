import pygame
import random
import math
from pygame import mixer

def start_spaceInvader():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    background = pygame.image.load('SpaceInvader/bg.jpg')
    mixer.music.load('SpaceInvader/background.wav')
    mixer.music.play(-1)

    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load('SpaceInvader/ufo (1).png')
    pygame.display.set_icon(icon)

    playerImg = pygame.image.load('SpaceInvader/player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('SpaceInvader/enemy.png'))
        enemyX.append(random.randint(30, 730))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.5)
        enemyY_change.append(30)

    bulletImg = pygame.image.load('SpaceInvader/bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 5
    bullet_state = "ready"

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    textX = 10
    textY = 10

    over_font = pygame.font.Font('freesansbold.ttf', 70)

    def player(x, y):
        screen.blit(playerImg, (x, y))

    def show_score(x, y):
        score = font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text():
        over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def enemy(x, y, a):
        screen.blit(enemyImg[a], (x, y))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))

    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        return distance < 27
          

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.9
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 0.9
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_sound = mixer.Sound('SpaceInvader/laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        bullet_state = "fire"
                        fire_bullet(bulletX, bulletY)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 735:
            playerX = 735

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 735:
                enemyX_change[i] = -0.5
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('SpaceInvader/explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(30, 730)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change


        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()

start_spaceInvader()
