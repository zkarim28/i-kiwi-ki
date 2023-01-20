import pygame

class Text(object):

    pygame.font.init()
    TITLE = pygame.font.SysFont("Arial", 75, bold = True)
    TEXT = pygame.font.SysFont("Arial", 40)
    BUTTON = pygame.font.SysFont("Arial", 60, italic = True)

    def __init__(self, winsize, text, color, style, loc, starting = None, coord = (0,0)):
        
        """
        winsize is a tuple of (x,y)
        text is a string
        color is a tuple of valid RGB values
        loc is a string:
        - TOPLEFT
        - TOPRIGHT
        - BOTTOMLEFT
        - BOTTOMRIGHT
        - MIDTOP
        - MIDRIGHT
        - MIDBOTTOM
        - MIDLEFT
        - CETNER
        - CUSTOM: tuple of coordinates 

        style is a string that tells what types of text or button to use
        - TITLE
        - TEXT
        - BUTTON
        """

        isinstance(winsize, tuple)
        isinstance(text, str)
        assert isinstance(color, tuple) == True 
        for num in color:
            assert num >=0 and num <=255
        assert isinstance(loc, tuple) or isinstance(loc, str)
        isinstance(type, str)
        
        if style == "TITLE":
            self.surface = self.TITLE.render(text, False, color)
        elif style == "TEXT":
            self.surface = self.TEXT.render(text, False, color)
        elif style == "BUTTON":
            self.surface = self.BUTTON.render(text, False, color)
            self.clicked = False

        self.rect = self.surface.get_rect()

        if loc == "TOPLEFT":
            self.rect.topleft = (0,0)
        elif loc == "TOPRIGHT":
            self.rect.topright = (winsize[0], 0)
        elif loc == "BOTTOMLEFT":
            self.rect.bottomleft = (0, winsize[1])
        elif loc == "BOTTOMRIGHT":
            self.rect.bottomright = (winsize[0], winsize[1])
        elif loc == "MIDTOP":
            self.rect.midtop = (winsize[0]/2, 0)
        elif loc == "MIDRIGHT":
            self.rect.midright = (winsize[0], winsize[1]/2)
        elif loc == "MIDBOTTOM":
            self.rect.midbottom = (winsize[0]/2, winsize[1])
        elif loc == "MIDLEFT":
            self.rect.midleft = (0, winsize[1]/2)
        elif loc == "CENTER":
            self.rect.center = (winsize[0]/2, winsize[1]/2)
        elif loc == "CUSTOM":
            if starting == "TOPLEFT":
                self.rect.topleft = (coord[0], coord[1])
            elif starting == "TOPRIGHT":
                self.rect.topright = (coord[0], coord[1])
            elif starting == "BOTTOMLEFT":
                self.rect.bottomleft = (coord[0], coord[1])
            elif starting == "BOTTOMRIGHT":
                self.rect.bottomright = (coord[0], coord[1])
            elif starting == "MIDTOP":
                self.rect.midtop = (coord[0], coord[1])
            elif starting == "MIDRIGHT":
                self.rect.midright = (coord[0], coord[1])
            elif starting == "MIDBOTTOM":
                self.rect.midbottom = (coord[0], coord[1])
            elif starting == "MIDLEFT":
                self.rect.midleft = (coord[0], coord[1])
            elif starting == "CENTER":
                self.rect.center = (coord[0], coord[1])


class InputBox:

    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 50)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.center = (x,y)
        self.color = (255,255,255)
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False
        self.name = 0
        self.done = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.name = self.text
                    self.text = ''
                    self.done = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)