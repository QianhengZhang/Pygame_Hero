import pygame

class Knight(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((100,120))
        image_surf = pygame.image.load('assets/imgs/knight/png/Idle.png').convert()
        self.image.blit(image_surf, (0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, click, left, right):
        if click:
            self.rect.center = click
        if left:
            self.rect.x -= 15
        if right:
            self.rect.x += 15

    def draw(self, surface):
        surface.blit(self.image, self.rect)
