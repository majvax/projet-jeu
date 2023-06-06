import tkinter
import time
import random
from PIL import Image, ImageTk

from modules.helper import Point

# Installing Better error
from rich.traceback import install; install()



class Entity:

    def __init__(self, coordinate: Point, canvas: tkinter.Canvas, block_size: int, image_map: dict[str, ImageTk.PhotoImage], speed: int, lvl: list[str]) -> None:
        self.canvas = canvas
        self.block_size = block_size
        self.lvl = lvl
        self.speed = speed
        self.image_map = image_map
        self.image = self.image_map["normal"]
        self.update(coordinate)

        self.canvas_id = self.canvas.create_image(*coordinate, image=self.image)
        self.is_jumping = False
        self.direction = bool(random.randint(0, 1))

    # Render
    def render(self, coordinate: Point):
        self.canvas.coords(self.canvas_id, *coordinate)
        self.update(coordinate)
    
    def update(self, coordinate: Point):
        self.center = coordinate
        self.top_left = Point(int(self.center.x-self.image.width()/2), int(self.center.y-self.image.height()/2))
        self.top_right = Point(int(self.center.x+self.image.width()/2), int(self.center.y-self.image.height()/2))
        self.bot_right = Point(int(self.center.x+self.image.width()/2), int(self.center.y+self.image.height()/2))
        self.bot_left = Point(int(self.center.x-self.image.width()/2), int(self.center.y+self.image.height()/2))


    # Collision
    def collison_left(self) -> bool:
        if self.lvl[self.top_left.y//self.block_size][(self.top_left.x-self.speed)//self.block_size].isupper():
            self.direction = not self.direction
            return True
        if self.lvl[self.bot_left.y//self.block_size][(self.bot_left.x-self.speed)//self.block_size].isupper():
            self.direction = not self.direction
            return True
        return False

    def collision_right(self) -> bool:
        if self.lvl[self.top_right.y//self.block_size][(self.top_right.x+self.speed)//self.block_size].isupper():
            self.direction = not self.direction
            return True
        if self.lvl[self.bot_right.y//self.block_size][(self.bot_right.x+self.speed)//self.block_size].isupper():
            self.direction = not self.direction
            return True
        return False

    def collision_ground(self) -> bool:
        if self.lvl[(self.bot_left.y+self.speed)//self.block_size][self.bot_left.x//self.block_size].isupper():
            return True
        if self.lvl[(self.bot_right.y+self.speed)//self.block_size][self.bot_right.x//self.block_size].isupper():
            return True
        return False

    def collision_ceiling(self) -> bool:
        if self.lvl[(self.top_right.y-self.speed)//self.block_size][self.top_right.x//self.block_size].isupper():
            return True
        if self.lvl[(self.top_left.y-self.speed)//self.block_size][self.top_left.x//self.block_size].isupper():
            return True
        return False

   # Movements
    def move_left(self):
        if not self.collison_left():
            self.render(Point(self.center.x-self.speed, self.center.y))

    def move_right(self):
        if not self.collision_right():
            self.render(Point(self.center.x+self.speed, self.center.y))

    def move_up(self, speed: int | None=None):
        if speed is None:
            speed = self.speed
        if not self.collision_ceiling():
            self.render(Point(self.center.x, self.center.y-self.speed))

    def move_down(self):
        if not self.collision_ground():
            self.render(Point(self.center.x, self.center.y+self.speed))

    def apply_gravity(self) -> None:
        if not self.is_jumping:
            self.move_down()

