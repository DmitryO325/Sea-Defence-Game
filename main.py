import random

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


class Ship(pygame.sprite.Sprite):  # класс корабля (общий для игрока и противников)
    def __init__(self, group):
        super().__init__(group)
        self.armor = 0  # количество брони
        self.speed = 0  # скорость корабля

    def torpedo_shot(self, coords, group):  # функция запуска торпеды
        if self.rect.x + self.rect.w * 0.5 > coords[0]:
            Torpedo(round(self.rect.x + 0.1 * self.rect.w), round(0.95 * self.rect.y), coords, group)
        else:
            Torpedo(round(self.rect.x + 0.8 * self.rect.w), round(0.95 * self.rect.y), coords, group)

    def get_damage(self, damage):  # функция получения урона
        self.armor -= damage


class Player(Ship):  # класс игрока
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('Player.png'), (width * 0.3, height * 0.3))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = round(0.35 * width), round(0.72 * height)
        self.left = False  # плывем влево
        self.right = False  # плывем вправо

    def gun_shot(self):  # функция выстрела из пушки
        pass

    def update(self, *args):  # изменение местоположения
        if self.right:
            self.rect.x += 4
            if self.rect.x + self.rect.w > width:
                self.rect.x = width - self.rect.w
        if self.left:
            self.rect.x -= 4
            if self.rect.x < 0:
                self.rect.x = 0

        if self.armor <= 0:
            pass  # заканчиваем игру


class Enemy(Ship):  # класс врага
    params = {'Канонерка': (), 'Крейсер': (),
              'Линкор': (), 'Эсминец': ()}
    # каждому виду корабля соответствуют свои характеристики: armor, speed, направление (вправо плывет или влево)

    def __init__(self, group, ship_type):
        super().__init__(group)
        self.info = self.params[ship_type]
        # появляется за экраном
        # выпускает торпеду с периодом ок. 3-6 секунд
        # каждому типу соответствует своя картинка (см. Images)

    def update(self):  # перемещение корабля
        pass


class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coords: tuple, group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.x1, self.y1 = point_coords
        self.delta_y = -0.002 * height
        self.delta_x = (self.x1 - self.x) / (self.y - self.y1) * 0.002 * height
        self.image = pygame.transform.scale(load_image('torpedo.png'), (round(width * 0.015), round(height * 0.12)))
        self.rect = self.image.get_rect()
        self.rotate()
        self.rect.x = self.x
        self.rect.y = self.y

    def rotate(self):
        if self.x != self.x1:
            angle = round(math.degrees(math.atan((self.y - self.y1) / (self.x1 - self.x))))
            if angle < 0:
                self.image = pygame.transform.rotate(self.image, abs(angle + 90))
            else:
                self.image = pygame.transform.rotate(self.image, angle + 270)

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                sprite.get_damage(80)
        else:
            if self.y < 0.25 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > height:
                self.kill()
            self.x += self.delta_x
            self.y += self.delta_y
            self.rect.x = self.x
            self.rect.y = self.y


class Battlefield:  # игровое поле
    def __init__(self, difficulty=None, conditions=None):
        # чем выше сложность, тем выше будет скорость всего происходящего
        # погодные условия потом
        self.bg = pygame.transform.scale(load_image('img.png'), screen.get_size())  # фоновое изображение
        self.ship_group = pygame.sprite.Group()
        self.torpedo_group = pygame.sprite.Group()  # группы спрайтов
        self.shoal_group = pygame.sprite.Group()
        self.player = Player(self.ship_group)  # игрок
        running = True
        self.random_event = pygame.USEREVENT + 1  # событие генерации событий
        pygame.time.set_timer(self.random_event, random.randint(1, 3) * 1000, 1)  # первое событие через 1-3 с
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
                    if event.key == pygame.K_LEFT:  # для перемещения игрока по сторонам
                        self.player.left = False
                    if event.key == pygame.K_RIGHT:
                        self.player.right = False
                if event.type == pygame.MOUSEBUTTONDOWN:  # ПКМ - пуск торпеды
                    if event.button == 3:
                        if event.pos[1] < height * 0.6:  # но вбок нельзя
                            self.player.torpedo_shot(event.pos, self.torpedo_group)
                if event.type == self.random_event:  # генерация случайного события
                    generated_event = random.choice(['мель', 'корабль'])  # сделать более вероятным то или иное событие
                    if generated_event == 'мель':
                        self.spawn_shoal()  # спавнит мель
                    else:
                        self.spawn_enemy()  # спавнит мель корабль врага
                    pygame.time.set_timer(self.random_event, random.randint(7, 11) * 1000, 1)  # новое событие 7-11 с
            pygame.display.flip()
            screen.blit(self.bg, (0, 0))
            self.ship_group.update()
            self.ship_group.draw(screen)
            self.torpedo_group.update(self.ship_group)  # обновление групп спрайтов
            self.torpedo_group.draw(screen)
            self.shoal_group.update(self.player)
            self.shoal_group.draw(screen)

    def spawn_shoal(self):  # функция спавна мели
        Shoal((random.random() * width, 0.3 * height),
              (random.uniform(0.05, 0.3) * width, random.uniform(0.05, 0.2) * height), self.shoal_group)

    def spawn_enemy(self):  # функция спавна корабля
        Enemy(self.ship_group,
              ship_type=random.choice(
                  ['Канонерка', 'Эсминец', 'Линкор', 'Крейсер']))


class Shoal(pygame.sprite.Sprite):  # класс мели
    def __init__(self, coords: tuple, size: tuple, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('shoal.png'), size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords

    def update(self, player):  # надо сделать так, чтобы из точки вырастал остров
        if pygame.sprite.collide_mask(self, player):  # проверка удара
            player.get_damage(40)
            self.kill()
            print('Получено 40 урона')
        else:
            self.rect.y += height * 0.001  # спуск вниз
            if self.rect.y >= 0.96 * height:  # выход за границу
                self.kill()


if __name__ == '__main__':
    pygame.init()
    FPS = 100
    full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    clock.tick(FPS)
    Battlefield()
