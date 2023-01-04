import pygame
import pygame_widgets
import sys
import os
import math


def delete_widgets():
    pygame_widgets.WidgetHandler._widgets = []


def load_image(name, colorkey=None):
    fullname = os.path.join('Images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Ship(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.armor = 0
        self.speed = 0

    def torpedo_shot(self, coords, group):
        Torpedo(round(self.rect.x + 0.5 * self.rect.w), round(self.rect.y), coords, group)


class Player(Ship):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('Player.png'), (width * 0.3, height * 0.3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = round(0.35 * width), round(0.72 * height)
        self.left = False
        self.right = False

    def gun_shot(self):
        pass

    def update(self, *args):
        if self.right:
            self.rect.x += 4
            if self.rect.x + self.rect.w > width:
                self.rect.x = width - self.rect.w
        if self.left:
            self.rect.x -= 4
            if self.rect.x < 0:
                self.rect.x = 0


class Enemy(Ship):
    def __init__(self, group, ship_type=None):
        super().__init__(group)


class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coords: tuple, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.x1, self.y1 = point_coords
        self.image = pygame.transform.scale(load_image('torpedo.png'), (round(width * 0.03), round(height * 0.1)))
        self.rect = self.image.get_rect()
        self.rotate()
        self.rect.x = self.x
        self.rect.y = self.y

    def rotate(self):
        angle = round(math.degrees(math.atan((self.y - self.y1) / (self.x1 - self.x))))
        if angle < 0:
            self.image = pygame.transform.rotate(self.image, abs(angle + 90))
        else:
            self.image = pygame.transform.rotate(self.image, angle + 270)

    def move(self):
        pass


class Battlefield:
    def __init__(self, difficulty=None, conditions=None):
        self.bg = pygame.transform.scale(load_image('img.png'), screen.get_size())
        self.player_group = pygame.sprite.Group()
        self.torpedo_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.shoal_group = pygame.sprite.Group()
        self.player = Player(self.player_group)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.left = True
                    if event.key == pygame.K_RIGHT:
                        self.player.right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.left = False
                    if event.key == pygame.K_RIGHT:
                        self.player.right = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.player.torpedo_shot(event.pos, self.torpedo_group)
            pygame.display.flip()
            screen.blit(self.bg, (0, 0))
            self.player_group.update()
            self.player_group.draw(screen)
            self.torpedo_group.update()
            self.torpedo_group.draw(screen)

    def spawn_shoal(self):
        pass


class Shoal(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, size: tuple, group):
        super().__init__(group)
        self.size = self.width, self.height = size
        self.coords = self.x, self.y = coords


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    print(width, height)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    clock.tick(FPS)
    Battlefield()
