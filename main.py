import pygame
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
import pygame_widgets


def delete_widgets():
    pygame_widgets.WidgetHandler._widgets = []


class Window:
    def __init__(self):
        # width = pygame.display.Info().current_w
        # height = pygame.display.Info().current_h
        self.running = True

    def switch(self):
        self.running = False
        delete_widgets()


class MainWindow(Window):
    def __init__(self):
        super().__init__()
        self.Win = None
        self.picture = pygame.image.load('Главное меню.png')
        self.picture = pygame.transform.scale(self.picture, (width, height))
        self.picture_size = self.picture.get_size()
        font = pygame.font.Font(None, 150)
        text = font.render('Морская оборона', True, (255, 0, 0))
        self.draw_buttons()
        self.name = TextBox(screen,
                            round(width * 0.95) - 400,
                            round(height * 0.03),
                            400,
                            60,
                            colour='lightblue', text='username', fontSize=48, textHAlign='centre')
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            screen.blit(self.picture, (0, 0))
            screen.blit(text, (round(0.5 * width) - 450, round(0.1 * height)))
            pygame_widgets.update(events)
            pygame.display.flip()

    def end(self):
        self.switch()

    def to_options(self):
        self.switch()
        self.Win = Options()

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
        # Button(  # создание кнопки для настройки пользователя
        #     screen,
        #     round(width * 0.835),
        #     round(height * 0.03),
        #     round(width * 0.15),
        #     round(height * 0.05),
        #     colour='lightblue', text='username', onRelease=lambda: print('hello'), fontSize=36
        # )


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


if __name__ == '__main__':
    pygame.init()
    FPS = 60
    full_width, full_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('Audio/Background.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    clock.tick(FPS)
    MainWindow()
    # pygame.mixer.music.set_volume(0.5)
    # pygame.mixer.music.stop()
    # pygame.mixer.music.pause()
    # pygame.mixer.music.unpause()
