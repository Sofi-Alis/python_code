import pygame
from random import randint


class Enemy(pygame.sprite.Sprite):               #класс врага
    def __init__(self, type):
        super().__init__()

        if type == 'jinn':
            jinn_1 = pygame.image.load('graphics/enemy/jinn/1.png').convert_alpha()
            jinn_2 = pygame.image.load('graphics/enemy/jinn/2.png').convert_alpha()
            self.frames = [jinn_1, jinn_2]
            y_pos = 250
        else:
            lizard_1 = pygame.image.load('graphics/enemy/lizard/1.png').convert_alpha()
            lizard_2 = pygame.image.load('graphics/enemy/lizard/2.png').convert_alpha()
            self.frames = [lizard_1, lizard_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):                                  #анимация спрайта
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):                                           #обновление
        self.animation_state()
        self.rect.x -= 6
        self.destroy()                                          #столкновение с врагом

    def destroy(self):                                          #столкновение с врагом игрок умирает
        if self.rect.x <= -100:
            self.kill()
