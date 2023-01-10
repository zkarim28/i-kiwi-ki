import sys
import serial
import serial.tools.list_ports
import json
import pygame
from pygame.locals import *
import objs
import math
import Text
import time
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
            controller_found = True
            arduino = serial.Serial(port=port_name, baudrate=9600,\
                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
            break

# if controller_found == False:
#     do something idk, it might not be worth it to make key controls

#initializes general variables
data_name_list = ['X','Y','R','P','A','B']
winsize = width, height = (1920, 1080)
screen = pygame.display.set_mode(winsize)
bck_color = (50, 150, 75)
pause_color = (211,211,211)
kiwi_thrown = []
starfruit_thrown = []
pawns = [objs.Pawn((250,250)), objs.Pawn((100,250)), objs.Pawn((250,100))]
knights = [objs.Knight((0,0)), objs.Knight((width, 0)),objs.Knight((0,height)), objs.Knight((width, height))]
kiwi_tick = 0
starfruit_tick = 0
start_menu_state = True
in_game_state = False
paused_state = False
in_calibration_instructions_state = False
in_calibration_state = False

#initialize player object
player = objs.Player()
player.rect.center = (width/2,height/2)

#createtest via text class,stores all text in dict
titles = {}
titles['calib'] = Text.Text(winsize, "Calibrating...", (255,255,255), "TITLE", "CENTER")
titles['kiwi'] = Text.Text(winsize, "I-KIWI-KI", (0,0,0), "TITLE", "MIDTOP")
titles['paused'] = Text.Text(winsize, "PAUSED", (0,0,0), "TITLE", "MIDTOP")
titles['instructions'] = Text.Text(winsize, "INSTRUCTIONS", (0,0,0), "TITLE", "MIDTOP")

texts = {}
texts['fun fact'] = Text.Text(winsize, \
    "Snapple Cap Fact 144: Texas is the only state that permits residents to cast absentee ballots from space.", \
    (255,255,255), "TEXT", "MIDBOTTOM")
texts['instructions1'] = Text.Text(winsize, \
    "Tilt controller around y-axis to move left and right",\
    (255,255,255), 'TEXT', 'CUSTOM', "MIDTOP", (width/2,100))
texts['instructions2'] = Text.Text(winsize, \
    "Tilt controller around x-axis to move up and down",\
    (255,255,255), 'TEXT', 'CUSTOM', "MIDTOP", (width/2,200))
texts['instructions3'] = Text.Text(winsize, \
    "Use joystick to aim Press button to shoot kiwis",\
    (255,255,255), 'TEXT', 'CUSTOM', "MIDTOP", (width/2,300))
texts['instructions4'] = Text.Text(winsize, \
    "Place controller on a flat surface to prepare for calibration", \
    (255,255,255), 'TEXT', 'CUSTOM', "MIDTOP", (width/2,400))

buttons = {}
buttons['start'] = Text.Text(winsize, "START", (255,255,255), "BUTTON", "CENTER")
buttons['continue'] = Text.Text(winsize, "CONTINUE", (255,255,255), "BUTTON", "MIDBOTTOM")
buttons['pause'] = Text.Text(winsize, "PAUSE", (255,255,255), "BUTTON", "TOPLEFT")
buttons['resume'] = Text.Text(winsize, "RESUME", (0,0,0), "BUTTON", "CENTER")
buttons['quit'] = Text.Text(winsize, "QUIT", (0,0,0), "BUTTON", "CUSTOM",\
    "CENTER", (winsize[0]/2,700))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    while start_menu_state == True:
        
        buttons['start'].clicked = False
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
            in_calibration_instructions_state = True
            break

    while in_calibration_instructions_state == True:
        
        buttons['continue'].clicked = False
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mx in range(buttons['continue'].rect.left, \
                        buttons['continue'].rect.right) and \
                        my in range(buttons['continue'].rect.top, \
                        buttons['continue'].rect.bottom):
                        buttons['continue'].clicked = True

        screen.fill(bck_color)
        screen.blit(buttons['continue'].surface, buttons['continue'].rect)
        screen.blit(titles['instructions'].surface, titles['instructions'].rect)
        screen.blit(texts['instructions1'].surface, texts['instructions1'].rect)
        screen.blit(texts['instructions2'].surface, texts['instructions2'].rect)
        screen.blit(texts['instructions3'].surface, texts['instructions3'].rect)
        screen.blit(texts['instructions4'].surface, texts['instructions4'].rect)
        pygame.display.flip()
        if buttons['continue'].clicked == True:
            in_calibration_instructions_state = False
            in_calibration_state = True
            break

    while in_calibration_state == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
        
        screen.fill((0,0,0))
        screen.blit(titles['calib'].surface, titles['calib'].rect)
        screen.blit(texts['fun fact'].surface, texts['fun fact'].rect)
        pygame.display.flip()
        player.calibration(arduino)
        in_calibration_state = False
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

        #keep reading lines to prevent movement while paused
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
                kiwi = objs.Bullets(in_place_vector, in_place_center, "kiwi.png")
                kiwi_thrown.append(kiwi)
                kiwi_tick = 0

        if starfruit_tick >= 15:
            for pawn in pawns:
                in_place_center = pawn.rect.center
                in_place_vector = pawn.facing_vector
                starfruit = objs.Bullets(in_place_vector, in_place_center, "starfruit.png")
                starfruit_thrown.append(starfruit)
                starfruit_tick = 0

        for pawn in pawns:
            pawn.facePlayer(player)

        for knight in knights:
            knight.facePlayer(player)
            knight.movement()

        for kiwi in kiwi_thrown:
            if kiwi.end == True:
                kiwi_thrown.remove(kiwi)
            else:
                kiwi.movement(winsize)

        for starfruit in starfruit_thrown:
            if starfruit.end == True:
                starfruit_thrown.remove(starfruit)
            else:
                starfruit.movement(winsize)

        screen.fill(bck_color)
        
        #draw kiwi
        for kiwi in kiwi_thrown:
            screen.blit(kiwi.image, \
            (kiwi.rect.centerx - int(kiwi.image.get_width() / 2), \
            kiwi.rect.centery - int(kiwi.image.get_height() / 2)))

        #draw starfruit
        for starfruit in starfruit_thrown:
            screen.blit(starfruit.image, \
            (starfruit.rect.centerx - int(starfruit.image.get_width() / 2), \
            starfruit.rect.centery - int(starfruit.image.get_height() / 2)))
        
        #draw pawn
        for pawn in pawns:
            screen.blit(pawn.image, pawn.rect.center)
        
        #draw knight
        for knight in knights:
            screen.blit(knight.image, knight.rect.center)
        
        #draw player
        screen.blit(player.moving_arrow, player.moving_arrow_rect.center)
        screen.blit(player.facing_arrow, player.facing_arrow_rect.center)
        screen.blit(player.image, \
            (player.rect.centerx - int(player.image.get_width() / 2), \
            player.rect.centery - int(player.image.get_height() / 2)))

        #draw text
        screen.blit(buttons['pause'].surface, buttons['pause'].rect)
        screen.blit(titles['kiwi'].surface, titles['kiwi'].rect)

        pygame.display.flip()

        #counters to prevent bullet laser spraying
        kiwi_tick += 1
        starfruit_tick += 1

        if buttons['pause'].clicked == True:
            in_game_state = False
            start_menu_state = False
            paused_state = True
            break

    while paused_state == True:

        buttons['resume'].clicked = False
        buttons['quit'].clicked = False
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
                    elif mx in range(buttons['quit'].rect.left, \
                        buttons['quit'].rect.right) and \
                        my in range(buttons['quit'].rect.top, \
                        buttons['quit'].rect.bottom):
                        buttons['quit'].clicked = True      

        #keep reading serial monitor lines to prevent moving on pause screen
        arduino.readline().decode(errors="ignore")

        screen.fill(pause_color)
        screen.blit(titles['paused'].surface, titles['paused'].rect)
        screen.blit(buttons['resume'].surface, buttons['resume'].rect)
        screen.blit(buttons['quit'].surface, buttons['quit'].rect)
        pygame.display.flip()
        if buttons['resume'].clicked == True:
            paused_state = False
            in_game_state = True
            break
        if buttons['quit'].clicked == True:
            sys.exit()