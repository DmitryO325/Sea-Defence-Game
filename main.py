import pygame
from pygame_widgets.button import Button


class Window:
    def __init__(self):
        pygame.init()
        # width = pygame.display.Info().current_w
        # height = pygame.display.Info().current_h
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

    def resize(self, x, y):
        self.width = x
        self.height = y

    def show(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
        pygame.quit()

    def hide(self):
        self.running = False


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        button = Button(self.screen, 100, 100, 300, 150, text='Тестирование кнопки', textColour=pygame.Color('blue'),
                        fontSize=30,
                        colour='red', borderThickness=10, pressedColour=pygame.Color('yellow'),
                        hoverColour=pygame.Color('green'))
        self.show()


win = MainWindow()
