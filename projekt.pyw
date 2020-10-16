import pygame
import os
from sys import exit
from read_obj import ObjLoader
from mesh import *

# Regulacja prędkości obrotu
rotate_speed = 0.03

# Zmiana pozycji kamery
def camera_position(key):
    # Pozycja bryły/kamery
    if key[pygame.K_w]:
        bryly.Back()
    if key[pygame.K_s]:
        bryly.Forward()
    if key[pygame.K_d]:
        bryly.Left()
    if key[pygame.K_a]:
        bryly.Right()
    if key[pygame.K_z]:
        bryly.Up()
    if key[pygame.K_c]:
        bryly.Down()
    
    # Rotacja
    if key[pygame.K_UP]:
        bryly.rotate('x', rotate_speed)
    if key[pygame.K_DOWN]:
        bryly.rotate('x', -rotate_speed)
    if key[pygame.K_RIGHT]:
        bryly.rotate('y', rotate_speed)
    if key[pygame.K_LEFT]:
        bryly.rotate('y', -rotate_speed)
    if key[pygame.K_e]:
        bryly.rotate('z', rotate_speed)
    if key[pygame.K_q]:
        bryly.rotate('z', -rotate_speed)

# Inicjalizacja pygame
pygame.init()
pygame.display.set_caption('Grafika komputerowa (projekt 2)')
screen = pygame.display.set_mode((1000, 600))

# Wyświetlenie napisów sterowania
font = pygame.font.SysFont("Arial", 20)
def show_movement():
    text1 = font.render("A,W,S,D,Z,C - poruszanie ", True, pygame.Color("white"))
    text2 = font.render("Strzałki i Q,E - obroty", True, pygame.Color("white"))
    return [text1, text2]

text = show_movement()

# Ładowanie obiektu
obj = ObjLoader("table.obj")
bryly = Mesh(obj.vertices, obj.faces, screen)

# Odświeżanie ekranu
def refresh():
    screen.fill((128,128,255))
    bryly.render()
    screen.blit(text[0], (5,0))
    screen.blit(text[1], (5,20))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    key = pygame.key.get_pressed()
    camera_position(key)

# Uruchomienie programu
while(True):
    refresh()
