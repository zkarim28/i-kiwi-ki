import pygame
import math
import random

class Player(object):

    JSTH = 200
    ACTH = 1000
    MOVE_RATE = 0.25
    
    def __init__(self):
        '''
        image is a string of a valid directory
        size is a tuple in the order (x,y)
        '''
        img = pygame.image.load("Player.png")
        facing_arrow = pygame.image.load("facing.png")
        moving_arrow = pygame.image.load("moving.png")
        
        self.image = pygame.transform.scale(img, (80,80))
        self.rect = self.image.get_rect()
        
        self.facing_arrow = pygame.transform.scale(facing_arrow, (12,12))
        self.facing_arrow_rect = self.facing_arrow.get_rect()
        self.facing_ang = 0
        
        self.moving_arrow = pygame.transform.scale(moving_arrow, (12, 12))
        self.moving_arrow_rect = self.moving_arrow.get_rect()
        self.moving_ang = 0
        
        self.velocity = (0,0)
        
        self.facing_vector = (0,0)
        self.moving_vector = (0,0)
        
        self.axcal = 0
        self.aycal = 0

        self.thrown = []
        self.kiwi_tick = 0

        self.lives = 5

    def movement(self, winsize, aX_data, aY_data):
        """
        monitors sensor input and determines speed of object at that instant
        also manages borders when detects image at the egdes of the screen

        winsize is a tuple
        x_data
        aY_data
        """
        self.move_vector = (aX_data/10000,-aY_data/10000)
        if (self.rect.left <= 0 and self.velocity[0] < 0) or \
            (self.rect.right >= winsize[0] and self.velocity[0] > 0):
            self.velocity = (-self.velocity[0]/2,self.velocity[1]/2)

        if (self.rect.top <= 0 and self.velocity[1] < 0) or \
            (self.rect.bottom >= winsize[1] and self.velocity[1] > 0):
            self.velocity = (self.velocity[0]/2,-self.velocity[1]/2)

        if ((self.rect.left <= 0 and self.velocity[0] < 0) and \
            (self.rect.top <= 0 and self.velocity[1] > 0)) or \
            ((self.rect.right >= winsize[0] and self.velocity[0] > 0) and \
            (self.rect.top <= 0 and self.velocity[1] > 0)) or \
            ((self.rect.left <= 0 and self.velocity[0] < 0) and \
            (self.rect.bottom >= winsize[1] and self.velocity[1] < 0)) or \
            ((self.rect.right >= winsize[0] and self.velocity[0] > 0) and \
            (self.rect.bottom >= winsize[1] and self.velocity[1] < 0)):
            self.velocity = (-self.velocity[0]/2.0,-self.velocity[1]/2.0)

        self.rect.centerx = self.rect.centerx + self.velocity[0]
        self.rect.centery = self.rect.centery + self.velocity[1]
        self.rect = self.rect.move(self.velocity[0], self.velocity[1])
        if (aX_data < self.axcal-Player.ACTH or aX_data > self.axcal+Player.ACTH)or\
            (aY_data < self.aycal-Player.ACTH or aY_data > self.aycal+Player.ACTH):
            impulse = (self.move_vector[0] * Player.MOVE_RATE, self.move_vector[1] * Player.MOVE_RATE)
            self.velocity = (self.velocity[0] + impulse[0], \
                self.velocity[1] + impulse[1])

    def arrows(self, jX_data, jY_data, aX_data, aY_data):
        self.facing_arrow_rect.center = (self.rect.centerx + self.facing_vector[0]-7,\
            self.rect.centery + self.facing_vector[1]-7)
        self.moving_arrow_rect.center = (self.rect.centerx + self.moving_vector[0],\
            self.rect.centery + self.moving_vector[1])
        if (jX_data < -20 or jX_data > 20) or (jY_data < -20 or jY_data > 20):
            self.facing_ang = math.atan2(-jY_data,jX_data)
            self.facing_vector = (math.cos(self.facing_ang)*65,\
                math.sin(self.facing_ang)*65)
        if (aX_data < self.axcal-1000 or aX_data > self.axcal+1000) or \
            (aY_data < self.aycal-1000 or aY_data > self.aycal+1000):
            
            if aX_data >= self.axcal:
                x = aX_data - self.axcal
            elif aX_data <= self.axcal:
                x = aX_data + self.axcal

            if aY_data >= self.aycal:
                y = aY_data - self.aycal
            elif aY_data <= self.aycal:
                y = aY_data + self.aycal

            self.moving_ang = (math.atan2(-y,x))
            norm = math.sqrt(math.pow(x,2)+math.pow(y,2))/5000
            self.moving_vector = (math.cos(self.moving_ang)*50*norm,\
                math.sin(self.moving_ang)*50*norm)
        else:
            self.moving_vector = (0,0)

    def calibration(self, arduino):
        data_name_list = ['X','Y','R','P','A','B']
        xsum = 0
        ysum = 0
        total_num = 250
        for i in range(total_num):
            while True:
                data = arduino.readline().decode(errors="ignore")
                name_count = 0
                for char in data:
                    if char in data_name_list:
                        name_count+=1
                if name_count == 6:
                    aX_data = int(data[data.index("R")+2:data.index("P")])
                    aY_data = int(data[data.index("P")+2:data.index("A")])  
                    xsum += aX_data
                    ysum += aY_data
                    break
                else:
                    continue
        self.axcal = xsum/total_num
        self.aycal = ysum/total_num

    def collision(self, enemy_list, hurt_sound):
        for enemy in enemy_list:
            if pygame.Rect.colliderect(self.rect, enemy.rect):
                enemy_list.remove(enemy)
                self.hit = True
                self.lives -=1 
                hurt_sound.play()      


class Bullets(object):
    
    def __init__(self, direction, player_center, img):
        image = pygame.image.load(img)
        self.image = pygame.transform.scale(image, (70,70))
        self.rect = self.image.get_rect()
        self.rect.center = player_center
        self.velocity = (direction[0],direction[1])
        self.impulse = (-direction[0]/12, -direction[1]/12)
        self.hit = False
        self.end = False
    
    def movement(self, winsize):
        self.rect.center = (self.rect.centerx + self.velocity[0], \
        self.rect.centery + self.velocity[1])
        self.velocity = (self.velocity[0] + self.impulse[0], \
            self.velocity[1] + self.impulse[1])
        if self.impulse[0] > 0 and self.impulse[1] > 0:
            if self.velocity[0] >= 0 and self.velocity[1] >= 0:
                self.end = True
        if self.impulse[0] > 0 and self.impulse[1] < 0:
            if self.velocity[0] >= 0 and self.velocity[1] <= 0:
                self.end = True
        if self.impulse[0] < 0 and self.impulse[1] > 0:
            if self.velocity[0] <= 0 and self.velocity[1] >= 0:
                self.end = True
        if self.impulse[0] < 0 and self.impulse[1] < 0:
            if self.velocity[0] <= 0 and self.velocity[1] <= 0:
                self.end = True
        if self.velocity[0] == 0 and self.velocity[1] == 0:
            self.end = True
        
        if self.rect.left < 0 or self.rect.right > winsize[0] or \
            self.rect.top < 0 or self.rect.bottom > winsize[1]:
            self.end = True
            
    def collision(self, kiwi_list):
        for kiwi in kiwi_list:
            if pygame.Rect.colliderect(self.rect, kiwi.rect):
                kiwi_list.remove(kiwi)
                self.hit = True


class Pawn(object):

    WIDTH = 70
    HEIGHT = 70

    def __init__(self, loc):
        
        img = pygame.image.load("pinapple.png")

        self.image = pygame.transform.scale(img, (Pawn.WIDTH, Pawn.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (loc[0],loc[1])
        self.health = 1
        self.hit = False
        self.facing_vector = (0,0)
        self.fireRate = random.randrange(25, 60)

    def facePlayer(self, player):

        vector = (player.rect.x-self.rect.x, \
            player.rect.y - self.rect.y)
        norm = math.sqrt(math.pow(player.rect.x-self.rect.x,2)\
            +math.pow(player.rect.y - self.rect.y,2))

        self.facing_vector = ((vector[0]/norm)*50, \
            (vector[1]/norm)*50) 
    
    def collision(self, kiwi_list):
        
        for kiwi in kiwi_list:
            if pygame.Rect.colliderect(self.rect, kiwi.rect):
                kiwi_list.remove(kiwi)
                self.hit = True
            
                        
class Knight(object):

    WIDTH = 60
    HEIGHT = 60
    
    def __init__(self, loc):
        
        img = pygame.image.load("apple.png")

        self.image = pygame.transform.scale(img, (Knight.WIDTH, Knight.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (loc[0],loc[1])
        self.health = 3
        self.hit = False

        self.facing_vector = (0,0)

    def facePlayer(self, player):

        vector = (player.rect.x-self.rect.x, \
            player.rect.y - self.rect.y)
        norm = math.sqrt(math.pow(player.rect.x-self.rect.x,2)\
            +math.pow(player.rect.y - self.rect.y,2))
        if norm == 0:
            norm = 1
        self.facing_vector = ((vector[0]/norm)*2, (vector[1]/norm)*2) 
    
    def movement(self):

        self.rect.centerx = self.rect.centerx + self.facing_vector[0]
        self.rect.centery = self.rect.centery + self.facing_vector[1]
        self.rect = self.rect.move(self.facing_vector[0], self.facing_vector[1])
    
    def collision(self, kiwi_list):
        
        for kiwi in kiwi_list:
            if pygame.Rect.colliderect(self.rect, kiwi.rect):
                kiwi_list.remove(kiwi)
                self.hit = True