#!/usr/bin/env python
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
import random
import csv
from sys import platform

def start():
    
    #initializes general game variables
    data_name_list = ['X','Y','R','P','A','B']
    winsize = width, height = (1920, 960)
    screen = pygame.display.set_mode(winsize)
    bck_color = (50, 150, 75)
    pause_color = (211,211,211)
    kiwi_thrown = []
    starfruit_thrown = []
    pawns = []
    knights = []
    kiwi_tick = 1
    starfruit_tick = 1
    pawn_tick = 1
    knight_tick = 1
    pawn_spawn_rate = random.randint(50,100)
    knight_spawn_rate = random.randint(50,100)
    start_menu_state = False
    in_game_state = False
    paused_state = False
    in_end_game_state = False
    in_calibration_instructions_state = False
    in_calibration_state = False
    controller_found = False
    score = 0
    updated = False

    #initialize player object
    player = objs.Player()
    player.rect.center = (width/2,height/2)

    #create titles, text, and buttons via Text.py, then stores all text objects in a dict
    titles = {}
    titles['controller'] = Text.Text(winsize, "Please plug in controller", (255,255,255), "TITLE", "CENTER")
    titles['calib'] = Text.Text(winsize, "Calibrating...", (255,255,255), "TITLE", "CENTER")
    titles['kiwi'] = Text.Text(winsize, "I-KIWI-KI", (0,0,0), "TITLE", "MIDTOP")
    titles['paused'] = Text.Text(winsize, "PAUSED", (0,0,0), "TITLE", "MIDTOP")
    titles['instructions'] = Text.Text(winsize, "INSTRUCTIONS", (0,0,0), "TITLE", "MIDTOP")
    titles['end'] = Text.Text(winsize, "YOU GOT KIWIED!", (0,0,0), "TITLE", "MIDTOP")
    titles['lb'] = Text.Text(winsize, "LEADERBOARD", (0,0,0), "TITLE", "MIDTOP")

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
    texts['lives'] = Text.Text(winsize, f"Lives: {player.lives}", (255,255,255), "TEXT", "TOPRIGHT")
    texts['score'] = Text.Text(winsize, f"Lives: {score}", (255,255,255), "TEXT", "MIDTOP")
    texts['lbname'] = Text.Text(winsize, "Enter your name for the leaderboard", \
        (0,0,0), 'TEXT', 'CUSTOM', "MIDTOP", (width/2,100))

    buttons = {}
    buttons['start'] = Text.Text(winsize, "START", (255,255,255), "BUTTON", "CENTER")
    buttons['continue'] = Text.Text(winsize, "CONTINUE", (255,255,255), "BUTTON", "MIDBOTTOM")
    buttons['pause'] = Text.Text(winsize, "PAUSE", (255,255,255), "BUTTON", "TOPLEFT")
    buttons['resume'] = Text.Text(winsize, "RESUME", (0,0,0), "BUTTON", "CENTER")
    buttons['exit'] = Text.Text(winsize, "EXIT GAME", (255,0,0), "BUTTON", "CUSTOM",\
        "CENTER", (winsize[0]/2, 700))
    buttons['restart'] = Text.Text(winsize, "RESTART", (0,0,0), "BUTTON", "CENTER")

    #starts game off with 4 of each enemy
    pawns = [objs.Pawn((100,100)), objs.Pawn((width - 100,100)), objs.Pawn((100,height - 100)), objs.Pawn((width - 100,height - 100))]
    knights = [objs.Knight((0,0)), objs.Knight((width, 0)),objs.Knight((0,height)), objs.Knight((width, height))]

    #creates an input box to enter in name for leaderboard
    input_box = Text.InputBox(width/2, (height/2)-250, 200, 50)

    #functions for reaidng, writing, and creating leaderboard
    def nameCheck(name):
        if type(name) != str:
            return False
        if len(name) > 16:
            return False
        if name.isalpha() == False:
            return False
        leaderboard_read = open('leaderboard.csv', encoding = 'utf-8')
        csv_data = csv.reader(leaderboard_read)
        data_lines = list(csv_data)
        for line in data_lines[1:]:
            if name.lower() == line[0].lower():
                leaderboard_read.close()
                return False 
        leaderboard_read.close()
        return True

    def updateLeaderboard(name, score):
        leaderboard_write = open('leaderboard.csv', mode = 'a', newline = '')
        csv_writer = csv.writer(leaderboard_write, delimiter=',')
        csv_writer.writerow([input_box.name,score])
        leaderboard_write.close()

    def getTopSix():
        leaderboard_read = open('leaderboard.csv', encoding = 'utf-8')
        csv_data = csv.reader(leaderboard_read)
        data_lines = list(csv_data)
        mydict = {}
        for line in data_lines[1:]:
            mydict[line[0]] = int(line[1])
        sorted_scores = sorted(mydict.items(), key = lambda kv: kv[1])
        sorted_dictionary = dict(sorted_scores)
        
        topSix = []
        for key in sorted_dictionary:
            topSix.append(f"{key}: {str(sorted_dictionary[key])}")
        texts['lb1'] = Text.Text(winsize, f"{topSix[-1]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 100))
        texts['lb2'] = Text.Text(winsize, f"{topSix[-2]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 155))
        texts['lb3'] = Text.Text(winsize, f"{topSix[-3]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 210))
        texts['lb4'] = Text.Text(winsize, f"{topSix[-4]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 265))
        texts['lb5'] = Text.Text(winsize, f"{topSix[-5]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 320))
        texts['lb6'] = Text.Text(winsize, f"{topSix[-6]}", (0,0,0), "TEXT", "CUSTOM", "CENTER", (width/2, 375))
        leaderboard_read.close()

    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        while controller_found == False:
            #check OS, then iterate through USB ports to find arduino controller
            available_ports = {}
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                available_ports[port] = desc
            if platform == "darwin":
                for port_name in available_ports:
                    if "IOUSBHostDevice" in available_ports[port_name]:
                        controller_found = True
                        start_menu_state = True
                        arduino = serial.Serial(port_name)
                        break
            elif platform == "win32":
                for port_name in available_ports:
                    if "Arduino Mega 2560" in available_ports[port_name]:
                        controller_found = True
                        start_menu_state = True
                        arduino = serial.Serial(port=port_name, baudrate=9600,\
                            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
                        break
            screen.fill((0,100,0))
            screen.blit(titles['controller'].surface, titles['controller'].rect)
            pygame.display.flip()
        
        while start_menu_state == True:
            
            buttons['start'].clicked = False
            buttons['exit'].clicked = False
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
                        elif mx in range(buttons['exit'].rect.left, \
                            buttons['exit'].rect.right) and \
                            my in range(buttons['exit'].rect.top, \
                            buttons['exit'].rect.bottom):
                            buttons['exit'].clicked = True  

            screen.fill(bck_color)
            screen.blit(buttons['start'].surface, buttons['start'].rect)
            screen.blit(buttons['exit'].surface, buttons['exit'].rect)
            screen.blit(titles['kiwi'].surface, titles['kiwi'].rect)
            pygame.display.flip()
            if buttons['start'].clicked == True:
                start_menu_state = False
                in_calibration_instructions_state = True
                break
            elif buttons['exit'].clicked == True:
                sys.exit()

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
            
            texts['lives'] = Text.Text(winsize, f"Lives: {player.lives}", (255,255,255), "TEXT", "TOPRIGHT")
            texts['score'] = Text.Text(winsize, f"Score: {score}", (255,255,255), "TEXT", "MIDTOP")
            
            #check for pawn-kiwi collisions
            for pawn in pawns:
                pawn.collision(kiwi_thrown)
                if pawn.hit == True:
                    pawns.remove(pawn)
                    score+=10
            
            #check for knight-kiwi collisions
            for knight in knights:
                knight.collision(kiwi_thrown)
                if knight.hit == True:
                    knights.remove(knight)
                    score+=5
            
            #check for starfruit-kiwi collisions        
            for starfruit in starfruit_thrown:
                starfruit.collision(kiwi_thrown)
                if starfruit.hit == True:
                    starfruit_thrown.remove(starfruit)
                    score+=1
            
            #check for pawn-player collisions
            player.collision(pawns)
            player.collision(knights)
            player.collision(starfruit_thrown)
            
            #check for macOS exit or pause button click
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

            #update movmenet based on controller sensor data
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
                B_data = int(data[data.index("A")+2:data.index("B")])  #calibrated
                B2_data = int(data[data.index("B")+2:])                #calibrated

                player.movement(winsize, aX_data, aY_data)
                player.arrows(jX_data, jY_data, aX_data, aY_data)

            #shooting kiwis with a fixed fire rate
            if kiwi_tick >= 10:
                if B_data == 0:
                    in_place_center = player.rect.center
                    in_place_vector = player.facing_vector
                    kiwi = objs.Bullets(in_place_vector, in_place_center, "kiwi.png")
                    kiwi_thrown.append(kiwi)
                    kiwi_tick = 0

            #pawns shoot starfruit at a random fireRate between 20 and 50
            for pawn in pawns:
                if pawn_tick % pawn.fireRate == 0:
                    in_place_center = pawn.rect.center
                    in_place_vector = pawn.facing_vector
                    starfruit = objs.Bullets(in_place_vector, in_place_center, "starfruit.png")
                    starfruit_thrown.append(starfruit)
            
            #pawns spawn in at a random spawn rate between 40 and 70 ticks
            if pawn_tick >= pawn_spawn_rate:
                xpos = random.randint(objs.Pawn.WIDTH, width-objs.Pawn.WIDTH)
                ypos = random.randint(objs.Pawn.HEIGHT, height-objs.Pawn.HEIGHT)
                pawns.append(objs.Pawn((xpos, ypos)))
                pawn_tick = 0
                pawn_spawn_rate = random.randint(40,70)
            
            #knights spawn in at a random spawn rate between 40 and 70 ticks
            if knight_tick >= knight_spawn_rate:
                xpos = random.randint(objs.Knight.WIDTH, width-objs.Knight.WIDTH)
                ypos = random.randint(objs.Knight.HEIGHT, height-objs.Knight.HEIGHT)
                knights.append(objs.Knight((xpos, ypos)))
                knight_tick = 0
                knight_spawn_rate = random.randint(40,70)
            
            #updates pawn to face player
            for pawn in pawns:
                pawn.facePlayer(player)

            #updates knights to face player and updates their movements
            for knight in knights:
                knight.facePlayer(player)
                knight.movement()

            #checks if kiwi has expired to delete it, otherwise update movement
            for kiwi in kiwi_thrown:
                if kiwi.end == True:
                    kiwi_thrown.remove(kiwi)
                else:
                    kiwi.movement(winsize)

            #checks if starfruit has expired to delete it, otherwise update movement
            for starfruit in starfruit_thrown:
                if starfruit.end == True:
                    starfruit_thrown.remove(starfruit)
                else:
                    starfruit.movement(winsize)

            #draw background
            screen.fill(bck_color)
            
            #draw kiwi updated image at its center
            for kiwi in kiwi_thrown:
                screen.blit(kiwi.image, \
                (kiwi.rect.centerx - int(kiwi.image.get_width() / 2), \
                kiwi.rect.centery - int(kiwi.image.get_height() / 2)))

            #draw starfruit updated image at its center
            for starfruit in starfruit_thrown:
                screen.blit(starfruit.image, \
                (starfruit.rect.centerx - int(starfruit.image.get_width() / 2), \
                starfruit.rect.centery - int(starfruit.image.get_height() / 2)))
            
            #draw pawn updated image
            for pawn in pawns:
                screen.blit(pawn.image, pawn.rect.center)
            
            #draw knight updated image
            for knight in knights:
                screen.blit(knight.image, knight.rect.center)
            
            #draw player and it's arrows with updated player image at its center
            screen.blit(player.moving_arrow, player.moving_arrow_rect.center)
            screen.blit(player.facing_arrow, player.facing_arrow_rect.center)
            screen.blit(player.image, \
                (player.rect.centerx - int(player.image.get_width() / 2), \
                player.rect.centery - int(player.image.get_height() / 2)))

            #draw text
            screen.blit(buttons['pause'].surface, buttons['pause'].rect)
            screen.blit(texts['score'].surface, texts['score'].rect)
            screen.blit(texts['lives'].surface, texts['lives'].rect)

            pygame.display.flip()

            #counters to prevent bullet laser spraying
            kiwi_tick += 1
            starfruit_tick += 1
            pawn_tick += 1
            knight_tick += 1

            #life check
            if player.lives <= 0:
                in_game_state = False
                in_end_game_state = True
                break
            
            #checks if player clicked pause buttons
            if buttons['pause'].clicked == True:
                in_game_state = False
                paused_state = True
                break

        while paused_state == True:

            buttons['resume'].clicked = False
            buttons['exit'].clicked = False
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
                        elif mx in range(buttons['exit'].rect.left, \
                            buttons['exit'].rect.right) and \
                            my in range(buttons['exit'].rect.top, \
                            buttons['exit'].rect.bottom):
                            buttons['exit'].clicked = True      

            #keep reading serial monitor lines to prevent in game moving on pause screen
            arduino.readline().decode(errors="ignore")

            screen.fill(pause_color)
            screen.blit(titles['paused'].surface, titles['paused'].rect)
            screen.blit(buttons['resume'].surface, buttons['resume'].rect)
            screen.blit(buttons['exit'].surface, buttons['exit'].rect)
            pygame.display.flip()
            if buttons['resume'].clicked == True:
                paused_state = False
                in_game_state = True
                break
            if buttons['exit'].clicked == True:
                sys.exit()
        
        while in_end_game_state == True:
            
            buttons['restart'].clicked = False
            buttons['exit'].clicked = False
            mx, my = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if input_box.done == False:
                    input_box.handle_event(event)
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if mx in range(buttons['restart'].rect.left, \
                            buttons['restart'].rect.right) and \
                            my in range(buttons['restart'].rect.top, \
                            buttons['restart'].rect.bottom):
                            buttons['restart'].clicked = True
                        elif mx in range(buttons['exit'].rect.left, \
                            buttons['exit'].rect.right) and \
                            my in range(buttons['exit'].rect.top, \
                            buttons['exit'].rect.bottom):
                            buttons['exit'].clicked = True
            
            arduino.readline().decode(errors="ignore")
            
            if (input_box.done == True) and (updated == False):
                if nameCheck(input_box.name)==True:
                    updateLeaderboard(input_box.name, score)
                    getTopSix()
                    updated = True
                else:
                    input_box.done = False
            
            screen.fill(pause_color)
            if input_box.done == False:
                screen.blit(titles['end'].surface, titles['end'].rect)
                screen.blit(texts['lbname'].surface, texts['lbname'].rect)
                input_box.draw(screen)
            else:
                screen.blit(titles['lb'].surface, titles['lb'].rect)
                screen.blit(texts['lb1'].surface, texts['lb1'].rect)
                screen.blit(texts['lb2'].surface, texts['lb2'].rect)
                screen.blit(texts['lb3'].surface, texts['lb3'].rect)
                screen.blit(texts['lb4'].surface, texts['lb4'].rect)
                screen.blit(texts['lb5'].surface, texts['lb5'].rect)
                screen.blit(texts['lb6'].surface, texts['lb6'].rect)  
            screen.blit(buttons['restart'].surface, buttons['restart'].rect)
            screen.blit(buttons['exit'].surface, buttons['exit'].rect)
            pygame.display.flip()
            
            if buttons['restart'].clicked == True:
                player.lives = 5
                score = 0
                starfruit_thrown.clear()
                kiwi_thrown.clear()
                pawns.clear()
                knights.clear()
                input_box.done = False
                updated = False
                in_end_game_state = False
                paused_state = False
                in_game_state = True
                break
            if buttons['exit'].clicked == True:
                sys.exit()   