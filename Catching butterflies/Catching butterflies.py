import os
import random
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def game_time():
    global startscreentime
    gametime = pygame.time.get_ticks() - startscreentime
    gametime = gametime // 1000
    minutes = str(gametime // 60)
    seconds = str(gametime % 60)
    if len(seconds) == 1:
        seconds = '0' + seconds
    return minutes + ':' + seconds


def terminate():
    pygame.quit()
    sys.exit()


def goose_chooser():
    intro_text = ["Выбери бабочку"]
    fon = pygame.transform.scale(load_image('поле4.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    butter_c = pygame.sprite.Group()
    global butterfie
    global clock
    bats = Butter(butter_c, 'bats.png')
    bat3 = Butter(butter_c, 'bat3.png')
    bat4 = Butter(butter_c, 'bats4.png')
    bat5 = Butter(butter_c, 'bat5.png')
    bat = Butter(butter_c, 'bat.png')
    bat2 = Butter(butter_c, 'bat2.png')
    bats.rect.topleft = (100, 200)
    bat3.rect.topleft = (600, 200)
    bat4.rect.topleft = (100, 400)
    bat5.rect.topleft = (600, 400)
    bat.rect.topleft = (350, 400)
    bat2.rect.topleft = (350, 200)

    chosed = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for but in butter_c:
                    chosed, butterfie = but.chosen(event.pos)
                    if chosed:
                        return
        clock.tick(FPS)
        butter_c.draw(screen)
        pygame.display.flip()


def teaser_screen():
    intro_text = [
        "Добро пожаловать в Catching Butterflies",
        "Здесь нужно ловить бабочек", " ",
        "Для продолжения кликни мышью!"]

    fon = pygame.transform.scale(load_image('вид.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 33)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Правила игры:", " ",
                  "Кликай сачком по бабочке и набирай очки.", " ",
                  "Через каждые 10 попаданий", "ты выходишь на новый уровень,",
                  "и бабочка ускоряется.",
                  " ", "Для продолжения кликни мышью"]

    fon = pygame.transform.scale(load_image('цветы1.jpg'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 18)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_goal():
    pygame.mouse.set_visible(True)
    global count
    global background
    global achieved
    achieved.append(count)
    intro_text = ["Ты поймал бабочку " + str(count) + ' раз!',
                  "Продолжить игру?"]

    fon = pygame.transform.scale(load_image(background), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 33)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect((150, 450), (100, 50)).collidepoint(event.pos):
                    return
                elif pygame.Rect((550, 450), (100, 50)).collidepoint(event.pos):
                    terminate()
        pygame.draw.rect(screen, (0, 255, 0), (150, 450, 100, 50))
        pygame.draw.rect(screen, (255, 0, 0), (550, 450, 100, 50))
        yes = font.render('Да!', 1, pygame.Color('black'))
        no = font.render('Нет', 1, pygame.Color('black'))
        screen.blit(yes, (175, 455, 100, 50))
        screen.blit(no, (570, 455, 100, 50))
        pygame.display.flip()
        clock.tick(FPS)


class Butter(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.image = load_image(image)
        self.image_file = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def caught(self, coords):
        global count
        global score
        global levelup
        global background
        global backgrounds
        if self.rect.collidepoint(coords):
            count += 1
            if count % 10 != 0:
                score.play()
            else:
                levelup.play()
                background = random.choice(backgrounds)

    def chosen(self, coords):
        if self.rect.collidepoint(coords):
            return True, self.image_file
        else:
            return False, 'поле1.jpg'


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('cursor.png')
        self.rect = self.image.get_rect()

    def movement(self, coords):
        self.rect.topleft = coords


global bat2
butterfie = 'bat.png'
backgrounds = ['Grass.png', 'Sand.png', 'Sky.png', 'Beach.png', 'Village.png',
               'Flowers.png', 'Land.png', 'цветы1.jpg', 'вид.jpg', 'поле4.jpg']
background = 'поле4.jpg'
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
goose_move = 1
new_coords = 2
honking = 3
count = 0
level = 1
new_x = 0
new_y = 0
FPS = 50
clock = pygame.time.Clock()
achieved = []
pygame.time.set_timer(goose_move, 10)
pygame.time.set_timer(new_coords, 500)
pygame.time.set_timer(honking, 10000)
score = pygame.mixer.Sound(os.path.join('data', 'score.wav'))
levelup = pygame.mixer.Sound(os.path.join('data', 'LevelUp.wav'))
pygame.mixer.music.load(os.path.join('data', 'Music.mp3'))
teaser_screen()
start_screen()
goose_chooser()
all_sprites = pygame.sprite.Group()
goose = Butter(all_sprites, butterfie)
pygame.mouse.set_visible(False)
cursor = Cursor(all_sprites)
startscreentime = pygame.time.get_ticks()
pygame.mixer.music.play(-1)
running = True
while running:
    pygame.mouse.set_visible(False)
    for event in pygame.event.get():
        if event.type == goose_move:
            if new_x > goose.rect.x and new_y > goose.rect.y:
                goose.rect.x += level
                goose.rect.y += level
            elif new_x > goose.rect.x and new_y < goose.rect.y:
                goose.rect.x += level
                goose.rect.y -= level
            elif new_x < goose.rect.x and new_y > goose.rect.y:
                goose.rect.x -= level
                goose.rect.y += level
            elif new_x < goose.rect.x and new_y < goose.rect.y:
                goose.rect.x -= level
                goose.rect.y -= level
            else:
                new_x = random.randint(-100, 800)
                new_y = random.randint(-100, 600)
        elif event.type == new_coords:
            new_x = random.randint(-100, 800)
            new_y = random.randint(-100, 600)
        elif event.type == pygame.MOUSEMOTION:
            cursor.movement(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            goose.caught(event.pos)
        elif event.type == pygame.QUIT:
            running = False
            terminate()

    intro_text = ['Попаданий: ' + str(count), 'Время: ' + game_time(),
                  'Уровень: ' + str(level)]
    fon = pygame.transform.scale(load_image(background), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(os.path.join('data', 'PTMono.ttc'), 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    level = count // 10 + 1
    if count % 100 == 0 and count != 0 and count not in achieved:
        end_goal()
    clock.tick(FPS)
    all_sprites.draw(screen)
    pygame.display.flip()
