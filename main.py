import sqlite3

import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import pygame_widgets


def delete_widgets():
    pygame_widgets.WidgetHandler._widgets = []


class Window:
    def __init__(self):
        with open('preferences.txt') as file:
            self.file_data = file.readlines()
            self.size = self.width, self.height = \
                tuple(map(int, self.file_data[1][self.file_data[1].find('=') + 2:].split('x')))
            self.screen = pygame.display.set_mode(self.size)

            self.max_resolution = pygame.display.Info().current_w, pygame.display.Info().current_h

            self.FPS = int(self.file_data[2][self.file_data[2].find('=') + 2:])
            self.clock = pygame.time.Clock()
            self.clock.tick(self.FPS)

            self.music_volume = int(self.file_data[3][self.file_data[3].find('=') + 2:])
            pygame.mixer.music.set_volume(self.music_volume / 100)

        self.running = True

    def resize(self, x, y):
        self.size = self.width, self.height = x, y
        self.screen = pygame.display.set_mode(self.size)

    def switch(self):
        self.running = False
        delete_widgets()

    def show(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()

    def hide(self):
        self.running = False


class Menu(Window):
    def __init__(self):
        super().__init__()
        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, self.screen.get_size())

        self.connection = sqlite3.connect('Файлы базы данных/name.sqlite')
        self.cursor = self.connection.cursor()

        self.names_data = tuple(self.cursor.execute('''SELECT * FROM data''').fetchall())
        self.names = tuple(map(lambda x: x[1], self.names_data))

        with open('preferences.txt') as file:
            self.file_data = file.readlines()
            self.name_id = int(self.file_data[0][7:])

        self.selected_name = self.names[self.name_id - 1]


class MainWindow(Menu):
    def __init__(self):
        super().__init__()
        self.Win = None

        self.button_titles = ('Имя', 'Выживание', 'Кампания', 'Верфь', 'Топ игроков', 'Настройки', 'Выход')
        self.button_functions = (self.to_name, self.to_survival, self.to_level_mode, self.to_shipyard,
                                 self.to_top_players, self.to_options, self.to_exit)

        self.show()

    def position_buttons(self):
        for number_of_button in range(1, 7):
            Button(
                self.screen,
                round(self.width * 0.2),
                round(self.height * (0.06 + number_of_button * 0.13 + 0.03)),
                round(self.width * 0.6),
                round(self.height * 0.1),
                colour='yellow', text=self.button_titles[number_of_button], textColour='red',
                fontSize=60, radius=10, hoverColour='cyan', pressedColour='blue',
                onRelease=self.button_functions[number_of_button]
            )

        Button(self.screen,
               round(self.width * 0.885),
               round(self.height * 0.03),
               round(self.width * 0.1),
               round(self.height * 0.05),
               colour='green', text=self.selected_name, fontSize=32,
               onRelease=self.button_functions[0]
               )

    def show(self):
        self.position_buttons()

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.picture, (0, 0))
            pygame_widgets.update(events)
            pygame.display.flip()

    def to_options(self):
        self.switch()
        self.Win = Options()

    def to_top_players(self):
        self.switch()

    def to_shipyard(self):
        self.switch()

    def to_level_mode(self):
        self.switch()

    def to_survival(self):
        self.switch()

    def to_name(self):
        self.switch()
        self.Win = Name()

    def to_exit(self):
        self.switch()


class Options(Menu):
    def __init__(self):
        super().__init__()
        self.Win = None

        with open('preferences.txt') as file:
            self.file_data = file.readlines()
            self.new_width, self.new_height = map(int, self.file_data[1][self.file_data[1].find('=') + 2:].split('x'))
            self.fps = int(self.file_data[2][self.file_data[2].find('=') + 2:])
            self.music_value = int(self.file_data[3][self.file_data[3].find('=') + 2:])
            self.sound_value = int(self.file_data[4][self.file_data[4].find('=') + 2:])

        self.music_box = TextBox(  # отображает громкость музыки
            self.screen,
            round(0.52 * self.width) + 200,
            round(0.2 * self.height) - 10, 60,
            50, fontSize=35
        )

        self.music_slider = Slider(  # ползунок громкости музыки
            self.screen,
            round(0.2 * self.width) + 200,
            round(0.2 * self.height),
            round(self.width * 0.3),
            30,
            colour='white', handleColour=pygame.Color('red'),
            max=100, min=0, step=1, initial=self.music_volume
        )

        self.sound_box = TextBox(  # отображает громкость звуков
            self.screen,
            round(0.52 * self.width) + 200,
            round(0.3 * self.height) - 10,
            60,
            50,
            fontSize=35
        )

        self.sound_slider = Slider(  # ползунок громкости звуков
            self.screen,
            round(0.2 * self.width) + 200,
            round(0.3 * self.height),
            round(0.3 * self.width),
            30,
            colour='white', handleColour=pygame.Color('red'),
            max=100, min=0, step=1, initial=self.sound_value
        )

        self.combobox1 = Dropdown(
            self.screen,
            round(0.2 * self.width) + 200,
            round(0.4 * self.height),
            round(0.3 * self.width),
            50,
            name='Разрешение экрана',  # настройка разрешения экрана
            choices=['Полный экран', '1280 x 720', '1920 x 1080',
                     '2048 x 1152', '3840 x 2160'],
            borderRadius=3, colour='grey', fontSize=50,
            values=[self.max_resolution,
                    (1280, 720), (1920, 1080), (2048, 1152), (3840, 2160)],
            direction='down', textHAlign='centre'
        )

        self.combobox2 = Dropdown(
            self.screen,
            round(0.2 * self.width) + 200,
            round(0.5 * self.height),
            round(0.3 * self.width),
            50, name='Максимальный FPS',  # настройка частоты кадров
            choices=['120', '100', '80', '60', '40'],
            borderRadius=3, colour='grey', fontSize=50,
            direction='down', textHAlign='centre'
        )

        self.draw_buttons()

        self.header_font = pygame.font.Font(None, 150)
        self.header_text = self.header_font.render('Настройки', True, (255, 0, 0))

        self.functions_texts = ['Музыка', 'Звуковые эффекты', 'Разрешение экрана', 'Частота кадров']
        self.functions_font = pygame.font.Font(None, 60)

        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, (self.width, self.height))

        self.show()

    def show(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.update_sliders()

            if self.combobox1.getSelected():
                self.new_width, self.new_height = self.combobox1.getSelected()

            if self.combobox2.getSelected():
                self.fps = int(self.combobox2.getSelected())

            self.screen.blit(self.picture, (0, 0))
            self.screen.blit(self.header_text, (round(0.4 * self.width), round(0.05 * self.height)))

            for num in range(len(self.functions_texts)):
                function_text = self.functions_font.render(self.functions_texts[num], True, (255, 0, 0))
                self.screen.blit(function_text, (round(0.01 * self.width), round((0.2 + num / 10) * self.height)))

            pygame_widgets.update(events)
            pygame.display.flip()

    def update_sliders(self):
        self.music_value = self.music_slider.getValue()
        self.music_box.setText(str(self.music_value))
        pygame.mixer.music.set_volume(self.music_value / 100)



        self.sound_value = self.sound_slider.getValue()
        self.sound_box.setText(str(self.sound_value))

    def draw_buttons(self):
        Button(
            self.screen,
            round(self.width * 0.75),
            round(self.height * (0.7 + 1 * 0.15)),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='blue', text='ОК', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

    def to_menu(self):
        with open('preferences.txt', 'r+') as file:
            self.file_data[1] = f'resolution = {self.new_width}x{self.new_height}\n'
            self.file_data[2] = f'FPS = {self.fps}\n'
            self.file_data[3] = f'music_volume = {self.music_value}\n'
            self.file_data[4] = f'sound_volume = {self.sound_value}\n'

            file.writelines(self.file_data)

            delete_widgets()

        self.switch()
        self.Win = MainWindow()


class TopPlayers(Menu):
    pass


class Shipyard(Menu):
    pass


class Name(Menu):  # переход к окну "Имя"
    def __init__(self):
        super().__init__()
        self.Win = None
        self.is_change = False
        self.width_value = 0
        self.new_name_status = 'repeat'
        self.create_name = False

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

            self.screen.blit(self.picture, (0, 0))
            pygame_widgets.update(events)
            pygame.display.flip()

    def draw_buttons(self):
        self.names_combobox = Dropdown(
            self.screen,
            round(0.35 * self.width),
            round(0.1 * self.height),
            round(0.3 * self.width),
            round(0.05 * self.height),
            name=self.selected_name, choices=self.names, fontSize=54,
            colour='green', hoverColour='yellow', pressedColour='red'
        )

        Button(  # кнопка "В меню без сохранения информации"
            self.screen,
            round(self.width * 0.75),
            round(self.height * 0.85),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='blue', text='Отмена', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

        Button(  # кнопка "Сохранить и вернуться в меню"
            self.screen,
            round(self.width * 0.53),
            round(self.height * 0.85),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='green', text='ОК', textColour='red',
            fontSize=50, radius=10, hoverColour='lightgreen', pressedColour='darkgrey',
            onRelease=self.change_data
        )

        Button(  # кнопка для создания нового профиля
            self.screen,
            round(self.width * 0.7),
            round(self.height * 0.1),
            round(self.width * 0.2),
            round(self.height * 0.05),
            colour='yellow', text='Создать профиль', textColour='red',
            fontSize=32, hoverColour='grey', pressedColour='darkgrey',
            onRelease=self.show_new_name
        )

        Button(  # кнопка для редактирования профиля
            self.screen,
            round(self.width * 0.1),
            round(self.height * 0.1),
            round(self.width * 0.2),
            round(self.height * 0.05),
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
                if self.create_name:
                    self.file_data[0] = f'name = {self.name_id + 1}\n'
                    self.create_name = False

                else:
                    self.file_data[0] = f'name = {self.names.index(self.names_combobox.getSelected()) + 1}\n'

            except ValueError:
                pass

            file.writelines(self.file_data)

        self.to_menu()

    def draw_field(self):
        Button(
            self.screen,
            round(self.width * (0.7 - self.width_value)),
            round(self.height * 0.1),
            round(self.width * 0.2),
            round(self.height * 0.05),
            colour='yellow', text='Введите имя' if self.is_change == 'new' else 'Измените имя',
            textColour='red', fontSize=32, hoverColour='grey', pressedColour='darkgrey'
        )

        self.name_box = TextBox(
            self.screen,
            round(self.width * (0.7 - self.width_value)),
            round(self.height * 0.18),
            round(self.width * 0.2),
            round(self.height * 0.05),
            fontSize=32, colour='grey', hoverColour='yellow', pressedColour='red'
        )

        Button(
            self.screen,
            round(self.width * (0.7 - self.width_value)),
            round(self.height * 0.26),
            round(self.width * 0.2),
            round(self.height * 0.05),
            colour='blue', text='Создать' if self.is_change == 'new' else 'Изменить', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.new_name if self.is_change == 'new' else self.change_name
        )

        Button(
            self.screen,
            round(self.width * (0.7 - self.width_value)),
            round(self.height * 0.34),
            round(self.width * 0.2),
            round(self.height * 0.05),
            colour='blue', text='Отмена', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.delete_name_field
        )

        self.width_value = 0

    def name_is_occupied(self):
        Button(
            self.screen,
            round(self.width * 0.7),
            round(self.height * 0.1),
            round(self.width * 0.2),
            round(self.height * 0.05),
            colour='yellow', text='Это имя занято!' if self.new_name_status == 'repeat' else 'Пустое имя!',
            textColour='red', fontSize=32, hoverColour='grey', pressedColour='darkgrey'
        )

        self.new_name_status = 'repeat'

    def delete_name_field(self):
        delete_widgets()
        self.draw_buttons()

    def update_data(self):
        self.names_data = tuple(self.cursor.execute('''SELECT * FROM data''').fetchall())
        self.names = tuple(map(lambda x: x[1], self.names_data))

    def new_name(self):
        try:
            if not self.name_box.getText():
                self.new_name_status = 'empty'
                raise sqlite3.IntegrityError

            self.cursor.execute(f'''INSERT INTO data(name, level) VALUES ('{self.name_box.getText()}', 1)''')
            self.connection.commit()
            self.update_data()
            self.delete_name_field()

            self.name_id = len(self.names) - 1
            self.selected_name = self.name_box.getText()

            self.create_name = True
            self.change_data()

        except sqlite3.IntegrityError:
            self.name_is_occupied()

    def change_name(self):
        self.cursor.execute(f'''UPDATE data SET name = '{self.name_box.getText()}' WHERE id = {self.name_id}''')
        self.connection.commit()
        self.update_data()
        self.delete_name_field()


if __name__ == '__main__':
    with open('preferences.txt') as text_file:
        file_data = text_file.readlines()
        music_volume = int(file_data[3][file_data[3].find('=') + 2:])

    pygame.init()
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_volume / 100)

    window = MainWindow()
