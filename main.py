import os.path
import sys
from os import environ
from random import shuffle, choice
from string import ascii_uppercase

if "linux" in sys.platform:
    import pyperclip
else:
    import win32clipboard

# Скрываем приветствие от PyGame
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


import pygame
from pygame import Surface, Rect

NUMBER_OF_NUMBERS = 6
NUMBER_START_POINT = (250, 100)
OUTPUT_FIELD_COORDS = (120, 500)
NUMBER_DELTA = 100
DARK_GREEN = (0, 170, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (150, 150, 150)
FPS = 60


def copy_func(text):
    if "linux" in sys.platform:
        pyperclip.copy(text)
    else:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()


def keygen(s):
    if " " in s:
        return ""
    n1, n2 = list(s[:3]), list(s[3:])
    shuffle(n1)
    shuffle(n2)
    n1, n2 = "".join(n1), "".join(n2)

    ls = [choice(ascii_uppercase) for _ in range(4)]
    sm = str(int(n1)+int(n2)).rjust(4, "0")

    return f"{n1}{ls[0]}{ls[1]}-{n2}{ls[2]}{ls[3]}-{sm}"


class NumberContainer:
    def __init__(self, x, y, next_node=None, prev_node=None):
        image = pygame.image.load(os.path.join(os.curdir, "green_rectangle.png")).convert_alpha()
        image = pygame.transform.rotate(image, 180)
        image = pygame.transform.scale(image, (80, 100))

        self.image = image
        self.font = pygame.font.SysFont('Comic Sans MS', 140)
        self.text = " "
        self.enable = False
        self.tick = 0

        self.x = x
        self.y = y

        self.next = next_node
        self.prev = prev_node

    def write(self, event):
        if event.key == pygame.K_LEFT:
            if self.prev is not None:
                self.enable = False
                self.prev.enable = True
        elif event.key == pygame.K_RIGHT:
            if self.next is not None:
                self.enable = False
                self.next.enable = True
        key = event.unicode
        if key.isdigit() and len(key) == 1:
            self.text = key
            if self.next is not None:
                self.enable = False
                self.next.enable = True
        elif key.isspace() and key not in "\n\r":
            self.text = " "
        elif key == "\b":
            self.text = " "
            if self.prev is not None:
                self.enable = False
                self.prev.enable = True

    def draw(self, screen: Surface):
        self.tick = (self.tick + 1) % 60
        screen.blit(self.image, (self.x, self.y))

        text = self.font.render(self.text, False, DARK_GREEN)
        screen.blit(text, (self.x + 15, self.y + 10))

        if self.enable and self.tick < 30:
            pygame.draw.line(screen, DARK_GREEN, (self.x + 15, self.y + 85), (self.x + 65, self.y + 85), 5)


def main():
    pygame.init()

    pygame.display.set_caption("KeyGen v1.0")
    screen = pygame.display.set_mode((1366, 768))

    clock = pygame.time.Clock()

    background = pygame.image.load(os.path.join(os.curdir, "bg_pic.png"))
    background_rect = background.get_rect()

    darkness = pygame.Surface((1366, 768), pygame.SRCALPHA)
    darkness_rect = darkness.get_rect()

    darkness.set_alpha(128)
    darkness.fill((0, 0, 0))

    copy = pygame.image.load(os.path.join(os.curdir, "copy.png"))
    copy = pygame.transform.scale(copy, (80, 80))
    font = pygame.font.SysFont('Comic Sans MS', 140)
    copy_rect = Rect(OUTPUT_FIELD_COORDS[0] + 1010, OUTPUT_FIELD_COORDS[1] + 10, 80, 80)

    containers = []
    for i in range(1, NUMBER_OF_NUMBERS + 1):
        containers.append(NumberContainer(
            NUMBER_START_POINT[0] + NUMBER_DELTA * i,
            NUMBER_START_POINT[1]
        ))
    for i in range(1, NUMBER_OF_NUMBERS):
        containers[i].prev = containers[i - 1]
    for i in range(NUMBER_OF_NUMBERS - 1):
        containers[i].next = containers[i + 1]

    containers[0].enable = True

    answer = ""

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for container in containers:
                    if container.enable:
                        container.write(event)
                        break
                if event.key == pygame.K_RETURN:
                    answer = keygen("".join([i.text for i in containers]))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                if copy_rect.collidepoint(event.pos):
                    copy_func(answer)

        screen.blit(background, background_rect)
        screen.blit(darkness, darkness_rect)

        for container in containers:
            container.draw(screen)

        pygame.draw.rect(screen, GRAY, (*OUTPUT_FIELD_COORDS, 1100, 100))
        text = font.render(answer, False, DARK_GRAY)
        screen.blit(text, (OUTPUT_FIELD_COORDS[0] + 10, OUTPUT_FIELD_COORDS[1] + 10))
        screen.blit(copy, (OUTPUT_FIELD_COORDS[0] + 1010, OUTPUT_FIELD_COORDS[1] + 10))

        pygame.display.flip()


if __name__ == '__main__':
    main()
