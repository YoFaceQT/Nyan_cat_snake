from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Все направления движения:
ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# Цвет фона - космос:
BOARD_BACKGROUND_COLOR = (1, 68, 121)

# Задний фон:
BACKGROUND_IMAGE = pygame.image.load('the_snake/images/background.png')

# Изображение головы змейки:
NYAN_CAT_IMG = pygame.image.load('the_snake/images/NyanCat.png')

# Изображение "Яблока":
APPLE_IMG = pygame.image.load('the_snake/images/bread.png')

# Изображение тела змейки:
BODY_IMG = pygame.image.load('the_snake/images/NyanCattail.png')

# Изображение хвоста змейки:
TAIL_IMG = pygame.image.load('the_snake/images/tail.png')

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Все классы игры.
class GameObject:
    """Родилельский класс (Игровой Объект)."""

    def __init__(self):
        """Инициализатор родительского класса."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод родительского класса, использован для отрисовки игровых \
        объектов, по умолчанию пустой."""
        pass


class Apple(GameObject):
    """Дочерний класс Яблоко."""

    def __init__(self):
        """Инициализатор дочернего класса Яблоко."""
        super().__init__()
        self.randomize_position()
        self.image = APPLE_IMG

    def randomize_position(self):
        """Метод выбора случайной позиции класса Яблоко."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод отрисовки класса Apple."""
        screen.blit(self.image, self.position)


class Snake(GameObject):
    """Дочерний класс Snake."""

    def __init__(self):
        """Атрибуты класса Snake."""
        super().__init__()
        self.reset()
        self.body_image = BODY_IMG
        self.head_image = NYAN_CAT_IMG

    def get_head_position(self):
        """Метод класса Snake возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод класса Snake обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_pos_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_pos_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_pos_x, new_pos_y)
        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Метод класса Snake сбрасывает змейку в начальное состояние."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(ALL_DIRECTIONS)
        self.next_direction = None
        self.last = None
        self.length = 1

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод отрисовки змейки на экране."""
        for position in self.positions[1:]:
            screen.blit(self.body_image, position)
        if self.direction == UP:
            head_img = pygame.transform.rotate(self.head_image, 90)
        elif self.direction == DOWN:
            head_img = pygame.transform.rotate(self.head_image, 270)
        elif self.direction == LEFT:
            head_img = pygame.transform.flip(self.head_image, True, False)
        elif self.direction == RIGHT:
            head_img = pygame.transform.rotate(self.head_image, 0)
        screen.blit(head_img, self.positions[0])
        if self.last:
            screen.blit(TAIL_IMG, self.positions[-1])


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
