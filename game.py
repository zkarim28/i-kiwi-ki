import sys
import serial
import serial.tools.list_ports
import json
import pygame
from pygame.locals import *
import objs
import math
import Text
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

#initialize player object
player = objs.Player()
player.rect.center = (width/2,height/2)

#createtest via text class,stores all text in dict
titles = {}
titles['calib'] = Text.Text(winsize, "Calibrating...", (255,255,255), "TITLE", "CENTER")
titles['kiwi'] = Text.Text(winsize, "I-KIWI-KI", (0,0,0), "TITLE", "MIDTOP")
titles['paused'] = Text.Text(winsize, "PAUSED", (0,0,0), "TITLE", "MIDTOP")

texts = {}
texts['intro'] = Text.Text(winsize, \
    "Snapple Cap Fact 144: Texas is the only state that permits residents to cast absentee ballots from space.", \
        (255,255,255), "TEXT", "MIDBOTTOM")

buttons = {}
buttons['start'] = Text.Text(winsize, "START", (255,255,255), "BUTTON", "CENTER")
buttons['pause'] = Text.Text(winsize, "PAUSE", (255,255,255), "BUTTON", "TOPLEFT")
buttons['resume'] = Text.Text(winsize, "RESUME", (0,0,0), "BUTTON", "CENTER")

#calibrates the accelerometer
screen.blit(titles['calib'].surface, titles['calib'].rect)
screen.blit(texts['intro'].surface, texts['intro'].rect)
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
                    if mx in range(buttons['start'].rect.left, \
                        buttons['start'].rect.right) and \
                        my in range(buttons['start'].rect.top, \
                        buttons['start'].rect.bottom):
                        buttons['start'].clicked = True

        screen.fill(bck_color)
        screen.blit(buttons['start'].surface, buttons['start'].rect)
        screen.blit(titles['kiwi'].surface, titles['kiwi'].rect)
        pygame.display.flip()
        if buttons['start'].clicked == True:
            start_menu_state = False
            in_game_state = True
            break

    while in_game_state == True:
        
        buttons['pause'].clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(buttons['pause'].rect.left, \
                        buttons['pause'].rect.right) and \
                        my in range(buttons['pause'].rect.top, \
                        buttons['pause'].rect.bottom):
                        buttons['pause'].clicked = True

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
        screen.blit(titles['kiwi'].surface, titles['kiwi'].rect)
        screen.blit(player.facing_arrow, player.facing_arrow_rect.center)
        for kiwi in thrown:
            screen.blit(kiwi.image, \
            (kiwi.rect.centerx - int(kiwi.image.get_width() / 2), \
            kiwi.rect.centery - int(kiwi.image.get_height() / 2)))
        screen.blit(player.moving_arrow, player.moving_arrow_rect.center)
        screen.blit(player.image, \
            (player.rect.centerx - int(player.image.get_width() / 2), \
            player.rect.centery - int(player.image.get_height() / 2)))
        screen.blit(buttons['pause'].surface, buttons['pause'].rect)
        pygame.display.flip()

        kiwi_tick += 1
        if buttons['pause'].clicked == True:
            in_game_state = False
            start_menu_state = False
            paused_state = True
            break

    while paused_state == True:

        buttons['resume'].clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(buttons['resume'].rect.left, \
                        buttons['resume'].rect.right) and \
                        my in range(buttons['resume'].rect.top, \
                        buttons['resume'].rect.bottom):
                        buttons['resume'].clicked = True   

        screen.fill(pause_color)
        screen.blit(titles['paused'].surface, titles['paused'].rect)
        screen.blit(buttons['resume'].surface, buttons['resume'].rect)
        pygame.display.flip()
        if buttons['resume'].clicked == True:
            paused_state = False
            in_game_state = True
            break