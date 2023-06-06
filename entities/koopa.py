import tkinter 


from modules.helper import Point
from entities.entity import Entity
from entities.player import Player

from PIL import Image, ImageTk
import time


class Koopa(Entity):
    def __init__(self, coordinate: Point, canvas: tkinter.Canvas, block_size: int, lvl: list[str]) -> None:


        image_map = {
            "normal": ImageTk.PhotoImage(Image.open("").resize((block_size, block_size), Image.Resampling.LANCZOS))
        }

        speed = int(2 * self.block_size/40)
        super().__init__(coordinate, canvas, block_size, image_map, speed, lvl)
    

    def animate(self):
        while True:
            if self.direction:
                pass
            
            time.sleep(.05)