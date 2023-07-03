# react-deffuse
Failed program. Attempt to recreate reaction diffusion.

Using pygame libraray: [pygame-ce](https://github.com/pygame-community/pygame-ce)

Only 3 dependencies
```python
import pygame, random, copy
```

Somebody fix this code. Fix rest of the code while you're at it.
```python
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
```

Tutorial link: [karlsims](https://www.karlsims.com/rd.html)
