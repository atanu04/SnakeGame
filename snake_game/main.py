import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND = (34, 78, 45)


class Apple:
    def __init__(self, parent_screen):
        self.image1 = pygame.image.load("resources/apple2.jpg").convert()
        self.image2 = pygame.image.load("resources/apple3.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
        self. p = 0

    def draw(self):

        if self.p % 2 == 0:
            self.parent_screen.blit(self.image1, (self.x, self.y))
        else:
            self.parent_screen.blit(self.image2, (self.x, self.y))

        pygame.display.flip()

    def move(self):
        self.p = random.randint(0, 100)
        self.x = random.randint(0, 15) * SIZE
        self.y = random.randint(0, 12) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block2.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill(BACKGROUND)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()


# def is_collision(x1, y1, x2, y2):
#    if x2 <= x1 <= x2 + SIZE:
#       if y2 <= y1 <= y2 + SIZE:
#           return True
#
#   return False


def is_collision_2(x1, y1, x2, y2):
    if x2 == x1:
        if y2 == y1:
            return True

    return False


def boundary_collision(x, y, direction):
    if direction == 'up' and y == -40:
        return True
    elif direction == 'down' and y == 600:
        return True
    elif direction == 'right' and x == 800:
        return True
    elif direction == 'left' and x == -40:
        return True
    else:
        return False


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.surface.fill(BACKGROUND)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.pause = False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if is_collision_2(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)

            self.snake.increase_length()
            self.apple.move()
        for i in range(3, self.snake.length):
            if is_collision_2(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                self.game_over()

        if boundary_collision(self.snake.x[0], self.snake.y[0], self.snake.direction):
            sound = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(sound)
            self.game_over()

    def game_over(self):
        self.surface.fill(BACKGROUND)
        font = pygame.font.SysFont('arial', 40, True)
        line0 = font.render('Game Over!!', True, (200, 200, 200))
        self.surface.blit(line0, (300, 100))
        line = font.render(f'Score: {(self.snake.length - 1) * 5}', True, (200, 200, 200))
        self.surface.blit(line, (300, 200))
        line2 = font.render('Restart: Enter', True, (200, 200, 200))
        self.surface.blit(line2, (300, 250))
        line3 = font.render('Exit: Escape', True, (200, 200, 200))
        self.surface.blit(line3, (300, 300))
        pygame.display.flip()
        self.pause = True
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('arial', 20, True)
        score = font.render(f'Score: {(self.snake.length - 1) * 5}', True, (255, 255, 255))
        self.surface.blit(score, (700, 10))

    def restart(self):
        self.surface.fill(BACKGROUND)
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        pygame.mixer.music.rewind()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        self.pause = False
                        self.restart()

                    if not self.pause:
                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()
                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()
                        if event.key == K_LEFT and self.snake.direction != 'right':
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            if not self.pause:
                self.play()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
