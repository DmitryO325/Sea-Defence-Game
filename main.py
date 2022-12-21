import pygame
from pygame_widgets.button import Button
import pygame_widgets


class Window:
    def __init__(self):
        pygame.init()

        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h

        self.size = self.width, self.height = 1600, 900
        self.screen = pygame.display.set_mode(self.size)

        self.running = True
        self.objects = {}

    def resize(self, x, y):
        self.width = x
        self.height = y

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


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.button_titles = ('name', 'survival', 'level_mode', 'shipyard', 'top_players', 'options', 'exit')

        self.picture = pygame.image.load('Главное меню.png')
        self.picture_size = self.picture.get_size()
        self.screen.blit(self.picture, self.picture_size)

    def position_buttons(self):
        # button = Button(self.screen, 100, 100, 300, 150, text='Тестирование кнопки', textColour='blue',
        #                 fontSize=30,
        #                 colour='red', borderThickness=10, pressedColour='yellow',
        #                 hoverColour='green')

        for number_of_button in range(1, 7):
            button = Button(
                self.screen,
                round(self.width * 0.2),
                round(self.height * (0.06 + number_of_button * 0.13 + 0.03)),
                round(self.width * 0.6),
                round(self.height * 0.1),
                colour='red'
            )

            self.objects[self.button_titles[number_of_button]] = button

        button = Button(
                self.screen,
                round(self.width * 0.885),
                round(self.height * 0.03),
                round(self.width * 0.1),
                round(self.height * 0.05),
                colour='blue'
            )

        self.objects[self.button_titles[0]] = button

    def show(self):
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


win = MainWindow()
win.position_buttons()
win.show()
