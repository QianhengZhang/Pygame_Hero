import pygame
import time

HERO_ASSET = 'assets/imgs/Sprites/HeroKnight/'
Warlock_ASSET = 'assets/imgs/Sprites/Warlock/'

class Hero(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.maxHp = 120
        self.hp = 120
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
            'hurt': [pygame.image.load(HERO_ASSET + f'Hurt/HeroKnight_Hurt_{i+1}.png') for i in range(0, 2)],
            'block' : [pygame.image.load(HERO_ASSET + f'BlockIdle/HeroKnight_Block Idle_{i+1}.png') for i in range(0, 7)]
        }

        image_surf = pygame.image.load(HERO_ASSET + 'idle/HeroKnight_Idle_0.png').convert()
        self.image = pygame.Surface((100,55))
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, controls):
        if self.hp <= 0:
            self.kill()

        new = time.time()
        if controls['attack'] and (new-self.last > self.coolDown):
            if controls['block']:
                self.status = 'attack2'
            elif self.status == 'run':
                self.status = 'attack3'
            else:
                self.status = 'attack'
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
        elif controls['block']:
            self.status = 'block'
            self.index = 0
        else:
            self.status = 'idle'
        self.index = (self.index + 1) % len(self.images[self.status])
        self.image = self.images[self.status][self.index]
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update_collisiton(self, battle):
        status = ['attack', 'attack1', 'attack2']
        new = time.time()
        if len(battle) > 0:
            if self.status in status:
                print('attack')
                for monster in battle:
                    monster.hp -= self.attack
            else:
                for monster in battle:
                    if new - self.lasthurt > self.damageCoolDown:
                        self.hp -= monster.attack
                        time.sleep(0.25)
                        self.rect.x -= 25
                        self.lasthurt = time.time()

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
