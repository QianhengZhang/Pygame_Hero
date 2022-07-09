from turtle import update
from unittest import result
import pygame
import time
import random

HERO_ASSET = 'assets/imgs/Sprites/HeroKnight/'
WARLOCK_ASSET = 'assets/imgs/Sprites/Warlock/'
SKELETON_ASSET = 'assets/imgs/Sprites/Skeleton/'
BOSS_ASSET = 'assets/imgs/Sprites/Boss/'

class Hero(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxHp = 200
        self.hp = 200
        self.type = 'hero'
        self.attack = 200
        self.coolDown = 0.7
        self.damageCoolDown = 2.5
        self.status = 'idle'
        self.direction = 1
        self.velocity = 12
        self.index = 0
        self.last = time.time()
        self.last_hurt = time.time()
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
            'block_success' : [pygame.image.load(HERO_ASSET + f'Block/HeroKnight_Block_{i+1}.png') for i in range(0, 4)],
            'death' : [pygame.image.load(HERO_ASSET + f'Death/HeroKnight_Death_{i+1}.png') for i in range(0, 9)]

        }

        image_surf = pygame.image.load(HERO_ASSET + 'idle/HeroKnight_Idle_0.png').convert()
        image_surf = pygame.transform.scale(image_surf, (150, 72))
        self.image = pygame.Surface((100,55))
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, controls):
        if self.hp <= 0:
            self.status = 'death'
            if self.index == len(self.images[self.status]) - 1:
                self.kill()
                pygame.mixer.music.load('assets/sounds/mixkit-player-losing-or-failing-2042.wav')
                pygame.mixer.music.play()
        new = time.time()
        if self.status == 'block_sucess' and self.index == len(self.images[self.status]) - 1:
            self.status = 'block'
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
                if self.status != 'block_success' or (self.status == 'block_success' and self.index == len(self.images[self.status]) - 1 ):
                    self.status = 'block'
            else:
                self.status = 'idle'
        self.index = (self.index + 1) % len(self.images[self.status])
        self.image = self.images[self.status][self.index]
        self.image = pygame.transform.scale(self.image, (150, 72))
        self.mask = pygame.mask.from_surface(self.image)
        if self.status in ['attack', 'attack2', 'attack3']:
            self.mask =  pygame.mask.from_surface( pygame.transform.scale(self.image, (165, 80)))
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def movement_wrapper(self, up, down, left, right):
        x = 0
        y = 0
        if up and self.rect.y > 344:
            y = -1
        elif down and self.rect.y < 700:
            y = 1
        if left and self.rect.x > -50:
            x = -1
            self.direction = -1
        elif right and self.rect.x < 950:
            x = 1
            self.direction = 1
        self.rect.x += x * self.velocity
        self.rect.y += y * self.velocity

    def update_attack_collision(self, monsters):
        new = time.time()
        for monster in monsters:
            if (self.rect.left < monster.rect.left + monster.rect.width and
                self.rect.left + self.rect.width + 5> monster.rect.left and
                self.rect.top < monster.rect.top + monster.rect.height and
                self.rect.top + self.rect.height - 20 > monster.rect.top
            ):
                if (new- monster.last_hurt > monster.hurt_cd) and monster.state != 'death' and (self.direction == monster.direction or monster.type == 'boss'):
                    if monster.type != 'boss' or monster.state == 'run_idle':
                        monster.last_hurt = time.time()
                        monster.hp -= self.attack
                        if monster.type == 'warlock':
                            monster.state = 'hurt'
                            monster.lock = 1
                            monster.index = -1
                        elif monster.direction == 1 and monster.type == 'skeleton':
                            monster.state = 'hurt_left'
                            monster.lock = 1
                            monster.index = -1
                        elif monster.type == 'skeleton':
                            monster.state = 'hurt_right'
                            monster.lock = 1
                            monster.index = -1

    def update_hurt_collision(self, battle):
        status = ['attack', 'attack1', 'attack2']
        new = time.time()
        if len(battle) > 0:
            for monster in battle:
                if monster.state in ['attack_left', 'attack_right', 'run_attack', 'run_idle'] and new - self.last_hurt > self.damageCoolDown:
                    if self.status in ['block', 'block_success', 'attack2'] and (self.direction == monster.direction or monster.type == 'boss'):
                        self.rect.x -= monster.direction * 10
                        if monster.type != 'boss':
                            monster.rect.x += monster.direction * 20
                        else:
                            self.last_hurt = time.time()
                            self.hp -= monster.attack * 0.2
                            self.status = 'block_success'
                            self.index = 0
                    else:
                        self.hp -= monster.attack
                        if self.hp > 0:
                            pygame.mixer.music.load('assets/sounds/mixkit-human-fighter-pain-scream-2768.wav')
                            pygame.mixer.music.play()
                        self.last_hurt = time.time()
                        self.index = 0
                        self.update_hurt(monster)

    def update_bullet_collision(self, battle):
        new = time.time()
        for bullet in battle:
            if bullet.type == 'fire' and bullet.status == 'vortex' or bullet.type == 'bullet':
                if self.status in ['block', 'block_success', 'attack2'] and (self.direction == bullet.direction):
                    self.rect.x -= bullet.direction * 10
                    self.hp -= bullet.damage * 0.1
                    self.status = 'block_success'
                    self.index = 0
                else:
                    if new - self.last_hurt > self.damageCoolDown:
                        self.hp -= bullet.damage
                        if self.hp > 0:
                            pygame.mixer.music.load('assets/sounds/mixkit-human-fighter-pain-scream-2768.wav')
                            pygame.mixer.music.play()
                            self.last_hurt = time.time()
                            self.index = 0
                            self.update_hurt(bullet)
                if bullet.type == 'bullet':
                    bullet.kill()

    def update_hurt(self, monster):
        self.status = 'hurt'
        if monster.type != 'breath':
            self.rect.x -= monster.direction * 15
            if self.rect.x < -50:
                self.rect.x = -45
            elif self.rect.x > 950:
                self.rect.x = 945
        self.image = self.images[self.status][self.index]
        self.index = (self.index + 1) % len(self.images[self.status])
        if self.index == len(self.images[self.status]) - 1:
            self.status = ['idle']
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        BOSS_ASSET = 'assets/imgs/Sprites/Boss/'
        self.hp = 1200
        self.maxHp = 1200
        self.type = 'boss'
        self.attack = 40
        self.index = 0
        self.image = pygame.Surface((160,144))
        image_surf = pygame.image.load(BOSS_ASSET + '/idle/demon-idle_0.png').convert()
        self.image.blit(image_surf,(0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)
        self.state = 'fly_attack'
        self.last_hurt = time.time()
        self.hurt_cd = 0.5
        self.images = {
            'fly_idle': [pygame.image.load(BOSS_ASSET + f'idle/demon-idle_{i}.png') for i in range(0, 6)],
            'fly_attack': [pygame.image.load(BOSS_ASSET + f'attack/demon-attack_{i}.png') for i in range(0, 8)],
            'transform' : [pygame.image.load(BOSS_ASSET + f'ImpactExplosion/ImpactExplosion_{i}.png') for i in range(0, 7)],
            'run_attack': [pygame.image.load(BOSS_ASSET + f'nightmare-run/nightmare-run_{i}.png') for i in range(0, 4)],
            'run_idle': [pygame.image.load(BOSS_ASSET + f'nightmare-idle/nightmare-idle_{i}.png') for i in range(0, 4)]
        }
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.modelock = 0
        self.lock = 0
        self.callminion = 0
        self.breath = 0
        self.mode = 0
        self.framecount = 0
        self.direction = -1
        self.run_mode_step1 = 0
        self.run_mode_step2 = 0
        self.run_mode_step3 = 0
        self.run_mode_step4 = 0
        self.run_mode_step5 = 0
        self.run_mode_step6 = 0
        self.run_mode_step7 = 0
        self.run_mode_step3_direction = 1
        self.run_mode_step4_direction = 1
        self.run_mode_step5_direction = 1

    def update(self,hero_pos):
        if self.hp <= 0:
            self.kill()
        xdistance = self.rect.centerx - hero_pos[0]
        if self.modelock == 0:
            choice = random.randint(0,1)
            if choice == 0:
                self.mode = (self.mode+1)%3
            if choice == 1:
                self.mode = (self.mode-1)%3
            self.modelock = 1
            print("mode ", end= '')
            print(self.mode)
            if self.mode == 1:
                self.run_mode_step1 = 0
                self.run_mode_step2 = 0
                self.run_mode_step3 = 0
                self.run_mode_step4 = 0
                self.run_mode_step5 = 0
                self.run_mode_step6 = 0
                self.run_mode_step7 = 0
        if self.modelock == 1:
            if self.mode == 0: #breath mode
                if self.rect.y > 150:
                    self.state = 'fly_idle'
                    self.rect.move_ip(0, -3)
                    if xdistance >= 0:
                        self.direction = 1
                    else:
                        self.direction = -1
                    if xdistance > 200:
                        self.rect.move_ip(-3,0)
                    if xdistance < -200:
                        self.rect.move_ip(3,0)
                if self.rect.y <= 150:
                    self.state = 'fly_attack'
                    if self.lock == 0:
                        if self.framecount == 151:
                            self.modelock = 0
                        else:
                            self.framecount = 0
                            self.lock = 1
                    if self.lock == 1:
                        if self.framecount == 49:
                            self.breath = 0
                        if self.framecount == 48:
                            self.breath = 1
                        if self.framecount < 100 and self.framecount > 49:
                            self.index = 5
                        if self.framecount >= 100 and self.framecount < 150:
                            xdistance = self.rect.centerx - hero_pos[0]
                            if xdistance >= 0:
                                self.direction = 1
                            else:
                                self.direction = -1
                            self.state = 'fly_idle'
                        if self.framecount == 150:
                            self.lock = 0
            if self.mode == 1: #run mode
                if self.run_mode_step1 == 0:
                    if (self.rect.centery <= hero_pos[1]+10 and self.rect.centery >= hero_pos[1]-10) and (self.rect.centerx >= 850 or self.rect.centerx <= 150):
                        self.run_mode_step1 = 1
                        self.framecount = 0
                        self.index = 0
                    else:
                        self.state = 'fly_idle'
                        if self.rect.centerx > 400:
                            self.direction = -1
                        else:
                            self.direction = 1
                        if self.rect.centerx > 400 and self.rect.centerx < 850:
                            self.rect.move_ip(5,0)
                        if self.rect.centerx <= 400 and self.rect.centerx > 150:
                            self.rect.move_ip(-5,0)
                        if self.rect.centery >= hero_pos[1]+10:
                            self.rect.move_ip(0,-3)
                        if self.rect.centery <= hero_pos[1]-10:
                            self.rect.move_ip(0,3)
                if self.run_mode_step1 == 1 and self.run_mode_step2 == 0:
                    self.state = 'transform'
                    if self.framecount == 6:
                        self.run_mode_step2 = 1
                        self.index = 0
                        self.run_mode_step3_direction = self.direction *(-1)
                if self.run_mode_step2 == 1 and self.run_mode_step3 == 0:
                    self.state = 'run_attack'
                    self.direction = self.run_mode_step3_direction
                    if (self.direction == 1 and self.rect.centerx < 150) or (self.direction == -1 and self.rect.centerx >850):
                        self.run_mode_step3 = 1
                        self.index = 0
                        self.run_mode_step4_direction = -self.direction
                    else:
                        if self.direction == 1:
                            self.rect.move_ip(-15,0)
                        else:
                            self.rect.move_ip(15,0)
                if self.run_mode_step3 == 1 and self.run_mode_step4 == 0:
                    self.direction = self.run_mode_step4_direction
                    if (self.direction == 1 and self.rect.centerx < 150) or (
                            self.direction == -1 and self.rect.centerx > 850):
                        self.run_mode_step4 = 1
                        self.index = 0
                        self.run_mode_step5_direction = -self.direction
                    else:
                        if self.direction == 1:
                            self.rect.move_ip(-15, 0)
                        else:
                            self.rect.move_ip(15, 0)
                if self.run_mode_step4 == 1 and self.run_mode_step5 == 0:
                    self.direction = self.run_mode_step5_direction
                    if (self.direction == 1 and self.rect.centerx < 150) or (
                            self.direction == -1 and self.rect.centerx > 850) or (random.randint(0,15) == 0):
                        self.run_mode_step5 = 1
                        self.index = 0
                        self.framecount = 0
                    else:
                        if self.direction == 1:
                            self.rect.move_ip(-15, 0)
                        else:
                            self.rect.move_ip(15, 0)
                if self.run_mode_step5 == 1 and self.run_mode_step6 == 0:
                    self.state = 'run_idle' #only in this step player can attack boss
                    if self.framecount == 100:
                        self.run_mode_step6 = 1
                        self.framecount = 0
                        self.index = 0
                if self.run_mode_step6 == 1 and self.run_mode_step7 == 0:
                    self.state = 'transform'
                    if self.framecount == 6:
                        self.run_mode_step7 = 1
                        self.index = 0
                if self.run_mode_step7 == 1:
                    self.modelock = 0
            if self.mode == 2: #call minions mode
                self.state = 'fly_idle'
                if self.rect.y > 150:
                    self.rect.move_ip(0, -3)
                else:
                    if self.lock == 0:
                        if self.framecount >= 201:
                            self.modelock = 0
                        else:
                            self.framecount = 0
                            self.lock = 1
                    else:
                        if xdistance >= 0:
                            self.direction = 1
                        else:
                            self.direction = -1
                        if self.framecount == 30:
                            self.callminion = 1
                        elif self.framecount == 31:
                            self.callminion = 0
                        elif self.framecount == 200:
                            self.lock = 0
        self.framecount+= 1
        self.index = (self.index + 1) % (len(self.images[self.state]))
        self.image = self.images[self.state][self.index]
        self.mask = pygame.mask.from_surface(self.image)

        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Breath(pygame.sprite.Sprite):
    def __init__(self,pos,direction):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'breath'
        self.index = 0
        self.attack = 30
        self.images = [pygame.image.load('assets/imgs/Sprites/Boss/breath/' +f'breath_{i}.png') for i in range(0, 5)]
        image_surf = pygame.image.load('assets/imgs/Sprites/Boss/breath/' +f'breath_0.png').convert()
        self.image = pygame.Surface((500, 350))
        self.image.blit(image_surf, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        if direction == 1:
            self.direction = 1
            self.rect = self.image.get_rect(topleft = (pos[0]-350, pos[1]-85))
        if direction == -1:
            self.direction = -1
            self.rect = self.image.get_rect(topleft = (pos[0]+40, pos[1]-85))
        self.framecount = 0
    def update(self):
        if self.framecount == 50:
            self.kill()
        self.framecount += 1
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image,(500,350))
        self.index = (self.index+1) % 5
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update_collision(self, battle):
        new = time.time()
        if len(battle) > 0:
            for sprite in battle:
                if (new - sprite.last_hurt > 1.5):
                    sprite.last_hurt = time.time()
                    sprite.hp -= self.attack
                    if sprite.type != 'hero':
                        if sprite.type == 'warlock':
                            sprite.state = 'hurt'
                            sprite.lock = 0
                        elif sprite.direction == 1:
                            sprite.state = 'hurt_left'
                        else:
                            sprite.state = 'hurt_right'
                            sprite.index = 0
                    else:
                        sprite.hp -= self.attack
                        if sprite.hp > 0:
                            pygame.mixer.music.load('assets/sounds/mixkit-human-fighter-pain-scream-2768.wav')
                            pygame.mixer.music.play()
                        sprite.last_hurt = time.time()
                        sprite.index = 0
                        sprite.update_hurt(self)
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Fire(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = {
            'small' :[pygame.image.load('assets/imgs/Sprites/SmallFire/' +f'SmallFire_{i}.png') for i in range(0, 5)],
            'vortex' : [pygame.image.load('assets/imgs/Sprites/Flamevortex/' +f'Flamevortex_{i}.png') for i in range(0, 9)]
        }
        image_surf = pygame.image.load('assets/imgs/Sprites/SmallFire/SmallFire_0.png').convert()
        self.image = pygame.Surface((30, 60))
        self.damage = 15
        self.direction = 0
        self.status = 'small'
        self.type = 'fire'
        self.image.blit(image_surf, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.count = 20

    def update(self):
        if self.count <= 150:
            self.status = 'small'
            self.image = self.images[self.status][self.index]
            self.index = (self.index + 1) % 5
        if self.count > 150:
            self.status = 'vortex'
            self.image = self.images[self.status][self.index]
            self.index = (self.index + 1) % 9
        if self.count > 300:
            self.kill()
        self.count += 4

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.attack = 88
        self.images = [pygame.image.load('assets/imgs/Sprites/Meteor/' + f'MeteorShower_{i}.png') for i in range(0, 16)]
        image_surf = pygame.image.load('assets/imgs/Sprites/Meteor/MeteorShower_0.png').convert()
        image_surf = pygame.transform.scale(image_surf, (120, 60))
        self.image = pygame.Surface((30, 60))
        self.image.blit(image_surf, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=pos)
        self.countframe = 0

    def update(self):
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (120, 60))
        self.index = (self.index+1)%16
        self.countframe += 1
        if self.countframe == 80:
            self.kill()

    def update_collision(self, battle):
        new = time.time()
        if len(battle) > 0:
            for monster in battle:
                if (new - monster.last_hurt > 2.5):
                    if monster.type != 'boss' or monster.state == 'run_idle':
                            monster.last_hurt = time.time()
                            monster.hp -= self.attack
                            if monster.type == 'warlock':
                                monster.state = 'hurt'
                                monster.lock = 1
                                monster.index = -1
                            elif monster.direction == 1 and monster.type == 'skeleton':
                                monster.state = 'hurt_left'
                                monster.lock = 1
                                monster.index = -1
                            elif monster.type == 'skeleton':
                                monster.state = 'hurt_right'
                                monster.lock = 1
                                monster.index = -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Portal(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.images = [pygame.image.load('assets/imgs/Sprites/Portal/' +f'Portal_{i}.png') for i in range(0, 15)]
        image_surf = pygame.image.load('assets/imgs/Sprites/Portal/Portal_0.png').convert()
        self.image = pygame.Surface((30, 60))
        self.image.blit(image_surf, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.lock = 0
        self.status = 'open'

    def update(self):
        if self.status == 'open':
            if self.lock == 0 and self.index != 10:
                self.image = self.images[self.index]
                #self.index += 1
            elif self.lock == 0 and self.index == 10:
                self.index == 4
                self.lock = 1
            elif self.lock == 1:
                if self.index == 11:
                    self.index = 4
        elif self.status == 'close':
            if self.index < 10:
                self.index = 11
            elif self.index == 14:
                self.kill()
        self.image = self.images[self.index]
        self.index += 1

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
        self.type = 'skeleton'
        self.hp = 50
        self.attack = 15
        self.state = 'born'
        self.index = 0
        self.hurt_cd = 0.2
        self.last_hurt = time.time()
        self.cd = 1.2
        self.last = time.time()
        self.image = pygame.Surface((64, 64))
        self.image_surf = pygame.image.load(SKELETON_ASSET + f'SkeletonMage_Blue.png').convert()
        self.image.blit(self.image_surf, (0, 0), (180, 0, 64, 64))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.lock = 1
        self.speed = random.randrange(1, 4)
        self.count = 2
        self.direction = 1
        self.score = 40
        self.image_rects = {
            'idle_left' : [pygame.Rect(0,64,64,64), pygame.Rect(64,64,64,64), pygame.Rect(128,64,64,64),
                           pygame.Rect(192,64,64,64)],
            'idle_right': [pygame.Rect(0, 192, 64, 64), pygame.Rect(64, 192, 64, 64), pygame.Rect(128, 192, 64, 64),
                          pygame.Rect(192, 192, 64, 64)],
            'run_left' : [pygame.Rect(0,320,64,64),pygame.Rect(64,320,64,64),pygame.Rect(128,320,64,64),
                        pygame.Rect(192,320,64,64),pygame.Rect(256,320,64,64),pygame.Rect(320,320,64,64)],
            'run_right': [pygame.Rect(0, 448, 64, 64), pygame.Rect(64, 448, 64, 64), pygame.Rect(128, 448, 64, 64),
                         pygame.Rect(192, 448, 64, 64), pygame.Rect(256, 448, 64, 64), pygame.Rect(320, 448, 64, 64)],
            'attack_left' : [pygame.Rect(0,576,64,64),pygame.Rect(64,576,64,64),pygame.Rect(128,576,64,64),
                        pygame.Rect(192,576,64,64),pygame.Rect(256,576,64,64),pygame.Rect(320,576,64,64),
                        pygame.Rect(384,576,64,64),pygame.Rect(448,576,64,64)],
            'attack_right': [pygame.Rect(0, 704, 64, 64), pygame.Rect(64, 704, 64, 64), pygame.Rect(128, 704, 64, 64),
                             pygame.Rect(192, 704, 64, 64), pygame.Rect(256, 704, 64, 64),
                             pygame.Rect(320, 704, 64, 64),
                             pygame.Rect(384, 704, 64, 64), pygame.Rect(448, 704, 64, 64)],
            'born' : [pygame.Rect(0,1088,64,64),pygame.Rect(64,1088,64,64),pygame.Rect(128,1088,64,64),
                        pygame.Rect(192,1088,64,64),pygame.Rect(256,1088,64,64),pygame.Rect(320,1088,64,64),
                        pygame.Rect(384,1088,64,64),pygame.Rect(448,1088,64,64),pygame.Rect(512,1088,64,64)],
            'hurt_left' : [pygame.Rect(0,1280,64,64),pygame.Rect(64,1280,64,64),pygame.Rect(128,1280,64,64),
                        pygame.Rect(192,1280,64,64),pygame.Rect(256,1280,64,64),pygame.Rect(320,1280,64,64)],
            'hurt_right': [pygame.Rect(0, 1344, 64, 64), pygame.Rect(64, 1344, 64, 64), pygame.Rect(128, 1344, 64, 64),
                           pygame.Rect(192, 1344, 64, 64), pygame.Rect(256, 1344, 64, 64),
                           pygame.Rect(320, 1344, 64, 64)],
            'death_left' : [pygame.Rect(0,1472,64,64),pygame.Rect(64,1472,64,64),pygame.Rect(128,1472,64,64),
                        pygame.Rect(192,1472,64,64),pygame.Rect(256,1472,64,64),pygame.Rect(320,1472,64,64),
                        pygame.Rect(384,1472,64,64)],
            'death_right': [pygame.Rect(0, 1600, 64, 64), pygame.Rect(64, 1600, 64, 64), pygame.Rect(128, 1600, 64, 64),
                      pygame.Rect(192, 1600, 64, 64), pygame.Rect(256, 1600, 64, 64), pygame.Rect(320, 1600, 64, 64),
                      pygame.Rect(384, 1600, 64, 64)]
        }

    def update(self,hero_center_pos,game):
        if self.lock == 1:
            if self.state == 'born' and self.index == 8:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if (self.state == 'death_left' or self.state == 'death_right') and self.index == 6:
                self.kill()
                game.score += self.score
            if self.state == 'hurt_left' and self.index == 5:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if self.state == 'hurt_right' and self.index == 5:
                self.lock = 0
                self.index = 0
                self.state = 'idle_right'
            if self.state == 'attack_left' and self.index == 7:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if self.state == 'attack_right' and self.index == 7:
                self.lock = 0
                self.index = 0
                self.state = 'idle_right'
        if self.lock == 0:
            if self.hp <= 0:
                if self.direction == 1:
                    self.state = 'death_left'
                else:
                    self.state = 'death_right'
                self.lock = 1
                self.index = 0
            if self.state not in ['death_left','death_right','hurt_left','hurt_right','born']:
                x = self.rect.centerx
                y = self.rect.centery
                distance = ((hero_center_pos[0] - x) ** 2 + (hero_center_pos[1] - y) ** 2) ** 0.5
                if distance <= 30 and distance >= 15 and time.time() - self.last > self.cd:
                    self.last = time.time()
                    if self.direction == 1:
                        self.state = 'attack_left'
                    if self.direction == -1:
                        self.state = 'attack_right'
                    self.lock = 1
                    self.index = 0
                if self.state not in ['attack_left','attack_right']:
                    if distance < 350 and distance > 20 and self.count % 2 == 0:
                        if self.direction == 1:
                            self.state = 'run_left'
                        if self.direction == -1:
                            self.state = 'run_right'
                        if hero_center_pos[0] < x:
                            self.direction = 1
                            self.rect.move_ip(-1 * self.speed, 0)
                        if hero_center_pos[0] > x:
                            self.direction = -1
                            self.rect.move_ip(1 * self.speed, 0)
                        if hero_center_pos[1] < y:
                            self.rect.move_ip(0, -1 * self.speed)
                        if hero_center_pos[1] > y:
                            self.rect.move_ip(0, 1 * self.speed)
                    self.count += 1
                    if distance >= 350:
                        if self.direction == 1:
                            self.state = 'idle_left'
                        if self.direction == -1:
                            self.state = 'idle_right'
        self.index = (self.index + 1)%len(self.image_rects[self.state])
        self.mask = pygame.mask.from_surface(self.image)
        self.image.blit(self.image_surf,(0,0),self.image_rects[self.state][self.index])

    def draw(self, surface):

        surface.blit(self.image, self.rect)


class Skeleton_red(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'skeleton'
        self.hp = 80
        self.attack = 15
        self.state = 'born'
        self.index = 0
        self.hurt_cd = 0.2
        self.last_hurt = time.time()
        self.cd = 1.2
        self.last = time.time()
        self.image = pygame.Surface((64, 64))
        self.image_surf = pygame.image.load(SKELETON_ASSET + f'SkeletonMage_Red.png').convert()
        self.image.blit(self.image_surf, (0, 0), (180, 0, 64, 64))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.lock = 1
        self.speed = random.randrange(1, 4)
        self.count = 2
        self.direction = 1
        self.score = 40
        self.image_rects = {
            'idle_left': [pygame.Rect(0, 64, 64, 64), pygame.Rect(64, 64, 64, 64), pygame.Rect(128, 64, 64, 64),
                          pygame.Rect(192, 64, 64, 64)],
            'idle_right': [pygame.Rect(0, 192, 64, 64), pygame.Rect(64, 192, 64, 64), pygame.Rect(128, 192, 64, 64),
                           pygame.Rect(192, 192, 64, 64)],
            'run_left': [pygame.Rect(0, 320, 64, 64), pygame.Rect(64, 320, 64, 64), pygame.Rect(128, 320, 64, 64),
                         pygame.Rect(192, 320, 64, 64), pygame.Rect(256, 320, 64, 64), pygame.Rect(320, 320, 64, 64)],
            'run_right': [pygame.Rect(0, 448, 64, 64), pygame.Rect(64, 448, 64, 64), pygame.Rect(128, 448, 64, 64),
                          pygame.Rect(192, 448, 64, 64), pygame.Rect(256, 448, 64, 64), pygame.Rect(320, 448, 64, 64)],
            'attack_left': [pygame.Rect(0, 832, 64, 64), pygame.Rect(64, 832, 64, 64), pygame.Rect(128, 832, 64, 64),
                            pygame.Rect(192, 832, 64, 64), pygame.Rect(256, 832, 64, 64), pygame.Rect(320, 832, 64, 64),
                            pygame.Rect(384, 832, 64, 64), pygame.Rect(448, 832, 64, 64)],
            'attack_right': [pygame.Rect(0, 960, 64, 64), pygame.Rect(64, 960, 64, 64), pygame.Rect(128, 960, 64, 64),
                             pygame.Rect(192, 960, 64, 64), pygame.Rect(256, 960, 64, 64),
                             pygame.Rect(320, 960, 64, 64),
                             pygame.Rect(384, 960, 64, 64), pygame.Rect(448, 960, 64, 64)],
            'born': [pygame.Rect(0, 1088, 64, 64), pygame.Rect(64, 1088, 64, 64), pygame.Rect(128, 1088, 64, 64),
                     pygame.Rect(192, 1088, 64, 64), pygame.Rect(256, 1088, 64, 64), pygame.Rect(320, 1088, 64, 64),
                     pygame.Rect(384, 1088, 64, 64), pygame.Rect(448, 1088, 64, 64), pygame.Rect(512, 1088, 64, 64)],
            'hurt_left': [pygame.Rect(0, 1280, 64, 64), pygame.Rect(64, 1280, 64, 64), pygame.Rect(128, 1280, 64, 64),
                          pygame.Rect(192, 1280, 64, 64), pygame.Rect(256, 1280, 64, 64),
                          pygame.Rect(320, 1280, 64, 64)],
            'hurt_right': [pygame.Rect(0, 1344, 64, 64), pygame.Rect(64, 1344, 64, 64), pygame.Rect(128, 1344, 64, 64),
                           pygame.Rect(192, 1344, 64, 64), pygame.Rect(256, 1344, 64, 64),
                           pygame.Rect(320, 1344, 64, 64)],
            'death_left': [pygame.Rect(0, 1472, 64, 64), pygame.Rect(64, 1472, 64, 64), pygame.Rect(128, 1472, 64, 64),
                           pygame.Rect(192, 1472, 64, 64), pygame.Rect(256, 1472, 64, 64),
                           pygame.Rect(320, 1472, 64, 64),
                           pygame.Rect(384, 1472, 64, 64)],
            'death_right': [pygame.Rect(0, 1600, 64, 64), pygame.Rect(64, 1600, 64, 64), pygame.Rect(128, 1600, 64, 64),
                            pygame.Rect(192, 1600, 64, 64), pygame.Rect(256, 1600, 64, 64),
                            pygame.Rect(320, 1600, 64, 64),
                            pygame.Rect(384, 1600, 64, 64)]
        }

    def update(self, hero_center_pos, game):
        if self.lock == 1:
            if self.state == 'born' and self.index == 8:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if (self.state == 'death_left' or self.state == 'death_right') and self.index == 6:
                self.kill()
                game.score += self.score
            if self.state == 'hurt_left' and self.index == 5:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if self.state == 'hurt_right' and self.index == 5:
                self.lock = 0
                self.index = 0
                self.state = 'idle_right'
            if self.state == 'attack_left' and self.index == 7:
                self.lock = 0
                self.index = 0
                self.state = 'idle_left'
            if self.state == 'attack_right' and self.index == 7:
                self.lock = 0
                self.index = 0
                self.state = 'idle_right'
        if self.lock == 0:
            if self.hp <= 0:
                if self.direction == 1:
                    self.state = 'death_left'
                else:
                    self.state = 'death_right'
                self.lock = 1
                self.index = 0
            if self.state not in ['death_left', 'death_right', 'hurt_left', 'hurt_right','born']:
                x = self.rect.centerx
                y = self.rect.centery
                distance = ((hero_center_pos[0] - x) ** 2 + (hero_center_pos[1] - y) ** 2) ** 0.5
                if distance <= 30 and distance >= 15 and time.time() - self.last > self.cd:
                    self.last = time.time()
                    if self.direction == 1:
                        self.state = 'attack_left'
                    if self.direction == -1:
                        self.state = 'attack_right'
                    self.lock = 1
                    self.index = 0
                if self.state not in ['attack_left', 'attack_right']:
                    if distance < 350 and distance > 20 and self.count % 2 == 0:
                        if self.direction == 1:
                            self.state = 'run_left'
                        if self.direction == -1:
                            self.state = 'run_right'
                        if hero_center_pos[0] < x:
                            self.direction = 1
                            self.rect.move_ip(-1 * self.speed, 0)
                        if hero_center_pos[0] > x:
                            self.direction = -1
                            self.rect.move_ip(1 * self.speed, 0)
                        if hero_center_pos[1] < y:
                            self.rect.move_ip(0, -1 * self.speed)
                        if hero_center_pos[1] > y:
                            self.rect.move_ip(0, 1 * self.speed)
                    self.count += 1
                    if distance >= 350:
                        if self.direction == 1:
                            self.state = 'idle_left'
                        if self.direction == -1:
                            self.state = 'idle_right'
        self.index = (self.index + 1) % len(self.image_rects[self.state])
        self.mask = pygame.mask.from_surface(self.image)
        self.image.blit(self.image_surf, (0, 0), self.image_rects[self.state][self.index])

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Warlock(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxHp = 40
        self.hp = 40
        self.attack = 10
        self.coolDown = 4
        self.damageCoolDown = 1.5
        self.state = 'idle'
        self.type = 'warlock'
        self.direction = -1
        self.velocity = 3
        self.index = 0
        self.lock = 0
        self.last = time.time()
        self.last_hurt = time.time()
        self.hurt_cd = 0.2
        self.last_hurt = time.time()
        self.images = {
            'idle': [pygame.image.load(WARLOCK_ASSET + f'Idle/Warlock_Idle_{i}.png') for i in range(0, 12)],
            'run': [pygame.image.load(WARLOCK_ASSET + f'Run/Warlock_Run_{i}.png') for i in range(0, 8)],
            'death': [pygame.image.load(WARLOCK_ASSET + f'Death/Warlock_Death_{i}.png') for i in range(0, 13)],
            'attack' : [pygame.image.load(WARLOCK_ASSET + f'Attack/Warlock_Attack_{i}.png') for i in range(0, 13)],
            'spellcast': [pygame.image.load(WARLOCK_ASSET + f'Spellcast/Warlock_Spellcast_{i}.png') for i in range(0, 14)],
            'hurt': [pygame.image.load(WARLOCK_ASSET + f'Hurt/Warlock_Hurt_{i}.png') for i in range(0, 4)],
        }
        image_surf = pygame.image.load(WARLOCK_ASSET + 'idle/Warlock_Idle_0.png').convert()
        image_surf = pygame.transform.scale(image_surf, (120, 96))
        self.image = pygame.Surface((100,80))
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.fire = 0
        self.cast = 0
        self.score = 80

    def update(self,hero_center_pos,game):
        new = time.time()
        if self.lock == 1:
            if self.state == 'death' and self.index == 12:
                self.kill()
                game.score += self.score
            if self.state == 'hurt' and self.index == 3:
                self.lock = 0
                self.index = 0
                self.state = 'idle'
            if self.state == 'spellcast' and self.index == 13:
                self.lock = 0
                self.index = 0
                self.state = 'idle'
            if self.state == 'spellcast' and self.index == 1:
                self.cast = 0
            if self.state == 'attack' and self.index == 12:
                self.lock = 0
                self.index = 0
                self.state = 'idle'
            if self.state == 'attack' and self.index == 1:
                self.fire = 0
        if self.lock == 0:
            if self.hp <= 0:
                self.state = 'death'
                self.index = 0
                self.lock = 1
            if self.state not in ['death','hurt']:
                x = self.rect.centerx
                y = self.rect.centery
                distance = ((hero_center_pos[0] - x) ** 2 + (hero_center_pos[1] - y) ** 2) ** 0.5
                if hero_center_pos[0] < x:
                    self.direction = -1
                else:
                    self.direction = 1
                if (distance <= 150 ) and (new - self.last > self.coolDown):
                    self.state = 'spellcast'
                    self.lock = 1
                    self.cast = 1
                    self.index = 0
                    self.last = time.time()
                if self.state != 'spellcast' and (self.rect.centery > hero_center_pos[1] - 30 and self.rect.centery < hero_center_pos[1] + 30) and (new - self.last > self.coolDown):
                    self.state = 'attack'
                    self.lock = 1
                    self.fire = 1
                    self.index = 0
                    self.last = time.time()
                if self.state not in ['spellcast','attack']:
                    if distance < 500 and distance > 150:
                        self.state = 'run'
                        if hero_center_pos[0] < x:
                            self.rect.move_ip(-1, 0)
                        if hero_center_pos[0] > x:
                            self.rect.move_ip(1, 0)
                        if hero_center_pos[1] < y:
                            self.rect.move_ip(0, -1)
                        if hero_center_pos[1] > y:
                            self.rect.move_ip(0, 1)
                    elif distance < 120:
                        self.state = 'run'
                        stuck = 1
                        if hero_center_pos[0] < x and x < 960:
                            self.direction = 1
                            self.rect.move_ip(1, 0)
                            stuck = 0
                        if hero_center_pos[0] > x and x > 40:
                            self.direction = -1
                            self.rect.move_ip(-1, 0)
                            stuck = 0
                        if hero_center_pos[1] < y and y < 700:
                            self.rect.move_ip(0, 1)
                            stuck = 0
                        if hero_center_pos[1] > y and y > 350:
                            self.rect.move_ip(0, -1)
                            stuck = 0
                        if stuck:
                            self.state = 'idle'
                    else:
                        self.state = 'idle'
        self.index = (self.index + 1) % len(self.images[self.state])
        self.image = self.images[self.state][self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (120, 96))
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Warlock_bullet(pygame.sprite.Sprite):
    def __init__(self,pos,direction):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.type = 'bullet'
        self.damage = 20
        self.direction = direction
        self.images = [pygame.image.load('assets/imgs/Sprites/LightningBolt/' +f'LightningBolt_{i}.png') for i in range(0, 3)]
        image_surf = pygame.image.load('assets/imgs/Sprites/LightningBolt/LightningBolt_0.png').convert()
        self.image = pygame.Surface((30, 40))
        self.image.blit(image_surf, (0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        if direction == 1:
            self.rect = self.image.get_rect(topleft=pos)
        if direction == -1:
            self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if self.direction == 1:
            if self.rect.x < -40:
                self.kill()
            self.rect.move_ip(-8,0)
        if self.direction == -1:
            if self.rect.x > 800:
                self.kill()
            self.rect.move_ip(8,0)
        self.index = (self.index + 1) % (len(self.images))
        self.image = self.images[self.index]
        if self.direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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
        self.fontobj = setup_fonts(36)
        self.rect = pygame.Rect((0,0),(1034, 778))
        self.rect.center = (517, 389)
        self.img2 = pygame.image.load('assets/imgs/final_scene.jpg').convert()
        self.image_surf = pygame.image.load('assets/imgs/pop_up.jpg').convert()
        self.image_surf = pygame. transform. scale(self.image_surf, (1034, 778))

    def pop_up(self, texts):
        row = len(texts)
        self.surface.blit(self.image_surf, self.rect)
        for i in range(0, row):
            text = texts[i]
            text_surface = self.fontobj.render(text, True, (255, 255, 255))
            text_center = (517, 150 + (389 / (row + 1)) * (i+1))
            text_rect = text_surface.get_rect(center = text_center)
            self.surface.blit(text_surface, text_rect)
        self.status = 'pop_up'

    def update(self, control):
        if control['pop'] == True and self.status != 'pop_up':
            self.status = 'pop_up'
            return 'pause'
        elif control['pop'] == True and self.status == 'pop_up':
            self.status = 'close'
            return 'running'

class Boss_icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = pygame.Surface((160,144))
        image_surf = pygame.image.load(BOSS_ASSET + '/idle/demon-idle_0.png').convert()
        self.image.blit(image_surf,(0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)
        self.state = 'idle'
        self.images = {
            'idle': [pygame.image.load(BOSS_ASSET + f'idle/demon-idle_{i+1}.png') for i in range(0, 5)],
            'attack': [pygame.image.load(BOSS_ASSET + f'attack/demon-attack_{i+1}.png') for i in range(0, 7)],
            'nightmare-run': [pygame.image.load(BOSS_ASSET + f'nightmare-run/nightmare-run_{i+1}.png') for i in range(0, 3)],
            'nightmare-idle': [pygame.image.load(BOSS_ASSET + f'nightmare-idle/nightmare-idle_{i+1}.png') for i in range(0, 3)],
        }
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        self.index = (self.index + 1) % (len(self.images[self.state]))
        self.image = self.images[self.state][self.index]
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameManager():
    def __init__(self):
        self.score = 0
        self.difficulty = 1
        self.fontobj = setup_fonts(24)
        self.state = 'running'
        self.next = True
        self.window_size_x = 1034
        self.window_size_y = 778
        self.magic = False
        self.revive_number = 0
        self.maze_time = 0
        self.mix1 = pygame.mixer.Sound('assets/sounds/background.wav')
        self.mix2 = pygame.mixer.Sound('assets/sounds/epic_battle_music_1-6275.wav')
        self.mix3 = pygame.mixer.Sound('assets/sounds/Maze.wav')
        self.mix4 = pygame.mixer.Sound('assets/sounds/Boss.wav')
        self.mix5 = pygame.mixer.Sound('assets/sounds/End.wav')
        self.background_channel = pygame.mixer.Channel(0)
        self.battle_channel = pygame.mixer.Channel(1)
        self.background_channel.play(self.mix1, -1)

    def draw(self, surface):
         text = self.fontobj.render("Score: "+str(self.score), True, (255, 255, 255))
         surface.blit(text,(880,50))
         text = self.fontobj.render('Press P to Pause the Game!', True, (255, 255, 255))
         surface.blit(text, (720, 20))
