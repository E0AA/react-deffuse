import pygame, random, copy

EMPTY: int = 0
CHEM_A: int = 1
CHEM_B: int = 2

def draw_grid(surface, grid: list, grid_offsets: dict, tile_size: int) -> None:
    surface.fill("#ffffff")

    tile_margin: int = -1
        
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            color: str = "#000000"

            if grid[y][x] == CHEM_A:
                color = "#FFFF94"
            if grid[y][x] == CHEM_B:
                color = "#0082D3"
            
            xpos: int = x*tile_size + (tile_margin*x) + grid_offsets["x"]
            ypos: int = y*tile_size + (tile_margin*y) + grid_offsets["y"]

            if 0 < xpos < 1024 and 0 < ypos < 512:
                pygame.draw.rect(
                    surface, color,
                    (
                        xpos, ypos,
                        tile_size, tile_size
                    )
                )
            if xpos > 1024:
                break

def get_region(grid: list, xpos: int, ypos: int, radius: int, mode: str) -> list:
    region: list = []

    width: int = len(grid[0])
    height: int = len(grid)

    for y in range(ypos-radius, ypos+radius):
        region.append([])
        for x in range(xpos-radius, xpos+radius):
            if x >= width: x -= width
            if y >= height: y -= height
            region[-1].append([x, y])
    
    if mode == "values":
        for y in range(len(region)):
            for x in range(len(region[y])):
                region[y][x] = grid[region[y][x][1]][region[y][x][0]]
    
    return region

def process_reaction(grid: list) -> list:
    region_radius: int = 2
    
    height: int = len(grid)
    width: int = len(grid[0])

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == CHEM_B:
                cells: list = sum(get_region(grid, x, y, region_radius, "values"), [])
                if cells.count(CHEM_B) >= 2 and cells.count(CHEM_A) > 0:
                    pos: list = sum(get_region(grid, x, y, region_radius, "coords"), [])[cells.index(CHEM_A)]
                    grid[pos[1]][pos[0]] = CHEM_B

    return grid

def add_chemicals(grid: list) -> list:
    feed_rate: int = 5000
    kill_rate: int = 500
 
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == EMPTY and 1 == random.randint(1, feed_rate):
                grid[y][x] = CHEM_A
            if grid[y][x] == CHEM_B and 1 == random.randint(1, kill_rate):
                grid[y][x] = EMPTY

    return grid

def populate_chem_b(grid: list) -> list:
    spawn_rate: int = 10

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if 1 == random.randint(1, spawn_rate):
                grid[y][x] = CHEM_B

    return grid

def main() -> None:
    RUN: bool = True
    FPS: int = 60

    GRID: list = [
        [EMPTY for _ in range(200)] for _ in range(200)
    ]

    grid_offsets: dict = {
        "x": -10,
        "y": -10
    }
    tile_size: int = 10

    screen = pygame.display.set_mode((1024, 512))
    clock = pygame.time.Clock()

    GRID = populate_chem_b(GRID)

    while RUN:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            grid_offsets["y"] += 5
        if keys[pygame.K_a]:
            grid_offsets["x"] += 5
        if keys[pygame.K_s]:
            grid_offsets["y"] -= 5
        if keys[pygame.K_d]:
            grid_offsets["x"] -= 5

        if keys[pygame.K_EQUALS]:
            tile_size += 1
        if keys[pygame.K_MINUS]:
            tile_size -= 1

        draw_grid(screen, GRID, grid_offsets, tile_size)

        GRID = add_chemicals(GRID)
        GRID = process_reaction(GRID)

        pygame.display.update()

    pygame.display.quit()

if __name__ == "__main__":
    main()
