import sqlite3

import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import pygame_widgets


def delete_widgets():
    pygame_widgets.WidgetHandler._widgets = []


class Window:
    def __init__(self):
        # self.width = pygame.display.Info().current_w
        # self.height = pygame.display.Info().current_h

        self.size = self.width, self.height = 1920, 1080
        self.screen = pygame.display.set_mode(self.size)

        self.running = True
        self.objects = {}

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
            # pygame_widgets.update(events)
            # # for element in self.objects:
            # #     element.listen(events)
            # #     element.draw()

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
            button = Button(
                self.screen,
                round(self.width * 0.2),
                round(self.height * (0.06 + number_of_button * 0.13 + 0.03)),
                round(self.width * 0.6),
                round(self.height * 0.1),
                colour='yellow', text=self.button_titles[number_of_button], textColour='red',
                fontSize=60, radius=10, hoverColour='cyan', pressedColour='blue',
                onRelease=self.button_functions[number_of_button]
            )

            self.objects[self.button_titles[number_of_button]] = button

        button = Button(self.screen,
                        round(self.width * 0.885),
                        round(self.height * 0.03),
                        round(self.width * 0.1),
                        round(self.height * 0.05),
                        colour='green', text='Имя', onRelease=self.button_functions[0]
                        )

        self.objects[self.button_titles[0]] = button

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

            # # for element in self.objects:
            # #     element.listen(events)
            # #     element.draw()

    def to_options(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_top_players(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_shipyard(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_level_mode(self):
        self.switch()
        # self.Win = MainWindow2()

    def to_survival(self):
        self.switch()
        # self.Win = MainWindow2()

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

        connection = sqlite3.connect('Файлы базы данных/name.sqlite')
        cursor = connection.cursor()
        self.names = tuple(map(lambda x: x[0], cursor.execute('''SELECT name FROM data''').fetchall()))

        self.names_combobox = Dropdown(self.screen, round(0.4 * self.width), round(0.1 * self.height),
                                       round(0.2 * self.width), round(0.05 * self.height),
                                       name=self.names[0], choices=self.names, fontSize=54,
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
            round(self.height * (0.7 + 1 * 0.15)),
            round(self.width * 0.2),
            round(self.height * 0.1),
            colour='blue', text='В главное меню', textColour='yellow',
            fontSize=50, radius=10, hoverColour='darkblue', pressedColour='darkgrey',
            onRelease=self.to_menu
        )

    def to_menu(self):
        self.switch()
        self.Win = MainWindow()


if __name__ == '__main__':
    pygame.init()
    window = MainWindow()
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play()
