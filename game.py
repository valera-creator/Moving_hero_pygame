import os
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 50
WIDTH = 500
HEIGHT = 500
STEP = 50
CELL_SIZE = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Перемещение героя. Новый уровень')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, png=False, obrezanie_fon=False):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        quit()
    image = pygame.image.load(fullname)
    if obrezanie_fon:  # убрать фон
        del_color = image.get_at((0, 0))
        image.set_colorkey(del_color)
    if not png:
        image = image.convert()  # не png форматы
    else:
        image = image.convert_alpha()  # png
    return image


def start_game():
    fon = pygame.transform.scale(load_image(name='fon.png', png=True, obrezanie_fon=True), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coords_y = 125
    intro_text = ["ЗАСТАВКА", "", "Правила игры:", "Алла Михайловна должна мне", "100 баллов или 100 рублей"]
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        coords_y += 5
        intro_rect.top = coords_y
        intro_rect.x = 140
        coords_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_levels(name):
    with open(os.path.join('data', name), mode='r') as file:
        level_map = [i.strip() for i in file]
        max_width = max(map(len, level_map))
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_levels(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == "@":
                Tile('empty', x, y)
                player = Player(x, y)
            elif level[y][x] == "#":
                Tile('box', x, y)
    return player, x, y


def move_block_left():
    left = []
    for elem in tiles_group:
        left.append([elem.rect.x, elem])
    max_cord = max(map(lambda x: x[0], left))
    for elem in left:
        if elem[1].rect.x == max_cord:
            elem[1].rect.x -= CELL_SIZE * len(level[0])


def move_block_right():
    right = []
    for elem in tiles_group:
        right.append([elem.rect.x, elem])
    min_cord = min(map(lambda x: x[0], right))
    for elem in right:
        if elem[1].rect.x == min_cord:
            elem[1].rect.x += CELL_SIZE * len(level[0])


def move_block_up():
    up = []
    for elem in tiles_group:
        up.append([elem.rect.y, elem])
    max_cord = max(map(lambda x: x[0], up))
    for elem in up:
        if elem[1].rect.y == max_cord:
            elem[1].rect.y -= CELL_SIZE * len(level)


def move_block_down():
    down = []
    for elem in tiles_group:
        down.append([elem.rect.y, elem])
    min_cord = min(map(lambda x: x[0], down))
    for elem in down:
        if elem[1].rect.y == min_cord:
            elem[1].rect.y += CELL_SIZE * len(level)


class Tile(pygame.sprite.Sprite):
    def __init__(self, obj, x, y):
        self.tile_images_and_sprites = {'box': load_image(name='box.png', png=True, obrezanie_fon=False),
                                        'empty': load_image(name='grass.png', png=True, obrezanie_fon=False),

                                        }
        super().__init__(tiles_group, all_sprites)
        self.image = self.tile_images_and_sprites[obj]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect().move(CELL_SIZE * x, CELL_SIZE * y)
        self.type_block = obj
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = load_image(name='mario.png', png=True, obrezanie_fon=True)
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 15
        self.rect.y = y * CELL_SIZE + 5

    def update(self, event):
        if event.key == pygame.K_LEFT:
            self.rect.x -= STEP
            if pygame.sprite.spritecollideany(self, tiles_group).type_block == 'box':
                self.rect.x += STEP
            else:
                move_block_left()

        if event.key == pygame.K_RIGHT:
            self.rect.x += STEP
            if pygame.sprite.spritecollideany(self, tiles_group).type_block == 'box':
                self.rect.x -= STEP
            else:
                move_block_right()

        if event.key == pygame.K_UP:
            self.rect.y -= STEP
            if pygame.sprite.spritecollideany(self, tiles_group).type_block == 'box':
                self.rect.y += STEP
            else:
                move_block_up()

        if event.key == pygame.K_DOWN:
            self.rect.y += STEP
            if pygame.sprite.spritecollideany(self, tiles_group).type_block == 'box':
                self.rect.y -= STEP
            else:
                move_block_down()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj_sprite):
        obj_sprite.rect.x += self.dx
        obj_sprite.rect.y += self.dy

    def update(self, tracker_obj):
        self.dx = -(tracker_obj.rect.x + tracker_obj.rect.w // 2 - WIDTH // 2)
        self.dy = -(tracker_obj.rect.y + tracker_obj.rect.h // 2 - HEIGHT // 2)


start_game()
level = load_levels('level.txt')
for i in range(len(level)):
    level[i] = list(level[i])

player, all_x, all_y = generate_levels(level)
camera = Camera()
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.update(event)

    camera.update(player)
    for elem in all_sprites:
        camera.apply(elem)

    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
