import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.init()
win = pygame.display.set_mode((600, 600))
button = Button(win, 100, 100, 300, 150, text='Тестирование кнопки', textColour=pygame.Color('blue'), fontSize=30,
                colour='red', borderThickness=10, pressedColour=pygame.Color('yellow'),
                hoverColour=pygame.Color('green'))
# неплохо, есть много прикольных моментов. Единственное, не смог найти border-radius
run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        if button.clicked:
            print('hello')  # работает

    win.fill((255, 255, 255))

    # Now
    pygame_widgets.update(events)

    # Instead of
    button.listen(events)  # делает кнопку активной (?)
    button.draw()  # прорисовка кнопки

    pygame.display.update()
