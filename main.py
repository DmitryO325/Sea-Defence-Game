import pygame
from pygame_widgets.button import Button
import pygame_widgets


class Window:
    def __init__(self):
        # width = pygame.display.Info().current_w
        # height = pygame.display.Info().current_h
        self.running = True
        self.objects = []


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.Win = None
        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, (width, height))
        self.picture_size = self.picture.get_size()
        self.button_titles = ('name', 'Выживание', 'Кампания', 'Верфь', 'Топ игроков', 'Настройки', 'Выход')
        self.button_functions = (self.to_survival, self.to_level_mode, self.to_shipyard,
                                 self.to_top_players, self.to_options, self.to_exit)
        for number_of_button in range(1, 7):  # создание кнопок для других окон
            Button(
                screen,
                round(width * 0.2),
                round(height * (0.06 + number_of_button * 0.13 + 0.03)),
                round(width * 0.6),
                round(height * 0.1),
                colour='yellow', text=self.button_titles[number_of_button], textColour='red',
                fontSize=60, radius=10, hoverColour='cyan', pressedColour='blue',
                onRelease=self.button_functions[number_of_button - 1]
            )
        Button(  # создание кнопки для настройки пользователя
            screen,
            round(width * 0.885),
            round(height * 0.03),
            round(width * 0.1),
            round(height * 0.05),
            colour='green', text='username'
        )
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            screen.blit(self.picture, (0, 0))
            pygame_widgets.update(events)
            for element in self.objects:
                element.listen(events)
                element.draw()
            pygame.display.flip()

    def to_exit(self):
        self.running = False

    def to_options(self):
        self.running = False
        # self.Win = MainWindow2()

    def to_top_players(self):
        self.running = False
        # self.Win = MainWindow2()

    def to_shipyard(self):
        self.running = False
        # self.Win = MainWindow2()

    def to_level_mode(self):
        self.running = False
        # self.Win = MainWindow2()

    def to_survival(self):
        self.running = False
        # self.Win = MainWindow2()


class MainWindow2(Window):
    def __init__(self):
        super().__init__()
        self.Win = None
        self.button = Button(screen, 100, 100, 300, 150, text='asdfasdf',
                             textColour=pygame.Color('blue'),
                             fontSize=30,
                             colour='red', borderThickness=10, pressedColour=pygame.Color('yellow'),
                             hoverColour=pygame.Color('green'))
        self.objects.append(self.button)
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if self.button.clicked:
                    self.new_window()
            pygame.display.flip()
            pygame_widgets.update(events)
            for element in self.objects:
                element.listen(events)
                element.draw()

    def new_window(self):
        self.running = False
        self.Win = MainWindow()


if __name__ == '__main__':
    pygame.init()
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play(-1)
    MainWindow()
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.stop()
    # pygame.mixer.music.pause()
    # pygame.mixer.music.unpause()
