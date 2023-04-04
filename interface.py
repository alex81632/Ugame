import pygame

class Button: 
    def __init__(self, text,  pos, font, feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.Font('fonts/dogicapixel.ttf', font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text)
 
    def change_text(self, text, color = (20, 20, 20)):
        self.text = self.font.render(text, 1, color)
        self.size = self.text.get_size()
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def display(self):
        return self.text, self.rect
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback)
                    return True
        return False
    
    def hover(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.change_text(self.feedback, (255, 30, 30))
            return True
        else:
            self.change_text(self.feedback)

    def get_size(self):
        return self.size
    
    def translate(self, x, y):
        self.x += x
        self.y += y
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

class Menu:
    def __init__(self, w, h):
        self.display = False
        self.padding = int(w/100)
        self.actual_button = 'Resume'
        self.w = w
        self.h = h
        self.menu_overlay = pygame.image.load('assets/menu_overlay.png').convert_alpha()
        scale = self.menu_overlay.get_width()/self.menu_overlay.get_height()
        self.menu_overlay = pygame.transform.scale(self.menu_overlay, (self.h*scale, self.h))
        self.scale = int(w/50)
        self.resume_button = Button("Resume", (0, 0), font= self.scale, feedback="Resume")
        self.resume_button.translate(self.w - self.resume_button.get_size()[0] - self.padding, self.padding + 300)
        self.settings_button = Button("Settings", (0, 0), font= self.scale, feedback="Settings")
        self.settings_button.translate(self.w - self.settings_button.get_size()[0] - self.padding, self.settings_button.get_size()[1]*2 + self.padding +300)
        self.exit_button = Button("Exit", (0, 0), font= self.scale, feedback="Exit")
        self.exit_button.translate(self.w - self.exit_button.get_size()[0] - self.padding, self.exit_button.get_size()[1]*5 + self.padding +300)
        
    
    def set_display(self, display):
        self.display = display
 
    def render(self, WIN, keys_pressed, general_volume, released_up, released_down):
        if not self.display:
            s = pygame.Surface((self.w,self.h))  
            s.set_alpha(128)                
            s.fill((0,0,0))           
            WIN.blit(s, (0,0))
            WIN.blit(self.menu_overlay, (self.w - self.menu_overlay.get_width(), 0))
            self.display = True

        if keys_pressed[pygame.K_UP] and released_up:
            if(self.actual_button == 'Resume'):
                self.actual_button = 'Exit'
            elif(self.actual_button == 'Settings'):
                self.actual_button = 'Resume'
            elif(self.actual_button == 'Exit'):
                self.actual_button = 'Settings'
        elif keys_pressed[pygame.K_DOWN] and released_down:
            if(self.actual_button == 'Resume'):
                self.actual_button = 'Settings'
            elif(self.actual_button == 'Settings'):
                self.actual_button = 'Exit'
            elif(self.actual_button == 'Exit'):
                self.actual_button = 'Resume'
        
        if(self.resume_button.hover()):
            self.actual_button = 'Resume'
        if(self.settings_button.hover()):
            self.actual_button = 'Settings'
        if(self.exit_button.hover()):
            self.actual_button = 'Exit'

        if(self.actual_button == 'Resume'):
            self.resume_button.change_text("Resume", (255, 30, 30))
            self.settings_button.change_text("Settings")
            self.exit_button.change_text("Exit")
        elif(self.actual_button == 'Settings'):
            self.resume_button.change_text("Resume")
            self.settings_button.change_text("Settings", (255, 30, 30))
            self.exit_button.change_text("Exit")
        elif(self.actual_button == 'Exit'):
            self.resume_button.change_text("Resume")
            self.settings_button.change_text("Settings")
            self.exit_button.change_text("Exit", (255, 30, 30))
        
        surface, rect = self.exit_button.display()
        WIN.blit(surface, rect)
        surface, rect = self.settings_button.display()
        WIN.blit(surface, rect)
        surface, rect = self.resume_button.display()
        WIN.blit(surface, rect)
 
    def click(self):
        return False

    def exit(self, event):
        if self.exit_button.click(event):
            return True
        return False
    
    def get_choice(self):
        return self.actual_button

class InitialScreen:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.scale = int(w/50)
        self.padding = int(w/100)
        self.start_button = Button("Start", (0, 0), font= self.scale, feedback="Start")
        self.start_button.translate(self.w/2 - self.start_button.get_size()[0]/2, self.h*3/4)
        self.exit_button = Button("Exit", (0, 0), font= self.scale, feedback="Exit")
        self.exit_button.translate(self.w/2 - self.exit_button.get_size()[0]/2, self.exit_button.get_size()[1] + self.h*3/4 + self.padding )
        self.actual_button = 'Start'

    def get_actual_button(self):
        return self.actual_button
    
    def render(self, WIN, keys_pressed, released_up, released_down):
        WIN.fill((0,0,0))
        #display noise background
        noise = pygame.image.load('assets/noise.png')
        #make noise pattern repeat
        for i in range(0, self.w, noise.get_width()):
            for j in range(0, self.h, noise.get_height()):
                WIN.blit(noise, (i, j))
        # display vignette
        # vignette = pygame.image.load('assets/vignette.png')
        # vignette = pygame.transform.scale(vignette, (self.w, self.h))
        # WIN.blit(vignette, (0,0))
        # display logo at center
        logo = pygame.image.load('assets/logo.png')
        logo = pygame.transform.scale(logo, (self.w/4, self.w/4))
        WIN.blit(logo, (self.w/2 - logo.get_width()/2, self.h/2 - logo.get_height()/2))
        # display start button

        if keys_pressed[pygame.K_UP] and released_up:
            if(self.actual_button == 'Start'):
                self.actual_button = 'Exit'
            elif(self.actual_button == 'Exit'):
                self.actual_button = 'Start'
        elif keys_pressed[pygame.K_DOWN] and released_down:
            if(self.actual_button == 'Start'):
                self.actual_button = 'Exit'
            elif(self.actual_button == 'Exit'):
                self.actual_button = 'Start'

        if(self.start_button.hover()):
            self.actual_button = 'Start'
        if(self.exit_button.hover()):
            self.actual_button = 'Exit'

        if(self.actual_button == 'Start'):
            self.start_button.change_text("Start", (255, 30, 30))
            self.exit_button.change_text("Exit", (255, 255, 255))
        elif(self.actual_button == 'Exit'):
            self.start_button.change_text("Start", (255, 255, 255))
            self.exit_button.change_text("Exit", (255, 30, 30))
        
        surface, rect = self.exit_button.display()
        WIN.blit(surface, rect)
        surface, rect = self.start_button.display()
        WIN.blit(surface, rect)

# def render_init(WIN):
#     WIN.fill((0,0,0))
#     #display noise background
#     noise = pygame.image.load('assets/noise.png')
#     #make noise pattern repeat
#     for i in range(0, WIDTH, noise.get_width()):
#         for j in range(0, HEIGHT, noise.get_height()):
#             WIN.blit(noise, (i, j))
#     # display vignette
#     vignette = pygame.image.load('assets/vignette.png')
#     vignette = pygame.transform.scale(vignette, (WIDTH, HEIGHT))
#     WIN.blit(vignette, (0,0))
#     # display logo at center
#     logo = pygame.image.load('assets/logo.png')
#     logo = pygame.transform.scale(logo, (WIDTH/4, WIDTH/4))
#     WIN.blit(logo, (WIDTH/2 - logo.get_width()/2, HEIGHT/2 - logo.get_height()/2))
#     font = pygame.font.Font('fonts/dogicapixel.ttf', int(WIDTH/80))
#     text = font.render("Aperte espaço para iniciar...", True, (255,255,255))
#     #make text fade in and out
#     constant = time.time()
#     constant = 255*math.sin(constant*math.pi*3/4)
#     if constant < 0:
#         constant = -constant
#     text.set_alpha(constant)
#     WIN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 + logo.get_height()))
