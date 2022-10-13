import pygame                          #библиотека пайгейм
from sys import exit
from random import choice
from person import Person
from enemy import Enemy


#Инициализация пайгейма
pygame.init()

SCREEN_WIDTH = 800                                                         #ширина
SCREEN_HEIGTH = 400                                                        #высота
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))            #размер дисплея


pygame.display.set_caption('Running World Game')                #названия дисплея
icon = pygame.image.load('graphics/ic.png')                     #иконка дисплея
pygame.display.set_icon(icon)                                   #загрузка иконки на дисплей

#Загрузка фона
background = pygame.image.load('graphics/bg.png')
ground_surface = pygame.image.load('graphics/tile.png').convert()

clock = pygame.time.Clock()                                     #обьект, который помогает отслеживать время
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)          #загрузка шрифта
game_active = False                                             #игра не активна
start_time = 0                                                  #начало времени игры по умолчании ноль
score = 0                                                       #очки по умолчании ноль
bg_music = pygame.mixer.Sound('audio/_Majesty_ _ Electro-House Music for Your Projects.mp3')
bg_music.play(loops=-1)



def display_score():                                                             #метод счета очков
    current_time = int(pygame.time.get_ticks() / 1000) - start_time                   #счет времени
    score_surf = test_font.render(f'Score: {current_time}', False, (255, 255, 255))   #надпись и его цвет
    score_rect = score_surf.get_rect(center=(90, 370))                                #положение надписи
    screen.blit(score_surf, score_rect)                                               #вывод надписи
    return current_time


def obstacle_movement(enemy_list):                           #метод препятствий
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5

            if enemy_rect.bottom == 300:
                screen.blit(lizard_surf, enemy_rect)
            else:
                screen.blit(jinn_surf, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]

        return enemy_list
    else:
        return []


def collisions(person, enemy):                                 #коллизия игрока и врага
    if enemy:
        for enemy_rect in enemy:
            if person.colliderect(enemy_rect):
                return False
    return True


def collision_sprite():                                        #коллизия спрайта
    if pygame.sprite.spritecollide(person.sprite, enemy_group, False):
        enemy_group.empty()
        return False
    else:
        return True


def person_animation():                                         #анимация игрока
    global person_surf, person_index

    if person_rect.bottom < 300:
        person_surf = person_jump
    else:
        person_index += 0.1
        if person_index >= len(person_idle):
            person_index = 0
        person_surf = person_idle[int(person_index)]


#Группы
person = pygame.sprite.GroupSingle()
person.add(Person())

enemy_group = pygame.sprite.Group()

#Враг лизь
lizard_frame_1 = pygame.image.load('graphics/enemy/lizard/1.png').convert_alpha()
lizard_frame_2 = pygame.image.load('graphics/enemy/lizard/1.png').convert_alpha()
lizard_frames = [lizard_frame_1, lizard_frame_2]
lizard_frame_index = 0
lizard_surf = lizard_frames[lizard_frame_index]

#Враг джин
jinn_frame1 = pygame.image.load('graphics/enemy/jinn/1.png').convert_alpha()
jinn_frame2 = pygame.image.load('graphics/enemy/jinn/2.png').convert_alpha()
jinn_frames = [jinn_frame1, jinn_frame2]
jinn_frame_index = 0
jinn_surf = jinn_frames[jinn_frame_index]

enemy_rect_list = []

#Загрузка игрока
person_idle_1 = pygame.image.load('graphics/player/run/1.png').convert_alpha()
person_idle_2 = pygame.image.load('graphics/player/run/2.png').convert_alpha()
person_idle = [person_idle_1, person_idle_2]
person_index = 0
person_jump = pygame.image.load('graphics/player/jump/2.png').convert_alpha()

person_surf = person_idle[person_index]
person_rect = person_surf.get_rect(midbottom=(80, 300))
person_gravity = 0

#Начальная окно с сообщением (МЕНЮ)
person_stand = pygame.image.load('graphics/player/3.png').convert_alpha()      #загрузка персонажа для начальной игры
person_stand = pygame.transform.rotozoom(person_stand, 0, 2)
person_stand_rect = person_stand.get_rect(center=(400, 200))                              #расположено по центру

game_name = test_font.render('Running World', False, (202, 212, 230))          #название игры и цвет шрифта
game_name_rect = game_name.get_rect(center=(400, 80))                          #название по центру

game_message = test_font.render('PLAY - "Enter"', False, (223, 142, 153))                #сообщением с надписью и цветом
game_message_rect = game_message.get_rect(center=(400, 330))                   #сообщение расположено по центру

#Время
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

lizard_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(lizard_animation_timer, 500)

jinn_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(jinn_animation_timer, 200)


#Цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        #выход из игры
            pygame.quit()
            exit()

        if game_active:                      #если игра активирована

            if event.type == pygame.KEYDOWN:                                             #позволяет прыгать игроку
                if event.key == pygame.K_SPACE and person_rect.bottom >= 300:
                    person_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:          #активация игры с помощи клавиши Enter
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:                       #если игра активирована
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['jinn', 'lizard', 'jinn', 'lizard'])))       #группа врагов рандом

            if event.type == lizard_animation_timer:
                if lizard_frame_index == 0:
                    lizard_frame_index = 1
                else:
                    lizard_frame_index = 0
                lizard_surf = lizard_frames[lizard_frame_index]

            if event.type == jinn_animation_timer:
                if jinn_frame_index == 0:
                    jinn_frame_index = 1
                else:
                    jinn_frame_index = 0
                jinn_surf = jinn_frames[jinn_frame_index]

    if game_active:                                                       #если игра активирована
        screen.blit(background, (0, 0))                                   #вывод неба на окно
        screen.blit(ground_surface, (0, 300))                             #вывод земли на окно

        score = display_score()                                           #вывод надписи "очко"

        person.draw(screen)                                               #нарисование игрока
        person.update()                                                   #обновление игрока

        enemy_group.draw(screen)                                          #нарисование врага
        enemy_group.update()                                              #обновление врага

        game_active = collision_sprite()                                  #коллизия



    else:
        screen.fill((81, 126, 147))                                   #вывод цвета окна
        screen.blit(person_stand, person_stand_rect)                  #вывод игрока
        enemy_rect_list.clear()                                       #очищает врага
        person_rect.midbottom = (80, 300)                             #расположение игрока
        person_gravity = 0                                            #гравитация

        #Итоговое окно со счетами пройденного времени
        score_message = test_font.render(f'Collected points: {score}', False, (255, 255, 255))   #шрифт и цвет сообщение
        score_message_rect = score_message.get_rect(center=(400, 330))                           #положение сообщение
        screen.blit(game_name, game_name_rect)                                                   #вывод сообщение на окно

        if score == 0:                                                #если очко равно нулю
            screen.blit(game_message, game_message_rect)              #то выводит начала игры
        else:
            screen.blit(score_message, score_message_rect)            #если не равно нулю, то показывает набранное очко




    pygame.display.update()                         #обновление окна
    clock.tick(60)                                  #FPS
