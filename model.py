from turtle import update
import pygame
import time

HERO_ASSET = 'assets/imgs/Sprites/HeroKnight/'
Warlock_ASSET = 'assets/imgs/Sprites/Warlock/'
Skeleton_ASSET = 'assets/imgs/Sprites/Skeleton/'

class Hero(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxHp = 80
        self.hp = 80
        self.attack = 20
        self.coolDown = 0.5
        self.damageCoolDown = 2.5
        self.status = 'idle'
        self.direction = 1
        self.velocity = 12
        self.index = 0
        self.last = time.time()
        self.lasthurt = time.time()
        self.images = {
            'idle': [pygame.image.load(HERO_ASSET + f'idle/HeroKnight_Idle_{i+1}.png') for i in range(0, 7)],
            'run': [pygame.image.load(HERO_ASSET + f'run/HeroKnight_Run_{i+1}.png') for i in range(0, 9)],
            'jump': [pygame.image.load(HERO_ASSET + f'Jump/HeroKnight_Jump_{i+1}.png') for i in range(0, 5)],
            'fall': [pygame.image.load(HERO_ASSET + f'fall/HeroKnight_fall_{i+1}.png') for i in range(0, 3)],
            'attack' : [pygame.image.load(HERO_ASSET + f'Attack1/HeroKnight_Attack1_{i+1}.png') for i in range(0, 5)],
            'attack2' : [pygame.image.load(HERO_ASSET + f'Attack2/HeroKnight_Attack2_{i+1}.png') for i in range(0, 5)],
            'attack3' : [pygame.image.load(HERO_ASSET + f'Attack3/HeroKnight_Attack3_{i+1}.png') for i in range(0, 7)],
            'hurt': [pygame.image.load(HERO_ASSET + f'Hurt/HeroKnight_Hurt_{i+1}.png') for i in range(0, 11)],
            'block' : [pygame.image.load(HERO_ASSET + f'BlockIdle/HeroKnight_Block Idle_{i+1}.png') for i in range(0, 7)],
            'death' : [pygame.image.load(HERO_ASSET + f'Death/HeroKnight_Death_{i+1}.png') for i in range(0, 9)]

        }

        image_surf = pygame.image.load(HERO_ASSET + 'idle/HeroKnight_Idle_0.png').convert()
        self.image = pygame.Surface((100,55))
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.healthBar = HealthBar(self)

    def update(self, controls):
        print(pygame.mixer.get_num_channels())
        if self.hp <= 0:
            self.status = 'death'
            if self.index == len(self.images[self.status]) - 1:
                self.kill()
                pygame.mixer.music.load('assets/sounds/mixkit-player-losing-or-failing-2042.wav')
                pygame.mixer.music.play()
        new = time.time()
        if self.index == len(self.images[self.status]) - 1 or self.status in ['idle', 'run', 'block'] and self.status != 'death':
            if controls['attack'] and (new-self.last > self.coolDown):
                pygame.mixer.music.load('assets/sounds/mixkit-sword-blade-attack-in-medieval-battle-2762.wav')
                pygame.mixer.music.play()
                if controls['block']:
                    self.status = 'attack2'
                elif self.status == 'run':
                    self.status = 'attack3'
                else:
                    self.status = 'attack'
                self.index = 0
                self.last = time.time()
            elif controls['up'] or controls['down'] or controls['left'] or controls['right']:
                self.status = 'run'
                self.movement_wrapper(controls['up'], controls['down'], controls['left'], controls['right'])
            elif controls['block']:
                self.status = 'block'
            else:
                self.status = 'idle'
        self.index = (self.index + 1) % len(self.images[self.status])
        self.image = self.images[self.status][self.index]
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def movement_wrapper(self, up, down, left, right):
        x = 0
        y = 0
        if up:
            y = -1
        elif down:
            y = 1
        if left:
            x = -1
            self.direction = -1
        elif right:
            x = 1
            self.direction = 1
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity

    def update_collisiton(self, battle):
        status = ['attack', 'attack1', 'attack2']
        new = time.time()
        if len(battle) > 0:
            if self.status in status:
                for monster in battle:
                    monster.hp -= self.attack
            else:
                for monster in battle:
                    if new - self.lasthurt > self.damageCoolDown:
                        self.hp -= monster.attack
                        if self.hp > 0:
                            pygame.mixer.music.load('assets/sounds/mixkit-human-fighter-pain-scream-2768.wav')
                            pygame.mixer.music.play()
                        self.lasthurt = time.time()
                        self.index = 0
                        self.update_hurt()

    def update_hurt(self):
        print('hurt')
        self.status = 'hurt'
        self.rect.x -= self.direction * 15
        self.image = self.images[self.status][self.index]
        self.index = (self.index + 1) % len(self.images[self.status])
        print(self.index)
        if self.index == len(self.images[self.status]) - 1:
            self.status = ['idle']
            print('end')
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Tester(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.maxHp = 200
        self.hp = 80
        self.attack = 20

        image_surf = pygame.image.load('tester.png').convert()
        self.image = pygame.Surface((44,55))
        image_surf = pygame.transform.flip(image_surf, True, False)
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if (self.hp <= 0):
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Skeleton_blue(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 50
        self.state = 'born'
        self.index = 0
        self.image = pygame.Surface((64,64))
        self.image_surf = pygame.image.load(Skeleton_ASSET + f'SkeletonMage_Blue.png').convert()
        self.image.blit(self.image_surf,(0,0),(180,0,64,64))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)
        self.image_rects = {
            'idle' : [pygame.Rect(0,64,64,64),pygame.Rect(64,64,64,64),pygame.Rect(128,64,64,64),pygame.Rect(192,64,64,64)],
            'run' : [pygame.Rect(0,320,64,64),pygame.Rect(64,320,64,64),pygame.Rect(128,320,64,64),
                        pygame.Rect(192,320,64,64),pygame.Rect(256,320,64,64),pygame.Rect(320,320,64,64)],
            'attack' : [pygame.Rect(0,576,64,64),pygame.Rect(64,576,64,64),pygame.Rect(128,576,64,64),
                        pygame.Rect(192,576,64,64),pygame.Rect(256,576,64,64),pygame.Rect(320,576,64,64),
                        pygame.Rect(384,576,64,64),pygame.Rect(448,576,64,64)],
            'born' : [pygame.Rect(0,1088,64,64),pygame.Rect(64,1088,64,64),pygame.Rect(128,1088,64,64),
                        pygame.Rect(192,1088,64,64),pygame.Rect(256,1088,64,64),pygame.Rect(320,1088,64,64),
                        pygame.Rect(384,1088,64,64),pygame.Rect(448,1088,64,64),pygame.Rect(512,1088,64,64)],
            'hurt' : [pygame.Rect(0,1280,64,64),pygame.Rect(64,1280,64,64),pygame.Rect(128,1280,64,64),
                        pygame.Rect(192,1280,64,64),pygame.Rect(256,1280,64,64),pygame.Rect(320,1280,64,64)],
            'death' : [pygame.Rect(0,1472,64,64),pygame.Rect(64,1472,64,64),pygame.Rect(128,1472,64,64),
                        pygame.Rect(192,1472,64,64),pygame.Rect(256,1472,64,64),pygame.Rect(320,1472,64,64),
                        pygame.Rect(384,1472,64,64)]
        }

    def update(self):
        if self.state == 'born' and self.index == 8:
            self.state = 'idle'
            self.index = 0
        if self.hp < 0:
            self.state == 'death'
        if self.state == 'death' and self.index == 6:
            self.kill()
        self.index = (self.index + 1)%len(self.image_rects[self.state])
        self.image.blit(self.image_surf,(0,0),self.image_rects[self.state][self.index])
    def draw(self, surface):

        surface.blit(self.image, self.rect)

class Skeleton_red(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 80
        self.state = 'born'
        self.index = 0
        self.image = pygame.Surface((64,64))
        self.image_surf = pygame.image.load(Skeleton_ASSET + f'SkeletonMage_Red.png').convert()
        self.image.blit(self.image_surf,(0,0),(180,0,64,64))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)
        self.image_rects = {
            'idle' : [pygame.Rect(0,64,64,64),pygame.Rect(64,64,64,64),pygame.Rect(128,64,64,64),pygame.Rect(192,64,64,64)],
            'run' : [pygame.Rect(0,320,64,64),pygame.Rect(64,320,64,64),pygame.Rect(128,320,64,64),
                        pygame.Rect(192,320,64,64),pygame.Rect(256,320,64,64),pygame.Rect(320,320,64,64)],
            'attack' : [pygame.Rect(0,832,64,64),pygame.Rect(64,832,64,64),pygame.Rect(128,832,64,64),
                        pygame.Rect(192,832,64,64),pygame.Rect(256,832,64,64),pygame.Rect(320,832,64,64),
                        pygame.Rect(384,832,64,64),pygame.Rect(448,832,64,64)],
            'born' : [pygame.Rect(0,1088,64,64),pygame.Rect(64,1088,64,64),pygame.Rect(128,1088,64,64),
                        pygame.Rect(192,1088,64,64),pygame.Rect(256,1088,64,64),pygame.Rect(320,1088,64,64),
                        pygame.Rect(384,1088,64,64),pygame.Rect(448,1088,64,64),pygame.Rect(512,1088,64,64)],
            'hurt' : [pygame.Rect(0,1280,64,64),pygame.Rect(64,1280,64,64),pygame.Rect(128,1280,64,64),
                        pygame.Rect(192,1280,64,64),pygame.Rect(256,1280,64,64),pygame.Rect(320,1280,64,64)],
            'death' : [pygame.Rect(0,1472,64,64),pygame.Rect(64,1472,64,64),pygame.Rect(128,1472,64,64),
                        pygame.Rect(192,1472,64,64),pygame.Rect(256,1472,64,64),pygame.Rect(320,1472,64,64),
                        pygame.Rect(384,1472,64,64)]
        }


    def update(self):
        if self.state == 'born' and self.index == 8:
            self.state = 'idle'
            self.index = 0
        if self.hp < 0:
            self.state == 'death'
        if self.state == 'death' and self.index == 6:
            self.kill()
        self.index = (self.index + 1)%len(self.image_rects[self.state])
        self.image.blit(self.image_surf,(0,0),self.image_rects[self.state][self.index])
    def draw(self, surface):

        surface.blit(self.image, self.rect)
class Warlock(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxHp = 40
        self.hp = 40
        self.attack = 10
        self.coolDown = 5
        self.damageCoolDown = 1.5
        self.status = 'idle'
        self.direction = 1
        self.velocity = 3
        self.index = 0
        self.last = time.time()
        self.lasthurt = time.time()
        self.images = {
            'idle': [pygame.image.load(Warlock_ASSET + f'Idle/Warlock_Idle_{i}.png') for i in range(0, 12)],
            'run': [pygame.image.load(Warlock_ASSET + f'Run/Warlock_Run_{i}.png') for i in range(0, 8)],
            'death': [pygame.image.load(Warlock_ASSET + f'Death/Warlock_Death_{i}.png') for i in range(0, 13)],
            'attack' : [pygame.image.load(Warlock_ASSET + f'Attack/Warlock_Attack_{i}.png') for i in range(0, 13)],
            'hurt': [pygame.image.load(Warlock_ASSET + f'Hurt/Warlock_Hurt_{i}.png') for i in range(0, 5)],
        }

        image_surf = pygame.image.load(Warlock_ASSET + 'idle/Warlock_Idle_0.png').convert()
        self.image = pygame.Surface((100,80))
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self,controls):
        new = time.time()
        if self.hp <= 0:
            self.status = "death"
            if self.index == 12:
                self.kill()
        if controls['attack'] and (new-self.last > self.coolDown):
            self.status = "attack"
            self.index = 0
            self.last = time.time()
        elif controls['up']:
            self.status = 'run'
            self.rect.y -= self.velocity
        elif controls['down']:
            self.status = 'run'
            self.rect.y += self.velocity
        elif controls['left']:
            self.direction = -1
            self.status = 'run'
            self.rect.x -= self.velocity
        elif controls['right']:
            self.direction = 1
            self.status = 'run'
            self.rect.x += self.velocity
        elif controls['hurt']:
            self.status = 'hurt'
            self.index = 0
        else:
            self.status = 'idle'
        self.index = (self.index + 1) % len(self.images[self.status])
        self.image = self.images[self.status][self.index]
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class HealthBar():

    def __init__(self, hero):
        self.healthPoint = hero.hp
        self.image = pygame.image.load('assets/imgs/heart.png').convert()
        self.image = pygame. transform. scale(self.image, (40, 40))
        self.image.set_colorkey((0,0,0))
        self.pos = (55, 50)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.fontobj = setup_fonts(24)
        self.text_pos = (20, 50)
        self.text_rect = self.image.get_rect(topleft=self.text_pos)

    def draw(self, surface):
        text_surface = self.fontobj.render('HP:', True, (255, 255, 255))
        surface.blit(text_surface, self.text_rect)
        number = self.healthPoint // 20
        for i in range(number):
            surface.blit(self.image, self.rect)
            self.rect.x += 40
        self.rect = self.image.get_rect(topleft=self.pos)

def setup_fonts(font_size, bold=False, italic=False):
    ''' Load a font, given a list of preferences

        The preference list is a sorted list of strings (should probably be a parameter),
        provided in a form from the FontBook list.
        Any available font that starts with the same letters (lowercased, spaces removed)
        as a font in the font_preferences list will be loaded.
        If no font can be found from the preferences list, the pygame default will be returned.

        returns -- A Font object
    '''
    font_preferences = ['Helvetica Neue', 'Iosevka Regular', 'Comic Sans', 'Courier New']
    available = pygame.font.get_fonts()
    prefs = [x.lower().replace(' ', '') for x in font_preferences]
    for pref in prefs:
        a = [x
             for x in available
             if x.startswith(pref)
            ]
        if a:
            fonts = ','.join(a) #SysFont expects a string with font names in it
            return pygame.font.SysFont(fonts, font_size, bold, italic)
    return pygame.font.SysFont(None, font_size, bold, italic)

class TextBox():

    def __init__(self, surface):
        self.status = 'close'
        self.surface = surface
        self.fontobj = setup_fonts(18)
        self.rect = pygame.Rect((0,0),(400, 200))
        self.rect.center = (540, 360)
        self.image_surf = pygame.image.load('pop_up.jpg').convert()
        self.image_surf = pygame. transform. scale(self.image_surf, (400, 200))



    def pop_up(self, text):
        text_surface = self.fontobj.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.surface.blit(self.image_surf, self.rect)
        self.surface.blit(text_surface, text_rect)
        self.status = 'pop_up'


    def update(self, control):
        if control['pop'] == True and self.status != 'pop_up':
            self.status = 'pop_up'
        elif control['pop'] == True and self.status == 'pop_up':
            self.status = 'close'
        if self.status == 'pop_up':
            self.pop_up('This is a pop up window')

class GameManager():

    def __init__(self) -> None:
        pass