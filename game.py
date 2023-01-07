import sys
import serial
import serial.tools.list_ports
import json
import pygame
from pygame.locals import *
import objs
import math
from sys import platform

#check OS, then iterate through USB ports to find arduino controller
available_ports = {}
controller_found = False
if platform == "darwin":
    arduino = serial.Serial('/dev/cu.usbmodem141101')
elif platform == "win32":
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        available_ports[port] = desc
    for port_name in available_ports:
        if "Arduino Mega 2560" in available_ports[port_name]:
            arduino = serial.Serial(port=port_name, baudrate=9600,\
                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
            controller_found = True
            break

#initializes general variables
data_name_list = ['X','Y','R','P','A','B']
winsize = width, height = (1900, 1000)
screen = pygame.display.set_mode(winsize)
bck_color = (50, 150, 75)
pause_color = (211,211,211)
thrown = []
kiwi_tick = 0
start_menu_state = True
in_game_state = False
paused_state = False
start_button_clicked = False
pause_button_clicked = False
resume_button_clicked = False

#initialize player object
player = objs.Player()
player.rect.center = (width/2,height/2)

#create font and text
pygame.font.init()
my_title_font = pygame.font.SysFont('Comic Sans MS', 75)
my_text_font = pygame.font.SysFont('Comic Sans MS', 45)

text_surface = my_title_font.render("I-KIWI-KI", False, (0,0,0))
text_surface_rect = text_surface.get_rect()
text_surface_rect.midtop = (width/2,0)

start_surface = my_title_font.render("i-kiki-ki", False, (0,0,0))
start_surface_rect = start_surface.get_rect()
start_surface_rect.midtop = (width/2, 0)

start_button_surface = my_text_font.render("start", False, (0,0,0))
start_button_surface_rect = start_button_surface.get_rect()
start_button_surface_rect.midtop = (width/2, height/2)

waiting_surface = my_title_font.render("Calibrating...", False, (255,255,255))

pause_button_surface = my_title_font.render("Pause", False, (0,0,0))
pause_button_surface_rect = pause_button_surface.get_rect()
pause_button_surface_rect.topright = (width, 0)

paused_surface = my_title_font.render("PAUSED", False, (0,0,0))
paused_surface_rect = start_button_surface.get_rect()
paused_surface_rect.midtop = (width/2, 0)

resume_button_surface = my_text_font.render("RESUME", False, (0,0,0))
resume_button_surface_rect = start_button_surface.get_rect()
resume_button_surface_rect.center = (width/2, height/2)

#calibrates the accelerometer
screen.blit(waiting_surface, (0,0))
pygame.display.flip()
player.calibration(arduino)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    while start_menu_state == True:
        
        start_button_clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(start_button_surface_rect.left, \
                        start_button_surface_rect.right) and \
                        my in range(start_button_surface_rect.top, \
                        start_button_surface_rect.bottom):
                        start_button_clicked = True

        screen.fill(bck_color)
        screen.blit(start_button_surface, start_button_surface_rect)
        screen.blit(start_surface, start_surface_rect)
        pygame.display.flip()
        if start_button_clicked == True:
            start_menu_state = False
            in_game_state = True
            break

    while in_game_state == True:
        
        pause_button_clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(pause_button_surface_rect.left, \
                        pause_button_surface_rect.right) and \
                        my in range(pause_button_surface_rect.top, \
                        pause_button_surface_rect.bottom):
                        pause_button_clicked = True

        data = arduino.readline().decode(errors="ignore")
        name_count = 0
        for char in data:
            if char in data_name_list:
                name_count+=1

        if name_count == 6:
            jX_data = int(data[data.index("X")+2:data.index("Y")]) #calibrated
            jY_data = int(data[data.index("Y")+2:data.index("R")]) #calibrated
            aX_data = int(data[data.index("R")+2:data.index("P")]) #calibrated
            aY_data = int(data[data.index("P")+2:data.index("A")]) #calibrated
            B_data = int(data[data.index("A")+2:data.index("B")]) #calibrated
            B2_data = int(data[data.index("B")+2:])  #calibrated

            player.movement(winsize, aX_data, aY_data)
            player.arrows(jX_data, jY_data, aX_data, aY_data)

            if kiwi_tick >= 10:
                if B_data == 0:
                    in_place_center = player.rect.center
                    in_place_vector = player.facing_vector
                    kiwi = objs.Bullets(in_place_vector, in_place_center)
                    thrown.append(kiwi)
                    kiwi_tick = 0

            for kiwi in thrown:
                if kiwi.end == True:
                    thrown.remove(kiwi)
                else:
                    kiwi.movement(winsize)

        screen.fill(bck_color)
        screen.blit(text_surface, text_surface_rect)
        screen.blit(player.facing_arrow, player.facing_arrow_rect.center)
        for kiwi in thrown:
            screen.blit(kiwi.image, kiwi.rect.center)
        screen.blit(player.moving_arrow, player.moving_arrow_rect.center)
        screen.blit(player.image, \
            (player.rect.centerx - int(player.image.get_width() / 2), \
            player.rect.centery - int(player.image.get_height() / 2)))
        screen.blit(pause_button_surface, pause_button_surface_rect)
        pygame.display.flip()
        kiwi_tick += 1
        if pause_button_clicked == True:
            in_game_state = False
            start_menu_state = False
            paused_state = True
            break

    while paused_state == True:

        resume_button_clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(resume_button_surface_rect.left, \
                        resume_button_surface_rect.right) and \
                        my in range(resume_button_surface_rect.top, \
                        resume_button_surface_rect.bottom):
                        resume_button_clicked = True   

        screen.fill(pause_color)
        screen.blit(paused_surface, paused_surface_rect)
        screen.blit(resume_button_surface, resume_button_surface_rect)
        pygame.display.flip()
        if resume_button_clicked == True:
            paused_state = False
            in_game_state = True
            break