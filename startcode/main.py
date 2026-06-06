import pygame
import time
import csv
from datetime import datetime
from snake import Snake
from food import Food

# kleuren
kleur_achtergrond = (0, 0, 0)
kleur_tekst = (0, 255, 0)

# schermgrootte
breedte = 800
hoogte = 600
veld_grootte = 20

# Snelheid van het spel
spel_snelheid = int(input("Wat wil je voor snelheid? 1 - 100: "))

# Initialiseren van de pygame-module
pygame.init()

# Creëer een venster met opgegeven breedte en hoogte
venster = pygame.display.set_mode((breedte, hoogte))
pygame.display.set_caption('Snake')

# Functie om de score op het scherm te tonen
def toon_score(score, venster):
    font = pygame.font.Font(None, 36)
    scoretekst = font.render(f"Score: {score}", True, kleur_tekst)
    venster.blit(scoretekst, (10, 10))

def haal_hoogste_score_op():
    try:
        with open('highscores.csv', mode='r') as file:
            reader = csv.reader(file)
            highscores = list(reader)
            highest_score = 0
            highest_score_with_speed = 0
            for row in highscores:
                if int(row[0]) > int(highest_score):
                    highest_score = row[0]
                    highest_score_with_speed = row[2]
            return highest_score, highest_score_with_speed

    except FileNotFoundError:
        return 0

def sla_op_in_csv(score, tijdstip, spel_snelheid):
    with open('highscores.csv', mode='a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([score, tijdstip, spel_snelheid])

# Start de hoofdloop van het spel
def game_lus():
    food = Food(breedte, hoogte)
    snake = Snake(breedte//2, hoogte//2)
    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.x_verandering == 0:
                    snake.x_verandering = -veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_RIGHT and snake.x_verandering == 0:
                    snake.x_verandering = veld_grootte
                    snake.y_verandering = 0
                elif event.key == pygame.K_UP and snake.y_verandering == 0:
                    snake.y_verandering = -veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_DOWN and snake.y_verandering == 0:
                    snake.y_verandering = veld_grootte
                    snake.x_verandering = 0
                elif event.key == pygame.K_p:
                    gepauzeerd = True
                    pauze_font = pygame.font.Font(None, 36)
                    pauze_tekst = pauze_font.render("Pauze (Druk op P om door te gaan)", True, kleur_tekst)
                    venster.blit(pauze_tekst, (breedte//2 - pauze_tekst.get_width() // 2, hoogte // 2))
                    pygame.display.update()
                    while gepauzeerd:
                        for pauze_event in pygame.event.get():
                            if pauze_event.type == pygame.KEYDOWN and pauze_event.key == pygame.K_p:
                                gepauzeerd = False


        snake.beweeg()
        if snake.is_buiten_veld(breedte, hoogte) or snake.raakt_zichzelf():
            game_over = True

        venster.fill(kleur_achtergrond)  # Vul het scherm met een zwarte achtergrond
        food.teken(venster)
        snake.teken(venster)
        toon_score(score, venster)

        if snake.x == food.x and snake.y == food.y:
            food.plaats_voedsel()
            snake.lengte_slang += 1
            score += 10

        pygame.display.update()
        time.sleep(1 / spel_snelheid)

    print(f"Jouw score is {score}")
    sla_op_in_csv(score, datetime.now(), spel_snelheid)
    hoogste_score, hoogste_speed = haal_hoogste_score_op()
    print(f"De highscore is {hoogste_score} en hoogste speed is {hoogste_speed}")

# Start de hoofdloop van het spel
game_lus()
