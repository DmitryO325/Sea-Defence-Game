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
        self.health = 0  # количество брони
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
        self.health -= damage

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

        self.reloading = False  # перезарядка орудия

        self.health = 100  # количество здоровья игрока
        self.max_health = self.health  # для вывода количества оставшегося здоровья на шкале

        self.total_ammo = 100  # первичный арсенал
        self.total_torpedoes = 20

        self.health_bar = ProgressBar(screen, 0.4 * width, 0.08 * height, 0.3 * width, 0.02 * height,
                                      lambda: self.health / self.max_health,  # шкала здоровья
                                      completedColour='darkgreen', incompletedColour='red')

        self.start = pygame.time.get_ticks()  # начало перезарядки пушки
        self.torpedo_time = pygame.time.get_ticks()  # начало подготовки торпеды

        self.ammo = 3  # количество снарядов в отсеке пушки
        self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                   lambda: self.ammo / 3, completedColour='blue', incompletedColour='red')
        # шкала со снарядами пушки
        self.torpedo = 1  # торпеда готова к пуску
        self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.08, width * 0.2, height * 0.02,
                                       lambda: 1, completedColour='blue', incompletedColour='red')
        # шкала готовности торпеды

    def gun_shot(self, coordinates, group, explosion_group):  # функция выстрела из пушки
        gun.play()  # звук выстрела из пушки
        Bullet(round(self.rect.centerx), round(0.98 * self.rect.y), coordinates, group, explosion_group)
        # запуск снаряда
        self.ammo -= 1  # изменения в арсенале
        self.total_ammo -= 1

        if self.ammo == 0:  # автоматическое начало перезарядки
            self.start_reloading()

    def start_reloading(self):
        self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                   lambda: (pygame.time.get_ticks() - self.start + self.ammo * 1700) / (1700 * 3),
                                   completedColour='yellow', incompletedColour='red')
        # обновление шкалы пушки
        self.start = pygame.time.get_ticks()  # замер времени
        self.reloading = True  # начало перезарядки

    def reload(self):
        if self.total_ammo >= 3:
            self.ammo = 3  # восполнение боекомплекта
        else:
            self.ammo = self.total_ammo

    def start_torpedo_reload(self):
        self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.08, width * 0.2, height * 0.02,
                                       lambda: (pygame.time.get_ticks() - self.torpedo_time) / 3000,
                                       completedColour='yellow', incompletedColour='red')
        # обновление шкалы торпеды
        self.total_torpedoes -= 1

        self.torpedo = 0  # начало подготовки новой торпеды
        self.torpedo_time = pygame.time.get_ticks()

    def torpedo_reload(self):
        self.torpedo = 1  # торпеда готова

    def add_bullets(self, ammo):
        self.total_ammo += ammo  # добавление снарядов

    def add_torpedoes(self, torpedoes):
        self.total_torpedoes += torpedoes  # добавление торпед

    def add_health(self, health):
        self.health = self.health + health if self.health + health <= self.max_health else self.max_health
        # добавление здоровья

    def add_max_health(self, health):
        self.max_health += health  # увеличение максимального здоровья
        self.health += health

    def update(self, *args):  # изменение местоположения
        if self.right:
            self.rect.x += 4

            if self.rect.x + self.rect.w > width:
                self.rect.x = width - self.rect.w

        if self.left:
            self.rect.x -= 4

            if self.rect.x < 0:
                self.rect.x = 0

        if pygame.time.get_ticks() - self.start >= 1700 * min((3 - self.ammo), self.total_ammo) and self.reloading:
            self.reloading = False  # завершение зарядки орудия
            self.reload()

            self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                       lambda: self.ammo / 3,
                                       completedColour='blue', incompletedColour='red')
            # обновление шкалы пушки
        if pygame.time.get_ticks() - self.torpedo_time >= 3000:
            self.torpedo_reload()  # завершение подготовки торпеды

            self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.08, width * 0.2, height * 0.02,
                                           lambda: 1, completedColour='blue', incompletedColour='red')

        self.gun_bar.draw()
        self.torpedo_bar.draw()  # прорисовка шкалы здоровья, пушки, торпеды
        self.health_bar.draw()

        if self.health <= 0:
            self.health_bar.hide()  # взрыв корабля
            self.explode()


class Enemy(Ship):  # класс врага
    params = {'Канонерка': (50, 2.0, 100), 'Эсминец': (100, 1.5, 150),
              'Линкор': (200, 1, 200), 'Крейсер': (300, 1, 300)}

    def __init__(self, group, explosion_group, ship_type):
        super().__init__(group, explosion_group)
        self.info = self.params[ship_type]  # параметры корабля: здоровье, скорость, очки за потопление
        self.ship_type = ship_type
        self.health = self.info[0]  # здоровье
        self.points = self.info[-1]  # очки за потопление

        self.event = 0  # выпадение бонуса при потоплении

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
        # спрайт корабля
        self.shot_time = random.randint(6, 10)  # таймер первого выстрела
        self.time = pygame.time.get_ticks()  # время прошлого выстрела
        self.rect = self.image.get_rect()  # получение квадрата спрайта
        self.direction = random.randint(0, 1)  # направление: право или влево

        if self.direction == 0:
            self.rect.x = width * -0.1

        else:
            self.rect.x = width
            self.image = pygame.transform.flip(self.image, True, False)
        # спавн корабля
        self.x = self.rect.x  # отслеживание координат корабля по оси абсцисс
        self.max_health = self.health  # аналогично в Player
        self.rect.y = height * 0.25  # координаты по оси ординат
        self.health_bar = ProgressBar(screen, self.rect.x, self.rect.y - 0.04 * height, self.rect.w, 0.01 * height,
                                      lambda: self.health / self.max_health, completedColour='red')  # шкала здоровья
        self.health_bar.draw()

    def update(self, player: Player, torpedo_group, bonus_group, explosion_group):  # перемещение корабля
        if self.direction == 0:
            self.x += self.params[self.ship_type][1]

        else:
            self.x -= self.params[self.ship_type][1]

        self.rect.x = self.x  # перемещение по оси абсцисс

        self.health_bar.moveX(self.rect.x - self.health_bar.getX())  # шкала движется с кораблем
        self.health_bar.draw()

        if (pygame.time.get_ticks() - self.time) / 1000 >= self.shot_time:  # время запуска торпеды
            Torpedo(self.rect.centerx, self.rect.y + self.rect.w * 0.5,
                    (player.rect.x + random.uniform(0.4, 0.6) * player.rect.w, player.rect.y),
                    torpedo_group, explosion_group)

            self.shot_time = random.randint(8, 12)  # новое время запуска
            self.time = pygame.time.get_ticks()  # обновление таймера

        if not width * -0.1 <= self.rect.x <= width * 1.1:
            self.kill()  # при выходе за горизонт

        if self.health <= 0:
            global score
            score += self.points

            self.kill()

            self.event = random.randint(1, 100)  # бонус

            if 1 <= self.event <= 70:
                Bonuses(self.rect.centerx, self.rect.y + self.rect.w * 0.5,
                        bonus_group, self.event)
            # Анимация взрыва
            self.explode()
            self.health_bar.hide()  # исчезновение шкалы здоровья


class Bonuses(pygame.sprite.Sprite):
    def __init__(self, x, y, group, bonus_number):
        super().__init__(group)
        self.x = x  # координаты бонуса
        self.y = y
        self.bonus_number = bonus_number  # тип бонуса

        if 1 <= self.bonus_number <= 20:
            self.image = pygame.transform.scale(load_image('Bullets.png'),  # снаряды
                                                (round(width * 0.05 * 9 / 16), round(height * 0.05)))

        elif 21 <= self.bonus_number <= 40:
            self.image = pygame.transform.scale(load_image('Torpedoes.png'),  # торпеды
                                                (round(width * 0.05 * 9 / 16), round(height * 0.05)))

        elif 41 <= self.bonus_number <= 60:
            self.image = pygame.transform.scale(load_image('Repair.png'),  # починка
                                                (round(width * 0.05 * 9 / 16), round(height * 0.05)))

        elif 61 <= self.bonus_number <= 70:
            self.image = pygame.transform.scale(load_image('Modification.png'),  # увеличение максимального здоровья
                                                (round(width * 0.05 * 9 / 16), round(height * 0.05)))

        self.delta_y = 0.0025 * height  # величина перемещения по оси ординат

        self.rect = self.image.get_rect()  # прямоугольник спрайта

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                if 1 <= self.bonus_number <= 20:
                    sprite.add_bullets(random.randint(5, 25))

                elif 21 <= self.bonus_number <= 40:
                    sprite.add_torpedoes(random.randint(1, 7))  # получение кораблем игрока бонуса

                elif 41 <= self.bonus_number <= 60:
                    sprite.add_health(random.randint(5, 20))

                elif 61 <= self.bonus_number <= 70:
                    sprite.add_max_health(random.randint(3, 15))

                self.kill()  # исчезновение при касании

        else:
            if self.y < 0.27 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > height:
                self.kill()  # исчезновение при выходе с поля

            self.y += self.delta_y  # перемещение по оси ординат
            self.rect.y = self.y


class Torpedo(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coordinates: tuple, group, explosion_group):
        super().__init__(group)
        self.x = x  # координаты торпеды
        self.y = y
        self.x1, self.y1 = point_coordinates
        self.image = pygame.transform.scale(load_image('torpedo1.png'), (round(width * 0.01), round(height * 0.12)))
        # изображение спрайта
        try:
            self.angle = math.ceil(math.degrees(math.atan((self.y1 - self.y) / (self.x - self.x1))))
            # первичный угол поворота спрайта
            if self.x > self.x1 and self.y > self.y1:
                self.angle += 180

            if self.x1 < self.x and self.y1 > self.y:
                self.angle += 180

        except ZeroDivisionError:
            self.angle = 90

            if self.y < self.y1:
                self.angle = 270

        self.rotate()  # вращение спрайта

        self.delta_y = -0.0025 * height * math.sin(math.radians(self.angle))  # величины смещения торпеды по осям
        self.delta_x = 0.0025 * height * math.cos(math.radians(self.angle))

        self.rect = self.image.get_rect()  # прямоугольник спрайта
        self.explosion_group = explosion_group  # группа для анимации взрыва

        self.rect.x = self.x  # присваивание спрайту координат
        self.rect.y = self.y

    def rotate(self):  # функция вращения спрайта
        self.image = pygame.transform.rotate(self.image, self.angle + 270)

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_mask(self, sprite):
                sprite.get_damage(80)  # нанесение урона

                if self.delta_y < 0:
                    Explosion((self.rect.centerx, self.rect.y), (0.05 * width, 0.03 * height), self.explosion_group)

                else:  # взрыв зависит от направления торпеды
                    Explosion((self.rect.centerx, self.rect.y + self.rect.h),
                              (0.05 * width, 0.03 * height), self.explosion_group)

                self.kill()

        else:
            if self.y < 0.27 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > 0.92 * height:
                self.kill()  # исчезновение при выходе с поля боя

            self.x += self.delta_x
            self.y += self.delta_y  # смещение по осям
            self.rect.x = self.x
            self.rect.y = self.y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, point_coordinates: tuple, group, explosion_group):
        super().__init__(group)
        self.x = x  # координаты снаряда
        self.y = y
        self.x1, self.y1 = point_coordinates
        self.image = pygame.transform.scale(load_image('Bullet.png'), (round(width * 0.006), round(height * 0.01)))
        # изображение снаряда
        try:
            self.angle = math.floor(math.degrees  # угол поворота
                                    (math.atan(abs((self.y1 - self.y) / (self.x - round(width * 0.025) - self.x1)))))

        except ZeroDivisionError:
            self.angle = 90

        if self.x1 < self.x:
            self.angle = 180 - self.angle

        self.rotate()  # вращение спрайта

        self.delta_y = -0.04 * height * math.sin(math.radians(self.angle))
        self.delta_x = 0.04 * height * math.cos(math.radians(self.angle))  # величины смещения по осям

        self.rect = self.image.get_rect()  # прямоугольник спрайта
        self.explosion_group = explosion_group  # группа для взрыва

        self.rect.x = self.x
        self.rect.y = self.y

    def rotate(self):  # функция поворота
        if self.x != self.x1:
            if self.angle < 0:
                self.image = pygame.transform.rotate(self.image, self.angle + 90)

            else:
                self.image = pygame.transform.rotate(self.image, self.angle + 270)

    def update(self, group):
        for sprite in group:
            if pygame.sprite.collide_rect(self, sprite):
                sprite.get_damage(16)  # нанесение урона противнику
                Explosion((self.rect.centerx, self.rect.y), (0.05 * width, 0.03 * height), self.explosion_group)
                self.kill()  # взрыв и исчезновение

        else:
            if self.y < 0.27 * height or self.x < -0.05 * width or self.x > 1.05 * width or self.y > height:
                self.kill()  # исчезновение при выходе

            self.x += self.delta_x
            self.y += self.delta_y  # смещение по осям
            self.rect.x = self.x
            self.rect.y = self.y


class Battlefield(Window):  # игровое поле, унаследовано от WINDOW
    def __init__(self):
        super().__init__()

        self.music_number = 0  # номер саундтрека
        global score

        self.music_list = [int(j) for j in range(18)]
        random.shuffle(self.music_list)  # перемешка музыки

        pygame.mixer.music.set_volume(music_volume / 3)  # музыка тише звуков (при максимумах)

        pygame.mixer.music.load(f'Audio/Battle{self.music_list[0]}.mp3')
        pygame.mixer.music.play()  # начало проигрывания трека
        self.music_number += 1

        self.start_time = pygame.time.get_ticks()  # начало таймера игры

        score = 0
        self.background = pygame.transform.scale(load_image('img.png'), screen.get_size())  # фоновое изображение

        self.torpedo_image = pygame.transform.scale(load_image('old_torpedo.png'), (width * 0.02, height * 0.06))
        self.torpedo_image = pygame.transform.rotate(self.torpedo_image, 270)  # изображение торпеды

        self.ammo_image = pygame.transform.scale(load_image('Bullet.png'), (width * 0.008, height * 0.03))
        self.ammo_image = pygame.transform.rotate(self.ammo_image, 270)  # изображение снаряда

        self.ship_group = pygame.sprite.Group()
        self.torpedo_group = pygame.sprite.Group()  # группы спрайтов
        self.bullet_group = pygame.sprite.Group()
        self.mine_group = pygame.sprite.Group()
        self.bonus_group = pygame.sprite.Group()
        self.other = pygame.sprite.Group()

        self.player = Player(self.ship_group, self.other)  # игрок
        self.cursor = Cursor()  # курсор
        self.other.add(self.cursor)

        self.score = TextBox(screen, 0.85 * width, 0.05 * height, 0.05 * width, 0.04 * height,  # счёт
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)

        self.timer = TextBox(screen, 0.85 * width, 0.01 * height, 0.05 * width, 0.04 * height,
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)  # время игры

        self.total_ammo_box = TextBox(screen, width * 0.27, height * 0.025, width * 0.03, height * 0.03,
                                      placeholderText=0, colour='grey', textColour='black', fontSize=24)
        # количество снарядов
        self.total_torpedoes_box = TextBox(screen, width * 0.27, height * 0.075, width * 0.03, height * 0.03,
                                           placeholderText=0, colour='grey', textColour='black', fontSize=24)
        # количество торпед
        self.end_event = pygame.USEREVENT + 3  # конец игры (пауза)
        self.update_time = pygame.USEREVENT + 2  # событие обновления экрана
        self.random_event = pygame.USEREVENT + 1  # событие генерации событий

        pygame.time.set_timer(self.random_event, random.randint(1, 3) * 1000, 1)  # первое событие через 1-3 с
        pygame.time.set_timer(self.update_time, 10, 1)  # запуск события

        self.end = False  # конец игры

        while self.running:
            if self.player.health <= 0 and not self.end:  # объявление конца игры
                self.end = True
                pygame.time.set_timer(self.end_event, 1500, 1)

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(f'Audio/Battle{self.music_list[self.music_number]}.mp3')
                pygame.mixer.music.play()
                self.music_number += 1  # смена трека при завершении
                self.music_number %= 18

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

                    if (event.key in {pygame.K_SPACE, pygame.K_w, pygame.K_UP} and
                            0 < self.player.ammo < 3 and not self.player.reloading):
                        self.player.start_reloading()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # ПКМ - пуск торпеды
                        if self.player.torpedo and self.player.total_torpedoes > 0:
                            if event.pos[1] < height * 0.6:  # но вбок нельзя
                                self.player.torpedo_shot(event.pos, self.torpedo_group, self.other)
                                self.player.start_torpedo_reload()

                    if event.button == 1:  # ЛКМ - выстрел из пушки
                        if self.player.ammo != 0 and not self.player.reloading and self.player.total_ammo > 0:
                            sprite = pygame.sprite.spritecollideany(self.cursor, self.mine_group)

                            if sprite:
                                Explosion(sprite.rect.center, (0.1 * width, 0.1 * height), self.other)
                                sprite.kill()  # взрыв мины
                                gun.play()
                                score += 50

                                self.player.ammo -= 1
                                self.player.total_ammo -= 1  # изменение в арсенале
                                self.total_ammo_box.setText(self.player.total_ammo)

                                if self.player.ammo == 0:
                                    self.player.start_reloading()

                            elif event.pos[1] < height * 0.6:  # но вбок нельзя
                                self.player.gun_shot(event.pos, self.bullet_group, self.other)

                    if event.button == 2 and 0 < self.player.ammo < 3 and not self.player.reloading:
                        self.player.start_reloading()

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
                if self.player.total_ammo == 0 and self.player.total_torpedoes == 0 and len(self.bonus_group) < 3:
                    Bonuses(random.uniform(0.1, 0.9) * width, 0.35 * height, self.bonus_group, random.randint(1, 41))
                    # если у игрока нет снарядов, приходит поддержка
                if event.type == self.update_time:
                    screen.blit(self.background, (0, 0))
                    screen.blit(self.torpedo_image, (width * 0.015, height * 0.072))
                    screen.blit(self.ammo_image, (width * 0.025, height * 0.032))

                    self.ship_group.update(self.player, self.torpedo_group, self.bonus_group, self.other)
                    self.torpedo_group.update(self.ship_group)
                    self.bullet_group.update(self.ship_group)  # обновление спрайтов
                    self.mine_group.update(self.player)
                    self.bonus_group.update(self.ship_group)
                    self.other.update()

                    self.torpedo_group.draw(screen)
                    self.bullet_group.draw(screen)
                    self.mine_group.draw(screen)  # прорисовка спрайтов
                    self.ship_group.draw(screen)
                    self.bonus_group.draw(screen)

                    self.score.setText(score)
                    self.score.draw()

                    self.timer.setText(f"{(pygame.time.get_ticks() - self.start_time) // 1000 // 60}:"
                                       f"{str((pygame.time.get_ticks() - self.start_time) // 1000 % 60).zfill(2)}")
                    self.timer.draw()

                    self.total_ammo_box.setText(self.player.total_ammo)
                    self.total_ammo_box.draw()  # обновление и прорисовка виджетов

                    self.total_torpedoes_box.setText(self.player.total_torpedoes)
                    self.total_torpedoes_box.draw()

                    self.other.draw(screen)
                    pygame.display.flip()
                    pygame.time.set_timer(self.update_time, 25, 1)

                if event.type == self.end_event:
                    pygame.mixer.music.stop()
                    self.switch()  # переход на конечный экран
                    self.Win = Endgame()

    def spawn_mine(self):  # функция спавна мины
        mine_width = random.uniform(0.05, 0.3)
        Mine((random.uniform(0.05, 1 - mine_width) * width, 0.3 * height),
             (mine_width * width, random.uniform(0.05, 0.2) * height), self.mine_group, self.other)

    def spawn_enemy(self):  # функция спавна корабля
        Enemy(self.ship_group, self.other,
              ship_type=random.choice(
                  ['Канонерка', 'Эсминец', 'Линкор', 'Крейсер']))


class Mine(pygame.sprite.Sprite):  # класс мины
    def __init__(self, coordinates: tuple, mine_size: tuple, group, explosion_group):
        super().__init__(group)
        self.size = mine_size  # размер мины
        self.image = pygame.transform.scale(load_image('Mine.png'), (0.03 * width, 0.03 * width))
        self.rect = self.image.get_rect()  # квадрат спрайта
        self.rect.x, self.rect.y = coordinates
        self.explosion_group = explosion_group  # группа для анимации взрыва

    def update(self, player):
        self.rect.y += 0.005 * height  # перемещение мины

        if pygame.sprite.collide_mask(self, player):  # проверка удара
            player.get_damage(40)
            Explosion((self.rect.centerx, self.rect.y + self.rect.h), (0.1 * width, 0.1 * height),
                      self.explosion_group)  # взрыв и исчезновение
            self.kill()

        else:
            if self.rect.y >= height * 0.98:  # выход за границу
                self.kill()


class Explosion(pygame.sprite.Sprite):  # класс взрыва
    def __init__(self, center, size, group):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[0]  # первая картинка анимации
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  # кадр
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # время смены кадров в мс
        group.add(self)
        explosion.play()  # звук взрыва

    def update(self):
        now = pygame.time.get_ticks()  # обновление времени

        if now - self.last_update > self.frame_rate:
            self.last_update = now  # смена таймера и кадра
            self.frame += 1

            if self.frame == len(explosion_anim):
                self.kill()  # конец анимации

            else:
                center = self.rect.center
                self.image = pygame.transform.scale(explosion_anim[self.frame], self.size)
                self.rect = self.image.get_rect()  # смена картинки
                self.rect.center = center


class Cursor(pygame.sprite.Sprite):  # курсор игрока - вместо курсора мыши
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(load_image('cursor.png'), (0.05 * width, 0.05 * width))  # картинка
        pygame.mouse.set_visible(False)  # сделать мышь невидимой
        self.rect = self.image.get_rect()

    def update(self):
        if pygame.mouse.get_focused():  # если мышь в окне
            x1, y1 = pygame.mouse.get_pos()
            self.rect.x = x1  # перемещение в соответствии с мышью
            self.rect.y = y1

        else:
            self.rect.x = -100


class Endgame(Window):
    def __init__(self):
        super().__init__()
        self.Win = None
        self.running = True
        self.music_number = 0
        pygame.mouse.set_visible(True)
        self.background = pygame.transform.scale(load_image('Взрыв корабля.png'), screen.get_size())

        self.music_list = [int(j) for j in range(4)]
        random.shuffle(self.music_list)

        pygame.mixer.music.set_volume(music_volume / 3)

        pygame.mixer.music.load(f'Audio/Defeat{self.music_list[0]}.mp3')
        pygame.mixer.music.play()
        self.music_number += 1

        self.show()

    def show(self):
        while self.running:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(f'Audio/Defeat{self.music_list[self.music_number]}.mp3')
                pygame.mixer.music.play()
                self.music_number += 1
                self.music_number %= 4

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            screen.blit(self.background, (0, 0))
            pygame.display.flip()


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
