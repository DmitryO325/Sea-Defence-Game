import pygame

from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.progressbar import ProgressBar

import pygame_widgets
import sqlite3
import os
import math
import random


class Window:  # класс, являющийся базой для создания других окон
    def __init__(self):
        self.running = True


class Menu(Window):  # класс, являющийся общим для окон из меню
    def __init__(self):
        super().__init__()
        global player, playerID, width, height, music_volume, audio_volume, screen, size

        playerID = int(open("Data/last_player.txt").readline())
        player, width, height, music_volume, audio_volume, fps = cursor.execute(f'SELECT name, width, height, music, '
                                                                                f'sounds, FPS FROM Player '
                                                                                f'WHERE ID={playerID}').fetchone()

        size = width, height
        screen = pygame.display.set_mode(size)
        pygame.mixer.music.set_volume(music_volume)

        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, screen.get_size())


class MainWindow(Menu):  # класс главного меню
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

            screen.blit(text, (0.5 * width - text.get_width() // 2, round(0.05 * height)))
            pygame_widgets.update(events)
            pygame.display.flip()

    def end(self):  # метод выхода из игры
        self.switch()

    def to_options(self):  # метод, который отвечает за переход к настройкам
        self.switch()
        self.Win = Options()

    def to_top_players(self):  # метод, который отвечает за переход к топу игроков
        self.switch()
        self.Win = TopPlayers()

    def to_shipyard(self):  # метод, который отвечает за переход к верфи
        self.switch()
        self.Win = Shipyard()

    def to_survival(self):  # метод, который отвечает за переход к выживанию
        self.switch()
        self.Win = Battlefield()

    def to_name(self):  # метод, который отвечает за переход к окну выбора имени
        self.switch()
        self.Win = Name()

    def draw_buttons(self):  # метод, отрисовывающий кнопки
        button_titles = ('name', 'Выживание', 'Верфь', 'Топ игроков', 'Настройки', 'Выход')
        button_functions = (self.to_survival, self.to_shipyard,
                            self.to_top_players, self.to_options, self.end)

        for number_of_button in range(1, 6):  # создание кнопок для перехода в другие окна
            Button(
                screen,
                round(width * 0.3),
                round(height * (0.06 + number_of_button * 0.15)),
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
            colour='lightblue', text=player, onRelease=self.to_name, fontSize=36
        )


class Name(Menu):  # переход к окну "Имя"
    def __init__(self):
        super().__init__()
        self.Win = None
        self.is_change = False
        self.width_value = 0
        self.names_combobox = None
        self.name_box = None

        self.name_status = 'repeat'

        self.create_name = self.edit_name = self.remove_name = False

        self.players_data = tuple(cursor.execute('''SELECT * FROM Player''').fetchall())
        self.players = tuple(map(lambda x: x[1], self.players_data))

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
        self.names_combobox = Dropdown(  # кнопка выбора имени
            screen,
            round(width * 0.35),
            round(height * 0.1),
            round(width * 0.3),
            round(height * 0.05),
            name=player, choices=self.players, fontSize=54,
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

        Button(  # кнопка для удаления профиля
            screen,
            round(width * 0.35),
            round(height * 0.03),
            round(width * 0.3),
            round(height * 0.05),
            colour='red', text='Удалить профиль', textColour='yellow',
            fontSize=32, hoverColour='grey', pressedColour='darkgrey',
            onRelease=self.show_deleted_name
        )

    def show_new_name(self):  # появляется окно для ввода нового имени
        self.is_change = 'new'
        self.delete_name_field()

    def show_changed_name(self):  # появляется окно для изменения имени
        self.is_change = 'change'
        self.delete_name_field()

    def show_deleted_name(self):  # появляется окно для подтверждения удаления имени
        self.is_change = 'delete'
        self.delete_name_field()

    def to_menu(self):  # метод, позволяющий вернуться в главное окно
        self.switch()
        self.Win = MainWindow()

    def change_data(self):  # метод, который изменяет информацию в текстовом файле last_player.txt
        with open('Data/last_player.txt', 'r+') as file:
            try:
                if self.create_name:
                    index = len(self.players)
                    self.create_name = False

                elif self.edit_name:
                    index = playerID
                    self.edit_name = False

                elif self.remove_name:
                    if playerID <= len(self.players):
                        index = playerID

                    else:
                        index = playerID - 1

                else:
                    if self.names_combobox.getSelected() is not None:
                        index = self.players.index(self.names_combobox.getSelected()) + 1

                    else:
                        index = playerID

            except ValueError:
                pass

            file.writelines(str(index))

        self.to_menu()

    def draw_field(self):  # метод, показывающий/скрывающий поля для ввода
        if self.is_change in {'new', 'change'}:
            # кнопка подсказки пользователю, появляется поверх кнопок с надписями "Создать/редактировать профиль"
            Button(
                screen,
                round(width * (0.7 - self.width_value)),
                round(height * 0.1),
                round(width * 0.2),
                round(height * 0.05),
                colour='yellow', text='Введите имя' if self.is_change == 'new' else 'Измените имя',
                textColour='red', fontSize=32, hoverColour='grey', pressedColour='darkgrey'
            )

            self.name_box = TextBox(  # текстовое поле для создания/изменения профиля
                screen,
                round(width * (0.7 - self.width_value)),
                round(height * 0.18),
                round(width * 0.2),
                round(height * 0.05),
                fontSize=32, colour='grey', hoverColour='yellow', pressedColour='red'
            )

            Button(  # кнопка подтверждения изменений
                screen,
                round(width * (0.7 - self.width_value)),
                round(height * 0.26),
                round(width * 0.2),
                round(height * 0.05),
                colour='blue', text='Создать' if self.is_change == 'new' else 'Изменить', textColour='yellow',
                fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
                onRelease=self.new_name if self.is_change == 'new' else self.change_name
            )

            Button(  # кнопка отмены изменений
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

        else:
            Button(  # кнопка удаления профиля
                screen,
                round(width * 0.07),
                round(height * 0.83),
                round(width * 0.26),
                round(height * 0.05),
                colour='blue', text=f'Удалить {self.players[playerID - 1]}', textColour='yellow',
                fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
                onRelease=self.delete_name
            )

            Button(  # кнопка отмены удаления
                screen,
                round(width * 0.07),
                round(height * 0.9),
                round(width * 0.26),
                round(height * 0.05),
                colour='blue', text='Отмена', textColour='yellow',
                fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
                onRelease=self.delete_name_field
            )

    def name_is_occupied(self, status):  # метод, сообщающий об ошибке при создании/изменении профиля
        Button(
            screen,
            round(width * 0.7) if status == 'new' else round(width * 0.1),
            round(height * 0.1),
            round(width * 0.2),
            round(height * 0.05),
            colour='yellow', text='Это имя занято!' if self.name_status == 'repeat' else 'Пустое имя!',
            textColour='red', fontSize=32, hoverColour='grey', pressedColour='darkgrey'
        )

        self.name_status = 'repeat'

    def delete_name_field(self):  # метод, скрывающий ненужные элементы
        delete_widgets()
        self.draw_buttons()

    def update_data(self):  # метод, обновляющий информацию в базе данных
        self.players_data = tuple(cursor.execute('''SELECT * FROM Player''').fetchall())
        self.players = tuple(map(lambda x: x[1], self.players_data))

    def new_name(self):  # метод, добавляющий новое имя в базу данных
        try:
            if not self.name_box.getText():
                self.name_status = 'empty'
                raise sqlite3.IntegrityError

            cursor.execute(f'''INSERT INTO Player(
            Name, Width, Height, FPS, Money, Music, Sounds, Score) VALUES 
            ('{self.name_box.getText()}', {full_width}, {full_height}, 240, 0, 1, 1, 0)''')

            cursor.execute(f'''INSERT INTO Ship(
                        HP, Ammo, Speed, Reload) VALUES (100, 2, 2, 1700)''')

            connection.commit()
            self.update_data()
            self.delete_name_field()

            self.create_name = True
            self.change_data()

        except sqlite3.IntegrityError:
            self.name_is_occupied('new')

    def change_name(self):  # метод, изменяющий информацию о профиле в базе данных
        try:
            if not self.name_box.getText():
                self.name_status = 'empty'
                raise sqlite3.IntegrityError

            cursor.execute(f'''UPDATE Player SET name = '{self.name_box.getText()}' 
                                    WHERE id = {playerID}''')
            connection.commit()

            self.update_data()
            self.delete_name_field()

            self.edit_name = True
            self.change_data()

        except sqlite3.IntegrityError:
            self.name_is_occupied('change')

    def delete_name(self):  # метод, удаляющий профиль из базы данных
        if len(self.players) == 1:
            Button(  # кнопка, сообщающая о невозможности удаления игрока из-за отсутствия других профилей
                screen,
                round(width * 0.35),
                round(height * 0.03),
                round(width * 0.3),
                round(height * 0.05),
                colour='red', text='Невозможно, так как больше нет аккаунтов!', textColour='yellow',
                fontSize=32, hoverColour='grey', pressedColour='darkgrey',
                onRelease=self.show_deleted_name
            )

        else:
            cursor.execute(f'''DELETE FROM Player WHERE id = {playerID}''')
            connection.commit()
            self.update_data()

            cursor.execute(f'''DELETE FROM Ship WHERE id = {playerID}''')
            connection.commit()
            self.update_data()

            for name_id in range(1, len(self.players) + 1):
                old_id = self.players_data[name_id - 1][0]

                cursor.execute(f'''UPDATE Player SET id = {name_id} 
                                   WHERE Name = "{self.players[name_id - 1]}"''')

                cursor.execute(f'''UPDATE Ship SET id = {name_id}
                                   WHERE id = {old_id}''')

            connection.commit()
            self.update_data()

            self.remove_name = True
            self.change_data()


class Options(Menu):  # переход к окну "Имя"
    def __init__(self):
        global FPS

        super().__init__()
        self.Win = None

        self.combobox2 = Dropdown(screen, round(0.2 * width) + 200, round(0.5 * height), round(width * 0.3),
                                  50, name='Максимальный FPS',  # настройка частоты кадров
                                  choices=['480', '360', '240', '120', '60'],
                                  borderRadius=3, colour='grey', fontSize=50,
                                  direction='down', textHAlign='centre')

            if self.combobox2.getSelected():
                FPS = int(self.combobox2.getSelected())
                cursor.execute(f'UPDATE Player SET FPS={FPS}')

    def update_sliders(self):  # метод, обновляющий ползунки и данные о звуках
        self.music_value = self.music_slider.getValue()
        self.music_box.setText(str(round(100 * self.music_value)))
        pygame.mixer.music.set_volume(self.music_value)

        self.sounds_value = self.sound_slider.getValue()
        self.sound_box.setText(str(round(100 * self.sounds_value)))


class Shipyard(Menu):  # переход к окну "Верфь"
    def __init__(self):
        super().__init__()

    def draw_widgets(self):  # метод, отрисовывающий кнопки
        self.info = (
            (self.upgrade_health, self.health / 500, 'Броня',
             {100: 1000, 200: 2000, 300: 4000, 400: 8000, 500: 'max'}),

            (self.upgrade_speed, (self.speed - 2) / 2, 'Скорость',
             {2: 1000, 3: 2000, 4: 4000, 5: 8000, 6: 'max'}),

            (self.upgrade_gun, (self.ammo - 1) / 5, 'Боезапас',
             {2: 1000, 3: 2000, 4: 4000, 5: 8000, 6: 'max'}),

            (self.upgrade_reload, 1 - (self.reload - 700) / 1250, 'Перезарядка',
             {1700: 1000, 1450: 2000, 1200: 4000, 950: 8000, 700: 'max'})
        )

        # эти прогресс-бары почему-то работают некорректно в циклах... приходится извращаться
        # прогресс-бары, показывающие уровень прокачки определённых характеристик
        ProgressBar(screen, 0.27 * width, 0.03 * height + 0.18 * height * (0 + 1),
                    0.5 * width, 0.04 * height, progress=lambda: self.info[0][1],
                    completedColour='green', incompletedColour='grey')

        ProgressBar(screen, 0.27 * width, 0.03 * height + 0.18 * height * (1 + 1),
                    0.5 * width, 0.04 * height, progress=lambda: self.info[1][1],
                    completedColour='green', incompletedColour='grey')

        ProgressBar(screen, 0.27 * width, 0.03 * height + 0.18 * height * (2 + 1),
                    0.5 * width, 0.04 * height, progress=lambda: self.info[2][1],
                    completedColour='green', incompletedColour='grey')

        ProgressBar(screen, 0.27 * width, 0.03 * height + 0.18 * height * (3 + 1),
                    0.5 * width, 0.04 * height, progress=lambda: self.info[3][1],
                    completedColour='green', incompletedColour='grey')

        for h in range(4):  # кнопки улучшения характеристик
            Button(screen, 0.8 * width, 0.18 * height * (h + 1), 0.15 * width, 0.1 * height, colour='blue',
                   text=f'Улучшить: {self.info[h][3][self.data[h]]}', textColour='gold',
                   fontSize=50, radius=10, borderThickness=3, borderColour='silver',
                   onClick=self.info[h][0], textHAlign='center', hoverColour='darkblue', hoverBorderColour='silver')

            Button(screen, 0.05 * width, 0.18 * height * (h + 1), 0.2 * width, 0.1 * height, colour='blue',
                   text=str(self.info[h][2]), textColour='gold',
                   fontSize=50, radius=10, borderThickness=3, borderColour='silver',
                   onClick=self.info[h][0], textHAlign='center').disable()

    def to_menu(self):
        self.switch()
        self.Win = MainWindow()


class Ship(pygame.sprite.Sprite):  # класс корабля (общий для игрока и противников)
    def __init__(self, group, explosion_group):
        super().__init__(group)

        self.health = 0  # количество здоровья
        self.speed = 0  # скорость корабля
        self.explosion_group = explosion_group


class Player(Ship):  # класс игрока
    def __init__(self, group, explosion_group):
        super().__init__(group, explosion_group)
        self.max_ammo, self.health, self.reload_time, self.speed = cursor.execute(f'SELECT Ammo, HP, Reload, '
                                                                                  f'Speed FROM SHIP WHERE '
                                                                                  f'ID={playerID}').fetchone()

        self.image = pygame.transform.scale(load_image('Player.png'), (width * 0.25, height * 0.25))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = round(0.375 * width), round(0.78 * height)

        self.left = False  # плывём влево
        self.right = False  # плывём вправо

        self.reloading = False  # перезарядка орудия
        self.torpedo_reloading = False  # перезарядка торпеды

        self.max_health = self.health  # для вывода количества оставшегося здоровья на шкале

        self.total_ammo = 100  # первичный арсенал
        self.total_torpedoes = 20

        self.health_bar = ProgressBar(screen, 0.4 * width, 0.08 * height, 0.3 * width, 0.02 * height,
                                      lambda: self.health / self.max_health,  # шкала здоровья
                                      completedColour='darkgreen', incompletedColour='red')

        self.start = pygame.time.get_ticks()  # начало перезарядки пушки
        self.torpedo_time = pygame.time.get_ticks()  # начало подготовки торпеды

        self.ammo = self.max_ammo  # количество снарядов в отсеке пушки
        self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                   lambda: self.ammo / self.max_ammo, completedColour='blue', incompletedColour='red')
        # шкала со снарядами пушки

        self.torpedo = 1  # торпеда готова к пуску
        self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.085, width * 0.2, height * 0.02,
                                       lambda: self.torpedo, completedColour='blue', incompletedColour='red')
        # шкала готовности торпеды

    def gun_shot(self, coordinates, group, explosion_group):  # функция выстрела из пушки
        gun.set_volume(audio_volume)
        gun.play()  # звук выстрела из пушки

        Bullet(round(self.rect.centerx), round(0.98 * self.rect.y), coordinates, group, explosion_group)
        # запуск снаряда

        self.ammo -= 1  # изменения в арсенале
        self.total_ammo -= 1

        if self.ammo == 0 and not self.total_ammo == 0:  # автоматическое начало перезарядки
            self.start_reloading()

    def start_reloading(self):
        self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                   lambda: (pygame.time.get_ticks() - self.start + self.ammo *
                                            self.reload_time) / (self.reload_time * self.max_ammo),
                                   completedColour='yellow', incompletedColour='red')
        # обновление шкалы пушки

        self.start = pygame.time.get_ticks()  # замер времени
        self.reloading = True  # начало перезарядки

    def reload(self):
        if self.total_ammo >= self.max_ammo:
            self.ammo = self.max_ammo  # восполнение боекомплекта

        else:
            self.ammo = self.total_ammo

    def start_torpedo_reload(self):
        self.torpedo_time = pygame.time.get_ticks()
        self.torpedo_reloading = True

        self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.085, width * 0.2, height * 0.02,
                                       lambda: (pygame.time.get_ticks() - self.torpedo_time) / 3000,
                                       completedColour='yellow', incompletedColour='red')

    def torpedo_reload(self):
        if self.total_torpedoes:  # торпеда готова
            self.torpedo = 1

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
            self.rect.x += self.speed

            if self.rect.x + self.rect.w > width:
                self.rect.x = width - self.rect.w

        if self.left:
            self.rect.x -= self.speed

            if self.rect.x < 0:
                self.rect.x = 0

        if pygame.time.get_ticks() - self.start >= self.reload_time * min((self.max_ammo - self.ammo),
                                                                          self.total_ammo) and self.reloading:
            self.reloading = False  # завершение зарядки орудия
            self.reload()

            self.gun_bar = ProgressBar(screen, width * 0.05, height * 0.03, width * 0.2, height * 0.02,
                                       lambda: self.ammo / self.max_ammo,
                                       completedColour='blue', incompletedColour='red')
            # обновление шкалы пушки

        if pygame.time.get_ticks() - self.torpedo_time >= 3000 and self.torpedo_reloading:
            self.torpedo_reloading = False
            self.torpedo_reload()  # завершение подготовки торпеды

            self.torpedo_bar = ProgressBar(screen, width * 0.05, height * 0.085, width * 0.2, height * 0.02,
                                           lambda: 1, completedColour='blue', incompletedColour='red')

        self.gun_bar.draw()
        self.torpedo_bar.draw()  # прорисовка шкалы здоровья, пушки, торпеды
        self.health_bar.draw()

        if not self.reloading and self.ammo == 0 and self.total_ammo > 0:
            self.start_reloading()

        if not self.torpedo_reloading and self.torpedo == 0 and self.total_torpedoes > 0:
            self.start_torpedo_reload()

        if self.health <= 0:
            self.explode()


class Enemy(Ship):  # класс врага
    params = {'Канонерка': (50, 2.0, 100), 'Эсминец': (100, 1.5, 150),
              'Линкор': (200, 1, 200), 'Крейсер': (300, 1, 300)}

    def __init__(self, group, explosion_group, ship_type):
        super().__init__(group, explosion_group)

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

        if self.health <= 0:
            global score
            score += self.points

            self.kill()

            self.event = random.randint(1, 100)  # бонус

            if 1 <= self.event <= 70:
                Bonuses(self.rect.centerx, self.rect.y + self.rect.w * 0.5,
                        bonus_group, self.event)


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
        global score

        super().__init__()
        self.music_number = 0  # номер саундтрека

        self.Win = None

        self.music_list = [int(j) for j in range(18)]
        random.shuffle(self.music_list)  # перемешка музыки

        pygame.mixer.music.set_volume(music_volume / 3)  # музыка тише звуков (при максимумах)

        pygame.mixer.music.load(f'Audio/Battle{self.music_list[0]}.mp3')
        pygame.mixer.music.play()  # начало проигрывания трека

        self.music_number += 1
        self.start_time = pygame.time.get_ticks()  # начало таймера игры


        self.torpedo_image = pygame.transform.scale(load_image('old_torpedo.png'), (width * 0.02, height * 0.06))
        self.torpedo_image = pygame.transform.rotate(self.torpedo_image, 270)  # изображение торпеды

        self.ammo_image = pygame.transform.scale(load_image('Bullet.png'), (width * 0.008, height * 0.03))
        self.ammo_image = pygame.transform.rotate(self.ammo_image, 270)  # изображение снаряда

        self.score = TextBox(screen, 0.85 * width, 0.07 * height, 0.06 * width, 0.05 * height,  # счёт
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)

        self.timer = TextBox(screen, 0.85 * width, 0.01 * height, 0.06 * width, 0.05 * height,
                             placeholderText=0, colour='grey', textColour='black', fontSize=36)  # время игры

        self.total_ammo_box = TextBox(screen, width * 0.27, height * 0.01, width * 0.03, height * 0.05,
                                      placeholderText=0, colour='grey', textColour='black', fontSize=24)
        # количество снарядов

        self.total_torpedoes_box = TextBox(screen, width * 0.27, height * 0.07, width * 0.03, height * 0.05,
                                           placeholderText=0, colour='grey', textColour='black', fontSize=24)
        # количество торпед

        self.health_box = TextBox(screen, width * 0.525, height * 0.02, width * 0.05, height * 0.05,
                                  placeholderText=0, colour='grey', textColour='black', fontSize=24)
        # здоровье


        while self.running:
            clock.tick(FPS)

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(f'Audio/Battle{self.music_list[self.music_number]}.mp3')
                pygame.mixer.music.play()

                self.music_number += 1  # смена трека при завершении
                self.music_number %= 18

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    all_keys = pygame.key.get_pressed()

                    if all_keys[pygame.K_p] and (all_keys[pygame.K_LCTRL] or all_keys[pygame.K_RCTRL]):
                        self.end_of_game()

                if event.type == pygame.KEYUP:
                    if (event.key in {pygame.K_SPACE, pygame.K_w, pygame.K_UP} and
                            0 < self.player.ammo < self.player.max_ammo and not self.player.reloading
                            and not self.player.total_ammo == 0):
                        self.player.start_reloading()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.button == 2 and 0 < self.player.ammo < self.player.max_ammo and
                            not self.player.reloading and not self.player.total_ammo == 0):
                        self.player.start_reloading()

                if self.player.total_ammo == 0 and self.player.total_torpedoes == 0 and len(self.bonus_group) < 3:
                    Bonuses(random.uniform(0.1, 0.9) * width, 0.35 * height, self.bonus_group, random.randint(1, 41))
                    # если у игрока нет снарядов, приходит поддержка

                if event.type == self.update_time:
                    screen.blit(self.background, (0, 0))
                    screen.blit(self.torpedo_image, (width * 0.015, height * 0.075))
                    screen.blit(self.ammo_image, (width * 0.025, height * 0.03))

                    self.score.setText(score)
                    self.score.draw()

                    self.timer.setText(f"{(pygame.time.get_ticks() - self.start_time) // 1000 // 60}:"
                                       f"{str((pygame.time.get_ticks() - self.start_time) // 1000 % 60).zfill(2)}")
                    self.timer.draw()

                    self.total_ammo_box.setText(self.player.total_ammo)
                    self.total_ammo_box.draw()  # обновление и прорисовка виджетов

                    self.total_torpedoes_box.setText(self.player.total_torpedoes)
                    self.total_torpedoes_box.draw()

                    self.health_box.setText(f'{self.player.health}/{self.player.max_health}')
                    self.health_box.draw()

                    self.player.gun_bar.draw()
                    self.player.torpedo_bar.draw()  # прорисовка шкалы здоровья, пушки, торпеды
                    self.player.health_bar.draw()

                if event.type == self.end_event:
                    self.end_of_game()

    def end_of_game(self):  # метод, окончивающий игру
        pygame.mixer.music.stop()

        try:
            new_id = cursor.execute('SELECT ID FROM GAME').fetchall()[-1][0] + 1

        except IndexError:
            new_id = 0

        time = ''.join(self.timer.text)

        cursor.execute(f'INSERT INTO GAME VALUES ({new_id}, "{player}", {score}, "{time}")')
        cursor.execute(f'UPDATE Player SET Score=Score+{score}, Money=Money+{score} WHERE ID={playerID}')
        connection.commit()

        self.switch()  # переход на конечный экран
        self.Win = Endgame(''.join(self.timer.text))


class Cursor(pygame.sprite.Sprite):  # курсор игрока - вместо курсора мыши
    def update(self):
        if pygame.mouse.get_focused():  # если мышь в окне
            x1, y1 = pygame.mouse.get_pos()
            self.rect.x = x1 - 0.025 * width  # перемещение в соответствии с мышью
            self.rect.y = y1 - 0.025 * width

        else:
            self.rect.x = -100


class Endgame(Window):
    def __init__(self, time):
        super().__init__()
        self.Win = None

        self.running = True
        self.music_number = 0
        pygame.mouse.set_visible(True)

        self.background = pygame.transform.scale(load_image('Взрыв корабля.png'), screen.get_size())

        font = pygame.font.Font(None, 200)
        self.text1 = font.render(f'Ваш счёт: {score}', True, (150, 50, 0))
        self.text2 = font.render(f'Ваше время: {time}', True, (150, 50, 0))

        self.music_list = [int(j) for j in range(4)]
        random.shuffle(self.music_list)

        pygame.mixer.music.set_volume(music_volume)

        pygame.mixer.music.load(f'Audio/Defeat{self.music_list[0]}.mp3')
        pygame.mixer.music.play()
        self.music_number += 1

        self.draw_buttons()
        self.show()

    def draw_buttons(self):
        Button(  # кнопка "Переиграть"
            screen,
            round(width * 0.5),
            round(height * 0.85),
            round(width * 0.2),
            round(height * 0.1),
            colour='blue', text='Переиграть', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_survival
        )

        Button(  # кнопка "В меню"
            screen,
            round(width * 0.75),
            round(height * 0.85),
            round(width * 0.2),
            round(height * 0.1),
            colour='blue', text='В меню', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

    def to_menu(self):
        self.switch()

        pygame.mixer.music.load('Audio/Background.mp3')
        pygame.mixer.music.play(-1)

        self.Win = MainWindow()

    def to_survival(self):
        self.switch()
        self.Win = Battlefield()

    def show(self):
        while self.running:
            events = pygame.event.get()

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(f'Audio/Defeat{self.music_list[self.music_number]}.mp3')
                pygame.mixer.music.play()
                self.music_number += 1
                self.music_number %= 4

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            screen.blit(self.background, (0, 0))
            screen.blit(self.text1, (0.5 * width - self.text1.get_width() // 2, round(0.05 * height)))
            screen.blit(self.text2, (0.5 * width - self.text2.get_width() // 2,
                                     round(0.1 * height + self.text1.get_height())))

            pygame_widgets.update(events)
            pygame.display.flip()
