import pygame
from pygame_widgets.button import Button
import pygame_widgets


class Window:
    def __init__(self):
        pygame.init()
        # width = pygame.display.Info().current_w
        # height = pygame.display.Info().current_h
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        self.running = True
        self.objects = []

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
            pygame_widgets.update(events)
            for element in self.objects:
                element.listen(events)
                element.draw()

    def hide(self):
        self.running = False


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        button = Button(self.screen, 100, 100, 300, 150, text='Тестирование кнопки', textColour=pygame.Color('blue'),
                        fontSize=30,
                        colour='red', borderThickness=10, pressedColour=pygame.Color('yellow'),
                        hoverColour=pygame.Color('green'))
        self.objects.append(button)


win = MainWindow()