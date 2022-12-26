import sqlite3

import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import pygame_widgets


def delete_widgets():
    pygame_widgets.WidgetHandler._widgets = []


class Window:
    def __init__(self):
        self.size = self.width, self.height = 1600, 900
        self.screen = pygame.display.set_mode(self.size)

        self.running = True

    def resize(self, x, y):
        self.width = x
        self.height = y

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
               colour='green', text='Имя', onRelease=self.button_functions[0]
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
    pass


class TopPlayers(Menu):
    pass


class Shipyard(Menu):
    pass


class Name(Menu):
    def __init__(self):
        super().__init__()
        self.Win = None

        self.connection = sqlite3.connect('Файлы базы данных/name.sqlite')
        self.cursor = self.connection.cursor()
        self.names_data = tuple(self.cursor.execute('''SELECT * FROM data''').fetchall())
        self.names = tuple(map(lambda x: x[1], self.names_data))
        self.change = False

        with open('preferences.txt') as file:
            self.file_data = file.readlines()
            name_id = int(self.file_data[0][7:])

        self.names_combobox = Dropdown(self.screen, round(0.4 * self.width), round(0.1 * self.height),
                                       round(0.2 * self.width), round(0.05 * self.height),
                                       name=self.names[name_id - 1], choices=self.names, fontSize=54,
                                       colour='green', hoverColour='yellow', pressedColour='red')

        self.draw_buttons()
        self.show()

    def show(self):
        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.picture, (0, 0))
            pygame_widgets.update(events)
            pygame.display.flip()

    def draw_buttons(self):
        Button(
            self.screen,
            round(self.width * 0.75),
            round(self.height * 0.85),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='blue', text='Отмена', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

        Button(
            self.screen,
            round(self.width * 0.53),
            round(self.height * 0.85),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='green', text='ОК', textColour='red',
            fontSize=50, radius=10, hoverColour='lightgreen', pressedColour='darkgrey',
            onRelease=self.change_data
        )

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


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play()
    window = MainWindow()
