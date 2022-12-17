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
        self.button = Button(screen, 100, 100, 300, 150, text='Тестирование кнопки',
                             textColour=pygame.Color('blue'),
                             fontSize=30,
                             colour='red', borderThickness=10, pressedColour='yellow',
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
        self.Win = MainWindow2()


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
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    MainWindow()
