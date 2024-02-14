
import math
import pygame, sys
from random import randint, choice
from player import Player
from obstacle import Obstacle

class Background():
    def __init__(self, type):
        if type == 'sky':
            self.image = pygame.image.load('./graphics/Sky.png').convert_alpha()
            self.y_pos = 0
        else:
            self.image = pygame.image.load('./graphics/ground.png').convert_alpha()
            self.y_pos = 300

        self.image_width = int(self.image.get_width())
        self.scroll = 0
        self.tiles = math.ceil(800/self.image_width) + 1

    def infinite_scrolling(self):
        for i in range(0, self.tiles):
            screen.blit(self.image, (i * self.image_width + self.scroll, self.y_pos))
        
        if type == 'sky':
            self.scroll -= 1
        else:
            self.scroll -= 4

        if abs(self.scroll) > self.image_width:
            self.scroll = 0

    def update(self):
        self.infinite_scrolling()


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    current_time_seconds = int(current_time/1000)
    score_surf = test_font.render(str(current_time_seconds), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center= (text_render_width, text_render_height))
    screen.blit(score_surf, score_rect)
    return current_time_seconds


def display_game_name():
    name_text_surf = test_font.render(f'My Game', False, (64, 64, 64))
    name_text_surf = pygame.transform.scale2x(name_text_surf)
    name_text_rect = name_text_surf.get_rect(center= (text_render_width, text_render_height))
    return screen.blit(name_text_surf, name_text_rect)


def display_final_score(value):
    current_time_seconds = value
    score_surf = test_font.render(f'High Score:{str(current_time_seconds)}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center= (text_render_width, text_render_height + 50))
    return screen.blit(score_surf, score_rect)


def display_instructions():
    instr_text_surf = test_font.render(f"press 'SPACE' to jump or start", False, (64, 64, 64))
    instr_text_rect = instr_text_surf.get_rect(center=(text_render_width, text_render_height+270))
    return screen.blit(instr_text_surf, instr_text_rect)


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


pygame.init()

window_width = 800
window_height = 400

font_size = 50

text_render_width = window_width/2
text_render_height = 50


#Dimensões da Janela
screen = pygame.display.set_mode((window_width, window_height))

#Muda o nome do "TITLE" da Janela criada
pygame.display.set_caption('Runner')

#Contagem do Frame Rate
clock = pygame.time.Clock()

#Criando uma fonte para texto
test_font = pygame.font.Font('./font/Pixeltype.ttf', font_size)

game_active = False
start_time = 0
score = 0

bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Carregando imagem
sky_background = Background(type='sky')
ground_background = Background(type='ground')

#Intro Screen
player_stand_surface = pygame.image.load('./graphics/Player/player_stand.png').convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface, 0, 1.25)
player_stand_rect = player_stand_surface.get_rect(center=(400, 200))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            """if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint((event.pos)) and player_rect.bottom == 300:
                    player_grav = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_grav = -20"""
            if event.type == obstacle_timer:
                if randint(0, 2):
                    #choice ajuda na aparição escolhida dos sprites nesse caso como tem mais snails na lista, tem mais chance de aparecer
                    obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = pygame.time.get_ticks()

    if game_active:
        screen.fill((94, 129, 162))

        sky_background.update()
        ground_background.update()

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surface, player_stand_rect)

        display_game_name()
        display_final_score(score)
        display_instructions()

    pygame.display.update()
    clock.tick(60)
