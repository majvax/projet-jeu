import tkinter

from modules.helper import Point
from entities.entity import Entity
from entities.player import Player

from PIL import Image, ImageTk
import itertools
import time


class Goomba(Entity):
    def __init__(self, coordinate: Point, canvas: tkinter.Canvas, block_size: int, lvl: list[str]) -> None:
        image_map = {
            "normal": ImageTk.PhotoImage(Image.open("resources/images/goomba/goomba1.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
            "normal2": ImageTk.PhotoImage(Image.open("resources/images/goomba/goomba2.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
            "dead": ImageTk.PhotoImage(Image.open("resources/images/goomba/goomba_die.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
        }
        speed = int(2 * block_size/40)
        super().__init__(coordinate, canvas, block_size, image_map, speed, lvl)
        self.is_dead = False

        
    def animate(self) -> None:

        for i in itertools.cycle([self.image_map["normal"], self.image_map["normal2"]]):
            if self.is_dead: break
            self.canvas.itemconfigure(self.canvas_id, image=i)
            time.sleep(.05)

        self.canvas.itemconfigure(self.canvas_id, image=self.image_map["dead"])
        time.sleep(.4)
        self.canvas.delete(self.canvas_id)

    def check_collision(self, player:Player):

        # check if player kill goomba
        if (player.bot_right.x - self.top_right.x)**2 + (player.bot_right.y - self.top_right.y)**2 < 150 \
            or (player.bot_left.x - self.top_left.x)**2 + (player.bot_left.y - self.top_left.y)**2 < 150 \
            or (player.bot_left.x - self.top_right.x)**2 + (player.bot_left.y - self.top_right.y)**2 < 150 \
            or (player.bot_right.x - self.top_left.x)**2 + (player.bot_right.y - self.top_left.y)**2 < 150:
            return (True, False)
        elif (player.center.x - self.center.x)**2 + (player.center.y - self.center.y)**2 < 800:
            return (True, True)
        
        return (False, False)
 

    def kill(self):
        self.is_dead = True
        
