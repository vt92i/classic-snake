import pygame, random, time, os


class Game():
    def __init__(self):
        self._Settings = self.Settings()
        self._Snake = self.Object().Snake()
        self._Food = self.Object().Food(self._Snake)

    class Settings():
        def __init__(self):
            self.game_title = "Classic Snake"
            self.fps = 14
            self.screen = {
                "width": 1024,
                "height": 640
            }
            self.grid = {
                "size": 32,
                "width": self.screen["width"] // 32,
                "height": self.screen["height"] // 32
            }
            self.sfx = {
                "food_eaten": os.path.join("assets/sfx", "food_eaten.oga"),
                "snake_dies": os.path.join("assets/sfx", "snake_dies.oga"),
                "start_game": os.path.join("assets/sfx", "start_game.oga"),
                "timer": os.path.join("assets/sfx", "timer.oga")
            }

        def handle_control(self, snake):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.turn(snake.movement_set["up"])
                    elif event.key == pygame.K_DOWN:
                        snake.turn(snake.movement_set["down"])
                    elif event.key == pygame.K_LEFT:
                        snake.turn(snake.movement_set["left"])
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(snake.movement_set["right"])

    class Object():
        class Utils():
            class Menu():
                pass

            class Messages():
                pass

        class Snake():
            def __init__(self):
                self._Settings = Game.Settings()

                self.screen_width, self.screen_height = self._Settings.screen["width"], self._Settings.screen["height"]
                self.gridsize, self.grid_width, self.grid_height = self._Settings.grid["size"], self._Settings.grid["width"], self._Settings.grid["height"]

                self.color = "#F3F7F0"
                self.length = 1
                self.lives = 3
                self.score = 0

                self.positions = [((self.screen_width // 2), (self.screen_height // 2))]

                self.movement_set = {
                    "up": (0, -1),
                    "down": (0, 1),
                    "left": (-1, 0),
                    "right": (1, 0),
                }

                self.direction = self.movement_set[random.choice([x for x in self.movement_set])]

            def get_head_position(self):
                return self.positions[0]

            def turn(self, point):
                if not (self.length > 1 and (point[0] * -1, point[1] * -1)) == self.direction:
                    self.direction = point

            def move(self, move):
                if move:
                    cur = self.get_head_position()
                    x, y = self.direction
                    new = (((cur[0] + (x * self.gridsize)) % self.screen_width), (cur[1] + (y * self.gridsize)) % self.screen_height)
                    if len(self.positions) > 2 and new in self.positions[2:]:
                        self.reset()
                    else:
                        self.positions.insert(0, new)
                        if len(self.positions) > self.length:
                            self.positions.pop()

            def reset(self):
                pygame.mixer.Sound.play(pygame.mixer.Sound(self._Settings.sfx["snake_dies"]))

                self.length = 1
                self.lives -= 1
                self.score = 0

                self.positions = [((self.screen_width / 2), (self.screen_height / 2))]
                self.direction = self.movement_set[random.choice([x for x in self.movement_set])]

            def draw(self, surface):
                for p in self.positions:
                    r = pygame.Rect((p[0], p[1]), (self.gridsize, self.gridsize))
                    pygame.draw.rect(surface, self.color, r)

        class Food():
            def __init__(self, target):
                self._Settings = Game.Settings()

                self.gridsize, self.grid_width, self.grid_height = self._Settings.grid["size"], self._Settings.grid["width"], self._Settings.grid["height"]

                self.color = "#E83F6F"
                self.position = (0, 0)
                self.target = target

                self.randomize_position()

            def randomize_position(self):
                new_position = (random.randint(0, self.grid_width - 1) * self.gridsize, random.randint(0, self.grid_height - 1) * self.gridsize)
                if new_position != self.position:
                    self.position = new_position
                else:
                    self.randomize_position()

            def draw(self, surface):
                if self.position not in self.target.positions:
                    r = pygame.Rect((self.position[0], self.position[1]), (self.gridsize, self.gridsize))
                    pygame.draw.rect(surface, self.color, r)
                else:
                    self.randomize_position()

    def drawGrid(self, surface):
        gridsize, grid_width, grid_height = self._Settings.grid["size"], self._Settings.grid["width"], self._Settings.grid["height"]

        grid_color = "#19323C"

        for x in range(0, grid_width):
            for y in range(0, grid_height):
                r = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, grid_color, r)

    def start(self):
        self.screen_width, self.screen_height = self._Settings.screen["width"], self._Settings.screen["height"]

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.display.set_caption(self._Settings.game_title)
        win = pygame.display.set_mode((self._Settings.screen["width"], self._Settings.screen["height"]))

        run = True
        clock = pygame.time.Clock()

        snake = self._Snake
        food = self._Food

        pygame.mixer.Sound.play(pygame.mixer.Sound(self._Settings.sfx["start_game"]))

        while run:
            clock.tick(self._Settings.fps)

            self._Settings.handle_control(snake)

            win.fill("black")
            self.drawGrid(win)

            _font_color = "#EEBA0B"
            font, _font = pygame.font.SysFont("Minecraft", 24), pygame.font.SysFont("Minecraft", 48)

            score = font.render(f"Score: {snake.score}", 1, _font_color)
            remaining_lives = font.render(f"Remaining Lives: {snake.lives}", 1, _font_color)
            pause_menu = _font.render(f"Game paused", 1, _font_color)
            game_over = _font.render(f"Game over! Try again?", 1, _font_color)

            if snake.lives >= 1:
                if not pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    snake.move(True)
                    if snake.get_head_position() == food.position:
                        snake.length += 1
                        snake.score += 1
                        pygame.mixer.Sound.play(pygame.mixer.Sound(self._Settings.sfx["food_eaten"]))
                        food.randomize_position()
                    snake.draw(win)
                    food.draw(win)
                else:
                    snake.move(False)
                    snake.draw(win)
                    food.draw(win)
                    win.blit(pause_menu, ((self.screen_width - pause_menu.get_width()) // 2, (self.screen_height - pause_menu.get_height()) // 2))
            else:
                win.blit(game_over, ((self.screen_width - game_over.get_width()) // 2, (self.screen_height - game_over.get_height()) // 2))
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    for n in range(3, 0, -1):
                        win.fill("black")
                        self.drawGrid(win)
                        pygame.mixer.Sound.play(pygame.mixer.Sound(self._Settings.sfx["timer"]))
                        restart_msg = _font.render(f"Game is starting in {n}", 1, _font_color)
                        win.blit(restart_msg, ((self.screen_width - restart_msg.get_width()) // 2, (self.screen_height - restart_msg.get_height()) // 2))
                        pygame.display.update()
                        time.sleep(1)
                    pygame.mixer.Sound.play(pygame.mixer.Sound(self._Settings.sfx["start_game"]))
                    snake.lives = 3

            win.blit(score, (8, 8))
            win.blit(remaining_lives, ((self.screen_width - remaining_lives.get_width()) // 2, 8))

            pygame.display.update()


if __name__ == "__main__":
    try:
        Game().start()
    except KeyboardInterrupt:
        exit("\nExiting...\n")
