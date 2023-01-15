import pygame
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.progressbar import ProgressBar
import pygame_widgets
import sqlite3
import sys
import os
import math
import random


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


class Window:
    def __init__(self):
        # width = pygame.display.Info().current_w
        # height = pygame.display.Info().current_h
        self.running = True

    def switch(self):
        self.running = False
        delete_widgets()


class Menu(Window):
    def __init__(self):
        super().__init__()
        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, screen.get_size())

        self.names_data = tuple(cursor.execute('''SELECT * FROM data''').fetchall())
        self.names = tuple(map(lambda x: x[1], self.names_data))

        with open('preferences.txt') as file:
            self.file_data = file.readlines()
            self.name_id = int(self.file_data[0][7:])

        self.selected_name = self.names[self.name_id - 1]


class MainWindow(Menu):
    def __init__(self):
        super().__init__()
        self.Win = None
        font = pygame.font.Font(None, 150)
        text = font.render('Морская оборона', True, (255, 0, 0))
        self.draw_buttons()
        screen.blit(self.picture, (0, 0))
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            screen.blit(text, (0.5 * width - text.get_width() // 2, round(0.1 * height)))
            pygame_widgets.update(events)
            pygame.display.flip()

    def end(self):
        self.switch()

    def to_options(self):
        self.switch()
        self.Win = Options()

    def to_top_players(self):
        self.switch()
        self.Win = TopPlayers()

    def to_shipyard(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_level_mode(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_survival(self):
        self.switch()
        self.Win = Battlefield()

    def to_name(self):
        self.switch()
        self.Win = Name()

    def draw_buttons(self):
        button_titles = ('name', 'Выживание', 'Кампания', 'Верфь', 'Топ игроков', 'Настройки', 'Выход')
        button_functions = (self.to_survival, self.to_level_mode, self.to_shipyard,
                            self.to_top_players, self.to_options, self.end)
        for number_of_button in range(1, 7):  # создание кнопок для перехода в другие окна
            Button(
                screen,
                round(width * 0.3),
                round(height * (0.06 + number_of_button * 0.13 + 0.03)),
                round(width * 0.4),
                round(height * 0.1),
                colour='blue', text=button_titles[number_of_button], textColour='yellow',
                fontSize=60, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
                onRelease=button_functions[number_of_button - 1]
            )
        Button(  # создание кнопки для настройки пользователя
            screen,
            round(width * 0.835),
            round(height * 0.03),
            round(width * 0.15),
            round(height * 0.05),
            colour='lightblue', text='username', onRelease=self.to_name, fontSize=36
        )


class Name(Menu):  # переход к окну "Имя"
    def __init__(self):
        super().__init__()
        self.Win = None
        self.is_change = False
        self.width_value = 0
        self.names_combobox = None
        self.name_box = None
        self.draw_buttons()
        self.show()

    def show(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.is_change:
                if self.is_change == 'change':
                    self.width_value = 0.6

                self.draw_field()
                self.is_change = False

            screen.blit(self.picture, (0, 0))
            pygame_widgets.update(events)
            pygame.display.flip()

    def draw_buttons(self):
        self.names_combobox = Dropdown(
            screen,
            round(0.35 * width),
            round(0.1 * height),
            round(0.3 * width),
            round(0.05 * height),
            name=self.selected_name, choices=self.names, fontSize=54,
            colour='green', hoverColour='yellow', pressedColour='red'
        )

        Button(  # кнопка "В меню без сохранения информации"
            screen,
            round(width * 0.75),
            round(height * 0.85),
            round(width * 0.2),
            round(height * 0.1),
            colour='blue', text='Отмена', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

        Button(  # кнопка "Сохранить и вернуться в меню"
            screen,
            round(width * 0.53),
            round(height * 0.85),
            round(width * 0.2),
            round(height * 0.1),
            colour='green', text='ОК', textColour='red',
            fontSize=50, radius=10, hoverColour='lightgreen', pressedColour='darkgrey',
            onRelease=self.change_data
        )

        Button(  # кнопка для создания нового профиля
            screen,
            round(width * 0.7),
            round(height * 0.1),
            round(width * 0.2),
            round(height * 0.05),
            colour='yellow', text='Создать профиль', textColour='red',
            fontSize=32, hoverColour='grey', pressedColour='darkgrey',
            onRelease=self.show_new_name
        )

        Button(  # кнопка для редактирования профиля
            screen,
            round(width * 0.1),
            round(height * 0.1),
            round(width * 0.2),
            round(height * 0.05),
            colour='yellow', text='Редактировать профиль', textColour='red',
            fontSize=32, hoverColour='grey', pressedColour='darkgrey',
            onRelease=self.show_changed_name
        )

    def show_new_name(self):
        self.is_change = 'new'
        self.delete_name_field()

    def show_changed_name(self):
        self.is_change = 'change'
        self.delete_name_field()

    def to_menu(self):
        self.switch()
        self.Win = MainWindow()

    def change_data(self):
        with open('preferences.txt', 'r+') as file:
            try:
                self.file_data[0] = f'name = {self.names.index(self.names_combobox.getSelected()) + 1}'

            except ValueError:
                pass

            file.writelines(self.file_data)

        self.to_menu()

    def draw_field(self):
        Button(
            screen,
            round(width * (0.7 - self.width_value)),
            round(height * 0.1),
            round(width * 0.2),
            round(height * 0.05),
            colour='yellow', text='Введите имя' if self.is_change == 'new' else 'Измените имя',
            textColour='red', fontSize=32, hoverColour='grey', pressedColour='darkgrey'
        )

        self.name_box = TextBox(
            screen,
            round(width * (0.7 - self.width_value)),
            round(height * 0.18),
            round(width * 0.2),
            round(height * 0.05),
            fontSize=32, colour='grey', hoverColour='yellow', pressedColour='red'
        )

        Button(
            screen,
            round(width * (0.7 - self.width_value)),
            round(height * 0.26),
            round(width * 0.2),
            round(height * 0.05),
            colour='blue', text='Создать' if self.is_change == 'new' else 'Изменить', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.new_name if self.is_change == 'new' else self.change_name
        )

        Button(
            screen,
            round(width * (0.7 - self.width_value)),
            round(height * 0.34),
            round(width * 0.2),
            round(height * 0.05),
            colour='blue', text='Отмена', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.delete_name_field
        )

        self.width_value = 0

    def delete_name_field(self):
        delete_widgets()
        self.draw_buttons()

    def update_data(self):
        self.names_data = tuple(cursor.execute('''SELECT * FROM data''').fetchall())
        self.names = tuple(map(lambda x: x[1], self.names_data))

    def new_name(self):
        cursor.execute(f'''INSERT INTO data(name, level) VALUES ('{self.name_box.getText()}', 1)''')
        connection.commit()
        self.update_data()
        self.delete_name_field()

    def change_name(self):
        cursor.execute(f'''UPDATE data SET name = '{self.name_box.getText()}' WHERE id = {self.name_id}''')
        connection.commit()
        self.update_data()
        self.delete_name_field()


class Options(Window):
    def __init__(self):
        super().__init__()
        self.Win = None
        self.music_box = TextBox(screen, round(0.52 * width) + 200, round(0.2 * height) - 10, 60,
                                 50, fontSize=35)  # отображает громкость музыки
        self.music_slider = Slider(screen, round(0.2 * width) + 200, round(0.2 * height), round(width * 0.3), 30,
                                   colour='white', handleColour=pygame.Color('red'),
                                   max=1, min=0, step=0.01, initial=1)  # ползунок громкости музыки
        self.sound_box = TextBox(screen, round(0.52 * width) + 200, round(0.3 * height) - 10, 60,
                                 50, fontSize=35)  # отображает громкость звуков
        self.sound_slider = Slider(screen, round(0.2 * width) + 200, round(0.3 * height), round(width * 0.3), 30,
                                   colour='white', handleColour=pygame.Color('red'),
                                   max=1, min=0, step=0.01, initial=1)  # ползунок громкости звуков
        self.combobox1 = Dropdown(screen, round(0.2 * width) + 200, round(0.4 * height), round(width * 0.3),
                                  50, name='Разрешение экрана',  # настройка расширения экрана
                                  choices=['Полный экран', '1280 x 720', '1920 x 1080',
                                           '2048 x 1152', '3840 x 2160'],
                                  borderRadius=3, colour='grey', fontSize=50,
                                  values=[(full_width, full_height),
                                          (1280, 720), (1920, 1080), (2048, 1152), (3840, 2160)],
                                  direction='down', textHAlign='centre')
        self.combobox2 = Dropdown(screen, round(0.2 * width) + 200, round(0.5 * height), round(width * 0.3),
                                  50, name='Максимальный FPS',  # настройка расширения экрана
                                  choices=['120', '100', '80', '60', '40'],
                                  borderRadius=3, colour='grey', fontSize=50,
                                  direction='down', textHAlign='centre')
        self.draw_buttons()
        header_font = pygame.font.Font(None, 150)
        header_text = header_font.render('Настройки', True, (255, 0, 0))
        functions_texts = ['Музыка', 'Звуковые эффекты', 'Разрешение экрана', 'Частота кадров']
        functions_font = pygame.font.Font(None, 60)
        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, (width, height))
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.update_sliders()
            if self.combobox1.getSelected():
                self.new_width, self.new_height = self.combobox1.getSelected()
            if self.combobox2.getSelected():
                clock.tick(int(self.combobox2.getSelected()))
            screen.blit(self.picture, (0, 0))
            screen.blit(header_text, (round(0.4 * width), round(0.05 * height)))
            for num in range(len(functions_texts)):
                function_text = functions_font.render(functions_texts[num], True, (255, 0, 0))
                screen.blit(function_text, (round(0.01 * width), round((0.2 + num / 10) * height)))
            pygame_widgets.update(events)
            pygame.display.flip()

    def update_sliders(self):
        current_music_slider_value = self.music_slider.getValue()
        self.music_box.setText(str(round(100 * current_music_slider_value)))
        pygame.mixer.music.set_volume(current_music_slider_value)
        current_sound_slider_value = self.sound_slider.getValue()
        self.sound_box.setText(str(round(100 * current_sound_slider_value)))

    def draw_buttons(self):
        Button(
            screen,
            round(width * 0.75),
            round(height * (0.7 + 1 * 0.15)),
            round(width * 0.2),
            round(height * 0.1),
            colour='blue', text='В главное меню', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

    def to_menu(self):
        global width, height, size
        self.switch()
        try:
            if self.new_width != width:
                size = width, height = self.new_width, self.new_height
                pygame.display.set_mode(size)
        except AttributeError:
            pass
        self.Win = MainWindow()


class TopPlayers(Menu):
    def __init__(self):
        super().__init__()
        self.Win = None
        screen.blit(self.picture, (0, 0))
        font = pygame.font.Font(None, 150)
        text = font.render('Топ игроков', True, (255, 0, 0))
        self.combobox = Dropdown(screen, 0.05 * width, 0.1 * height, 0.3 * width, 0.075 * height, name='Тип рекорда',
                                 choices=['Всего набранных очков', 'Набрано очков за игру', 'Время боя'],
                                 values=[1, 2, 3],
                                 borderRadius=3, colour='blue', fontSize=50,
                                 direction='down', textHAlign='centre', textColour='yellow')
        self.draw_widgets()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            if self.combobox.getSelected():
                if self.combobox.getSelected() == 1:
                    pass
                elif self.combobox.getSelected() == 2:
                    pass
                else:
                    pass
            screen.blit(self.picture, (0, 0))
            screen.blit(text, (width * 0.5 - text.get_width() // 2, round(0.01 * height)))
            pygame_widgets.update(events)
            pygame.display.flip()

    def draw_widgets(self):
        for h in range(10):
            for w in range(2):
                cell = Button(screen, 0.05 * width + 0.45 * w * width, 0.2 * height + h * 0.07 * height, 0.45 * width,
                              0.07 * height, textHAlign='center', textColour='blue', fontSize=40,
                              borderColour='black', borderThickness=5)
                cell.disable()
                cell.draw()
        Button(
            screen,
            round(width * 0.75),
            round(height * 0.91),
            round(width * 0.2),
            round(height * 0.07),
            colour='blue', text='В главное меню', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

    def to_menu(self):
        self.switch()
        self.Win = MainWindow()


class Ship(pygame.sprite.Sprite):  # класс корабля (общий для игрока и противников)
    def __init__(self, group, explosion_group):
        super().__init__(group)
        self.armor = 0  # количество брони
        self.speed = 0  # скорость корабля
        self.explosion_group = explosion_group

    def torpedo_shot(self, coordinates, group, explosion_group):  # функция запуска торпеды
        torpedo.play()

        if self.rect.x + self.rect.w * 0.5 > coordinates[0]:
            Torpedo(round(self.rect.x + 0.1 * self.rect.w), round(0.93 * self.rect.y),
                    coordinates, group, explosion_group)

        else:
            Torpedo(round(self.rect.x + 0.9 * self.rect.w), round(0.93 * self.rect.y),
                    coordinates, group, explosion_group)

    def get_damage(self, damage):  # функция получения урона
        self.armor -= damage

    def explode(self):
        self.kill()
        Explosion((self.rect.centerx - self.rect.w * 0.25, self.rect.centery),
                  (self.rect.w * 1.5, self.rect.h * 1.5), self.explosion_group)


class Player(Ship):  # класс игрока
    def __init__(self, group, explosion_group):
        super().__init__(group, explosion_group)
        self.image = pygame.transform.scale(load_image('Player.png'), (width * 0.25, height * 0.25))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = round(0.35 * width), round(0.78 * height)
        self.left = False  # плывём влево
        self.right = False  # плывём вправо
        self.reloading = False
        self.torpedo = True
        self.armor = 100
        self.max_armor = self.armor

        self.ammo = 0
        self.health_bar = ProgressBar(screen, self.rect.x, 0.05 * height, self.rect.w, 0.02 * height,
                                      lambda: self.armor / self.max_armor, completedColour='green',
                                      incompletedColour='white')

        self.start = pygame.time.get_ticks()
        self.torpedo_time = pygame.time.get_ticks()
        self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                   lambda: (pygame.time.get_ticks() - self.start) / (1700 * (3 - self.ammo)),
                                   completedColour='blue', incompletedColour='red')

        self.ammo = 3
        self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.08, width * 0.2, height * 0.02,
                                       lambda: (pygame.time.get_ticks() - self.torpedo_time) / 3000,
                                       completedColour='blue', incompletedColour='red')

        self.health_bar.draw()

    def gun_shot(self, coordinates, group, explosion_group):  # функция выстрела из пушки
        gun.play()
        Bullet(round(self.rect.centerx), round(0.98 * self.rect.y), coordinates, group, explosion_group)
        self.ammo -= 1

        if self.ammo == 0:
            self.start_reloading()

    def start_reloading(self):
        self.start = pygame.time.get_ticks()
        self.reloading = True

    def reload(self):
        self.ammo = 3

    def start_torpedo_reload(self):
        self.torpedo = False
        self.torpedo_time = pygame.time.get_ticks()

    def torpedo_reload(self):
        self.torpedo = True

    def update(self, *args):  # изменение местоположения
        if self.right:
            self.rect.x += 4

            if self.rect.x + self.rect.w > width:
                self.rect.x = width - self.rect.w

        if self.left:
            self.rect.x -= 4

            if self.rect.x < 0:
                self.rect.x = 0

        if pygame.time.get_ticks() - self.start >= 1700 * (3 - self.ammo) and self.reloading:
            self.reloading = False
            self.reload()

        if pygame.time.get_ticks() - self.torpedo_time >= 3000:
            self.torpedo_reload()

        if self.reloading:
            self.gun_bar.draw()

        if not self.torpedo:
            self.torpedo_bar.draw()

        self.health_bar.draw()

        if self.armor <= 0:
            self.health_bar.hide()
            self.explode()


class Enemy(Ship):  # класс врага
    params = {'Канонерка': (50, 2.0, 100), 'Эсминец': (100, 1.5, 150),
              'Линкор': (200, 1, 200), 'Крейсер': (300, 1, 300)}

    # каждому виду корабля соответствуют свои характеристики: armor, speed, направление (вправо плывет или влево)

    def __init__(self, group, explosion_group, ship_type):
        super().__init__(group, explosion_group)
        self.info = self.params[ship_type]
        self.ship_type = ship_type
        self.armor = self.info[0]
        self.points = self.info[-1]
        if ship_type == 'Канонерка':
            self.image = pygame.transform.scale(load_image(random.choice(('Канонерка.png',
                                                                          'Канонерка2.png',
                                                                          'Канонерка3.png'))),
                                                (width * 0.1, height * 0.04))

        elif ship_type == 'Эсминец':
            self.image = pygame.transform.scale(load_image(random.choice(('Эсминец.png',
                                                                          'Эсминец2.png'))),
                                                (width * 0.1, height * 0.04))

        elif ship_type == 'Линкор':
            self.image = pygame.transform.scale(load_image(random.choice(('Линкор.png',
                                                                          'Линкор2.png'))),
                                                (width * 0.1, height * 0.04))

        elif ship_type == 'Крейсер':
            self.image = pygame.transform.scale(load_image(random.choice(('Крейсер.png',
                                                                          'Крейсер2.png'))),
                                                (width * 0.1, height * 0.04))

        self.shot_time = random.randint(6, 10)
        self.time = pygame.time.get_ticks()
        self.rect = self.image.get_rect()
        self.direction = random.randint(0, 1)

        if self.direction == 0:
            self.rect.x = width * -0.1

        else:
            self.rect.x = width
            self.image = pygame.transform.flip(self.image, True, False)

        self.x = self.rect.x
        self.max_armor = self.armor
        self.rect.y = height * 0.25
        self.clear_event = pygame.USEREVENT + 3
        self.health_bar = ProgressBar(screen, self.rect.x, self.rect.y - 0.04 * height, self.rect.w, 0.01 * height,
                                      lambda: self.armor / self.max_armor, completedColour='red')
        self.health_bar.draw()
        # появляется за экраном
        # выпускает торпеду с периодом ок. 3-6 секунд
        # каждому типу соответствует своя картинка (см. Images)

    def update(self, player: Player, torpedo_group, explosion_group):  # перемещение корабля
        if self.direction == 0:
            self.x += self.params[self.ship_type][1]

        else:
            self.x -= self.params[self.ship_type][1]
        self.rect.x = self.x

        self.health_bar.moveX(self.rect.x - self.health_bar.getX())
        self.health_bar.draw()

        if (pygame.time.get_ticks() - self.time) / 1000 >= self.shot_time:
            Torpedo(self.rect.centerx, self.rect.y + self.rect.w * 0.5,
                    (player.rect.x + random.uniform(0.4, 0.6) * player.rect.w, player.rect.y),
                    torpedo_group, explosion_group)

            self.shot_time = random.randint(8, 12)
            self.time = pygame.time.get_ticks()

        if not width * -0.1 <= self.rect.x <= width * 1.1:
            self.kill()

        if self.armor <= 0:
            global score
            score += self.points
            # Анимация взрыва
            self.kill()
            self.explode()
            self.health_bar.hide()


class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coordinates: tuple, group, explosion_group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.x1, self.y1 = point_coordinates
        self.image = pygame.transform.scale(load_image('torpedo1.png'), (round(width * 0.01), round(height * 0.12)))

        try:
            self.angle = math.ceil(math.degrees
                                   (math.atan((self.y1 - self.y) / (self.x - self.x1))))

            if self.x > self.x1 and self.y > self.y1:
                self.angle += 180

            if self.x1 < self.x and self.y1 > self.y:
                self.angle += 180

        except ZeroDivisionError:
            self.angle = 90

            if self.y < self.y1:
                self.angle = 270

        self.rotate()
        self.delta_y = -0.0025 * height * math.sin(math.radians(self.angle))
        self.delta_x = 0.0025 * height * math.cos(math.radians(self.angle))

        self.rect = self.image.get_rect()
        self.explosion_group = explosion_group
        self.rect.x = self.x
        self.rect.y = self.y

    def rotate(self):
        self.image = pygame.transform.rotate(self.image, self.angle + 270)

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                sprite.get_damage(80)
                if self.delta_y < 0:
                    Explosion((self.rect.centerx, self.rect.y), (0.05 * width, 0.03 * height), self.explosion_group)
                else:
                    Explosion((self.rect.centerx, self.rect.y + self.rect.h),
                              (0.05 * width, 0.03 * height), self.explosion_group)
                self.kill()

        else:
            if self.y < 0.27 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > 0.92 * height:
                self.kill()

            self.x += self.delta_x
            self.y += self.delta_y
            self.rect.x = self.x
            self.rect.y = self.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coordinates: tuple, group, explosion_group):
        super().__init__(group)
        self.x = x
        self.y = y
        self.x1, self.y1 = point_coordinates

        try:
            self.angle = math.floor(math.degrees
                                    (math.atan(abs((self.y1 - self.y) / (self.x - round(width * 0.025) - self.x1)))))

        except ZeroDivisionError:
            self.angle = 90

        if self.x1 < self.x:
            self.angle = 180 - self.angle

        self.delta_y = -0.04 * height * math.sin(math.radians(self.angle))
        self.delta_x = 0.04 * height * math.cos(math.radians(self.angle))
        self.image = pygame.transform.scale(load_image('Bullet.png'), (round(width * 0.006), round(height * 0.01)))
        self.rect = self.image.get_rect()
        self.explosion_group = explosion_group
        self.rect.x = self.x
        self.rect.y = self.y
        self.rotate()

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(self, sprite):
                sprite.get_damage(16)
                Explosion((self.rect.centerx, self.rect.y), (0.05 * width, 0.03 * height), self.explosion_group)
                self.kill()

        else:
            if self.y < 0.27 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > height:
                self.kill()

            self.x += self.delta_x
            self.y += self.delta_y
            self.rect.x = self.x
            self.rect.y = self.y

    def rotate(self):
        if self.x != self.x1:
            if self.angle < 0:
                self.image = pygame.transform.rotate(self.image, self.angle + 90)

            else:
                self.image = pygame.transform.rotate(self.image, self.angle + 270)


class Battlefield(Window):  # игровое поле, унаследовать от WINDOW
    def __init__(self):
        super().__init__()
        music_number = 0
        # чем выше сложность, тем выше будет скорость всего происходящего
        # погодные условия потом
        global score

        music_list = [int(j) for j in range(17)]
        random.shuffle(music_list)

        pygame.mixer.music.set_volume(music_volume / 3)

        pygame.mixer.music.load(f'Audio/Battle{music_list[0]}.mp3')
        pygame.mixer.music.play()
        music_number += 1
        self.start_time = pygame.time.get_ticks()
        score = 0
        self.bg = pygame.transform.scale(load_image('img.png'), screen.get_size())  # фоновое изображение
        self.ship_group = pygame.sprite.Group()
        self.torpedo_group = pygame.sprite.Group()  # группы спрайтов
        self.bullet_group = pygame.sprite.Group()
        self.mine_group = pygame.sprite.Group()
        self.other = pygame.sprite.Group()
        self.player = Player(self.ship_group, self.other)  # игрок
        self.cursor = Cursor()
        self.other.add(self.cursor)
        self.score = TextBox(screen, 0.85 * width, 0.06 * height, 0.08 * width, 0.04 * height,
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)
        self.timer = TextBox(screen, 0.85 * width, 0.01 * height, 0.08 * width, 0.04 * height,
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)
        self.score.disable()
        self.end_event = pygame.USEREVENT + 3
        self.update_time = pygame.USEREVENT + 2
        self.random_event = pygame.USEREVENT + 1  # событие генерации событий
        pygame.time.set_timer(self.random_event, random.randint(1, 3) * 1000, 1)  # первое событие через 1-3 с
        pygame.time.set_timer(self.update_time, 10, 1)
        end = False
        while self.running:
            if self.player.armor <= 0 and not end:
                end = True
                pygame.time.set_timer(self.end_event, 1500, 1)

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(f'Audio/Battle{music_list[music_number]}.mp3')
                pygame.mixer.music.play()
                music_number += 1
                music_number %= 17

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key in {pygame.K_LEFT, pygame.K_a}:
                        self.player.left = True

                    if event.key in {pygame.K_RIGHT, pygame.K_d}:
                        self.player.right = True

                if event.type == pygame.KEYUP:
                    if event.key in {pygame.K_LEFT, pygame.K_a}:  # для перемещения игрока по сторонам
                        self.player.left = False

                    if event.key in {pygame.K_RIGHT, pygame.K_d}:
                        self.player.right = False

                    if event.key == pygame.K_SPACE and 0 < self.player.ammo < 3 and not self.player.reloading:
                        self.player.start_reloading()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # ПКМ - пуск торпеды
                        if self.player.torpedo:
                            if event.pos[1] < height * 0.6:  # но вбок нельзя
                                self.player.torpedo_shot(event.pos, self.torpedo_group, self.other)
                                self.player.start_torpedo_reload()

                    if event.button == 1:  # ЛКМ - выстрел из пушки
                        if self.player.ammo != 0 and not self.player.reloading:
                            sprite = pygame.sprite.spritecollideany(self.cursor, self.mine_group)
                            if sprite:
                                Explosion(sprite.rect.center, (0.1 * width, 0.1 * height), self.other)
                                sprite.kill()
                                gun.play()
                                score += 50
                                self.player.ammo -= 1
                                if self.player.ammo == 0:
                                    self.player.start_reloading()

                            elif event.pos[1] < height * 0.6:  # но вбок нельзя
                                self.player.gun_shot(event.pos, self.bullet_group, self.other)

                if event.type == self.random_event:  # генерация случайного события
                    if len(self.ship_group) != 1:
                        generated_event = random.choice(['мина' for _ in range(13)] + ['корабль' for _ in range(7)])
                    else:
                        generated_event = 'корабль'

                    if generated_event == 'мина':
                        self.spawn_mine()  # спавнит мину

                    else:
                        self.spawn_enemy()  # спавнит корабль врага

                    pygame.time.set_timer(self.random_event, random.randint(7, 11) * 1000, 1)  # новое событие 7-11 с
                if event.type == self.update_time:
                    screen.blit(self.bg, (0, 0))
                    self.ship_group.update(self.player, self.torpedo_group, self.other)
                    self.torpedo_group.update(self.ship_group)
                    self.bullet_group.update(self.ship_group)
                    self.mine_group.update(self.player)
                    self.other.update()
                    self.torpedo_group.draw(screen)
                    self.bullet_group.draw(screen)
                    self.mine_group.draw(screen)
                    self.ship_group.draw(screen)
                    self.score.setText(score)
                    self.score.draw()
                    self.timer.setText(f"{(pygame.time.get_ticks() - self.start_time) // 1000 // 60}м: "
                                       f"{(pygame.time.get_ticks() - self.start_time) // 1000 % 60}с")
                    self.timer.draw()
                    self.other.draw(screen)
                    pygame.display.flip()
                    pygame.time.set_timer(self.update_time, 25, 1)
                if event.type == self.end_event:
                    pygame.mixer.music.stop()
                    self.switch()
                    self.Win = Endgame()

    def spawn_mine(self):  # функция спавна мины
        shoal_width = random.uniform(0.05, 0.3)
        Mine((random.uniform(0.05, 1 - shoal_width) * width, 0.3 * height),
             (shoal_width * width, random.uniform(0.05, 0.2) * height), self.mine_group, self.other)

    def spawn_enemy(self):  # функция спавна корабля
        Enemy(self.ship_group, self.other,
              ship_type=random.choice(
                  ['Канонерка', 'Эсминец', 'Линкор', 'Крейсер']))


class Mine(pygame.sprite.Sprite):  # класс мины
    def __init__(self, coordinates: tuple, shoal_size: tuple, group, explosion_group):
        super().__init__(group)
        self.size = shoal_size
        self.image = pygame.transform.scale(load_image('Mine.png'), (0.03 * width, 0.03 * width))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coordinates
        self.explosion_group = explosion_group

    def update(self, player):  # надо сделать так, чтобы из точки появлялась мина
        self.rect.y += 0.005 * height

        if pygame.sprite.collide_mask(self, player):  # проверка удара
            player.get_damage(40)
            Explosion((self.rect.centerx, self.rect.y + self.rect.h), (0.1 * width, 0.1 * height),
                      self.explosion_group)
            self.kill()

        else:
            if self.rect.y >= height * 0.98:  # выход за границу
                self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size, group):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        group.add(self)
        explosion.play()

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame == len(explosion_anim):
                self.kill()

            else:
                center = self.rect.center
                self.image = pygame.transform.scale(explosion_anim[self.frame], self.size)
                self.rect = self.image.get_rect()
                self.rect.center = center


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image('cursor.png'), (0.05 * width, 0.05 * width))
        pygame.mouse.set_visible(False)
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.mouse.get_focused():
            x1, y1 = pygame.mouse.get_pos()
            self.rect.x = x1
            self.rect.y = y1

        else:
            self.rect.x = -100


class Endgame(Window):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pygame.init()
    connection = sqlite3.connect('Data/name.sqlite')
    cursor = connection.cursor()
    FPS = 60
    full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    clock.tick(FPS)
    music_volume = 1
    audio_volume = 1
    explosion = pygame.mixer.Sound('Audio/explosion.mp3')
    torpedo = pygame.mixer.Sound('Audio/torpedo.mp3')
    gun = pygame.mixer.Sound('Audio/gun.mp3')
    score = 1
    explosion_anim = []
    for i in range(1, 17):
        filename = 'взрыв торпеды{}.png'.format(i)
        img = load_image(filename).convert()
        img = pygame.transform.scale(img, (width * 0.05, height * 0.05))
        explosion_anim.append(img)
    MainWindow()
