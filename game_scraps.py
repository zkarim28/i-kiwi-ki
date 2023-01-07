#object will bounce reverse speed when bounced against border:
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = - speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]

#brain dead way of checking through chars in list
    # counter = 0
    # counter += data.count('X')
    # counter += data.count('Y')
    # counter += data.count('B')
    # counter += data.count('R')
    # counter += data.count('P')

#movement based on joystick sensor data
        # if (x_data < -100 or x_data > 100) or (y_data < -100 or y_data > 100):
        #     wspeed = (x_data/50,-y_data/50)
        # else:
        #     wspeed = (0,0)
        # if (wrect.left <= 0 and x_data < 0) or (wrect.right >= size[0] and x_data > 0):
        #     wspeed = (0, -y_data/50)
        # if (wrect.top <= 0 and y_data > 0) or (wrect.bottom >= size[1] and y_data < 0):
        #     wspeed = (x_data/50, 0)
        # if ((wrect.left <= 0 and x_data < 0) and (wrect.top <= 0 and y_data > 0)) or \
        #     ((wrect.right >= size[0] and x_data > 0) and (wrect.top <= 0 and y_data > 0)) or \
        #     ((wrect.left <= 0 and x_data < 0) and (wrect.bottom >= size[1] and y_data < 0)) or \
        #     ((wrect.right >= size[0] and x_data > 0) and (wrect.bottom >= size[1] and y_data < 0)):
        #     wspeed = (0,0)
        # wrect = wrect.move(wspeed)

#movement based on accelerometer sesnosr data
        #Accelerometer movement
        # if (aX_data < -2000 or aX_data > 2000) or (aaY_data < -4000 or aY_data > 4000):
        #     zspeed = (aX_data/1000, -aY_data/1000)
        # else:
        #     zspeed = (0,0)
        # zrect = zrect.move(zspeed)

        #Static movement of player with accelerometer data
        # if (aX_data < -1000 or aX_data > 1000) or (aY_data < -1000 or aY_data > 1000):
        #     speed = (aX_data/500,-aY_data/500)
        # else:
        #     speed = (0,0)
        # if (self.rect.left <= 0 and aX_data < 0) or (self.rect.right >= winsize[0] and aX_data > 0):
        #     speed = (0, -aY_data/500)
        # if (self.rect.top <= 0 and aY_data > 0) or (self.rect.bottom >= winsize[1] and aY_data < 0):
        #     speed = (aX_data/500, 0)
        # if ((self.rect.left <= 0 and aX_data < 0) and (self.rect.top <= 0 and aY_data > 0)) or \
        #     ((self.rect.right >= winsize[0] and aX_data > 0) and (self.rect.top <= 0 and aY_data > 0)) or \
        #     ((self.rect.left <= 0 and aX_data < 0) and (self.rect.bottom >= winsize[1] and aY_data < 0)) or \
        #     ((self.rect.right >= winsize[0] and aX_data > 0) and (self.rect.bottom >= winsize[1] and aY_data < 0)):
        #     speed = (0,0)
        # self.rect = self.rect.move(speed)

    # def faceCheck(self, jX_data, jY_data):
    #     ang_dif = math.atan2(jX_data, jY_data) - math.atan2(self.facing[0], self.facing[1])
    #     angleRad = (math.atan2(self.rect.y-mY, mX-self.rect.x)) # y is reversed due to top-left coordinate system
    #     if ang_dif > 0:
    #         pygame.transform.rotate(self.image, data_ang)
    #     data_ang = math.degrees(math.atan2(jY_data, jX_data))
    #     if (jX_data < -100 or jX_data > 100) or (jY_data < -100 or jY_data > 100):
    #         pygame.transform.rotate(self.image, data_ang)

    # def turn(self, jX_data, jY_data):
    #     if (jX_data < -100 or jX_data > 100) or (jY_data < -100 or jY_data > 100):
    #         data_ang = (math.atan2(jY_data, jX_data))
    #         data_vector = (math.cos(data_ang), math.sin(data_ang))
            
    #         # relative_vector = (jX_data - self.rect.centerx, jY_data - self.rect.centery)
    #         #rel_vec_ang = math.atan2(relative_vector[1], relative_vector[0])
            
    #         player_ang = (math.atan2(self.facing[1], self.facing[0]))
    #         turn_ang = data_ang - player_ang
    #         turn_ang = math.degrees(turn_ang)
    #         if turn_ang not in range(-10,10):
    #             self.facing = (math.cos(data_ang), math.sin(data_ang))
    #             img_copy = pygame.transform.rotate(self.image, turn_ang)
    #             self.image = img_copy

#moving_arrow:
            # self.moving_ang = (math.atan2(-aY_data,aX_data))
            # norm = math.sqrt(math.pow(aX_data,2)+math.pow(aY_data,2))/5000
            # self.moving_vector = ((math.cos(self.moving_ang)*50)*norm,\
            #   math.sin(self.moving_ang)*50*norm)