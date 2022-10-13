import pygame


class Person(pygame.sprite.Sprite):                               #класс игрока
    def __init__(self):
        super().__init__()

        person_idle_1 = pygame.image.load('graphics/player/run/1.png').convert_alpha()
        person_idle_2 = pygame.image.load('graphics/player/run/2.png').convert_alpha()

        self.person_idle = [person_idle_1, person_idle_2]
        self.person_index = 0
        self.person_jump = pygame.image.load('graphics/player/jump/2.png').convert_alpha()

        self.image = self.person_idle[self.person_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')     #звук при прыжке
        self.jump_sound.set_volume(0.5)                            #гроскость звука

    def person_input(self):                                        #управление над персонажом
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -22                                     #высота прыжка
            self.jump_sound.play()                                 #звук при прыжке

    def apply_gravity(self):                                       #гравитация
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):                                    #анимация спрайта
        if self.rect.bottom < 300:
            self.image = self.person_jump
        else:
            self.person_index += 0.1
            if self.person_index >= len(self.person_idle):
                self.person_index = 0
            self.image = self.person_idle[int(self.person_index)]

    def update(self):                                             #обновление
        self.person_input()
        self.apply_gravity()
        self.animation_state()
