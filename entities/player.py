import tkinter

from entities.entity import Entity
from modules.helper import Point

from PIL import Image, ImageTk
import time


class Player:
    def __init__(self, coordinate: Point, canvas: tkinter.Canvas, block_size: int, lvl: list[str]) -> None:
        self.canvas = canvas
        self.block_size = block_size
        self.lvl = lvl
        # adapt speed in function of ratio
        self.speed = int(4 * self.block_size/40)
        self.image_map = {
            "normal": ImageTk.PhotoImage(Image.open("resources/images/mario/mario.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
            "left": [
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-left0.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-left1.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-left2.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-left3.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-left4.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
            ],
            "right": [
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-right0.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-right1.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-right2.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-right3.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
                ImageTk.PhotoImage(Image.open("resources/images/mario/mario-right4.png").resize((block_size, block_size), Image.Resampling.LANCZOS)),
            ],
            "dead": ImageTk.PhotoImage(Image.open("resources/images/mario/dead.png").resize((block_size, block_size), Image.Resampling.LANCZOS))
        }
        self.image = self.image_map["normal"]
        self.update(coordinate)
        self.canvas_id = canvas.create_image(*self.center, image=self.image)
        self.is_jumping = False
        self.is_jumpkill = False
        self.jump_tick = 0
        self.animation = False

        # can be either -1: left; 0: static; 1: right
        self.direction = 0
        self.is_dead = False

    def render(self, coord: Point):
        self.canvas.coords(self.canvas_id, *coord)
        self.canvas.xview_moveto((coord.x-self.canvas.master.WIDTH/2)/(self.block_size*len(self.lvl[0])))
        self.update(coord)

    def update(self, coord: Point):
        self.center = coord
        self.top_left = Point(x=int(self.center.x-self.image.width()/2), y=int(self.center.y-self.image.height()/2))
        self.top_right = Point(x=int(self.center.x+self.image.width()/2), y=int(self.center.y-self.image.height()/2))
        self.bot_right = Point(x=int(self.center.x+self.image.width()/2), y=int(self.center.y+self.image.height()/2))
        self.bot_left = Point(x=int(self.center.x-self.image.width()/2), y=int(self.center.y+self.image.height()/2))

    def animate(self):
        while not self.is_dead:
            for i in range(5):
                match self.direction:
                    case -1:
                        self.image = self.image_map["left"][i]
                        self.canvas.itemconfig(self.canvas_id, image=self.image)
                    case 1:
                        self.image = self.image_map["right"][i]
                        self.canvas.itemconfig(self.canvas_id, image=self.image)
                    case 0:
                        self.image = self.image_map["normal"]
                        self.canvas.itemconfig(self.canvas_id, image=self.image)

                time.sleep(.05)
        
    
    def reset(self):
        self.direction = 0

    # Collision
    def collison_left(self) -> bool:
        if self.lvl[self.top_left.y//self.block_size][(self.top_left.x-self.speed)//self.block_size].isupper(): 
            return True
        if self.lvl[self.bot_left.y//self.block_size][(self.bot_left.x-self.speed)//self.block_size].isupper():
            return True
        return False

    def collision_right(self) -> bool:
        if self.lvl[self.top_right.y//self.block_size][(self.top_right.x+self.speed)//self.block_size].isupper():
            return True
        if self.lvl[self.bot_right.y//self.block_size][(self.bot_right.x+self.speed)//self.block_size].isupper():
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

    def adjust_ground(self) -> None:
        """if self.lvl[(self.bot_left.y+2)//self.block_size][self.bot_left.x//self.block_size].isupper():
            self.render(Point(self.center.x, self.center.y+2))
        if self.lvl[(self.bot_right.y+2)//self.block_size][self.bot_right.x//self.block_size].isupper():
            self.render(Point(self.center.x, self.center.y+2))"""
        return 

    # Movements
    def move_left(self, speed: int=None):
        if not self.collison_left():
            if speed is None: 
                speed = self.speed
            self.direction = -1
            self.render(Point(self.center.x-speed, self.center.y))

    def move_right(self, speed: int=None):
        if not self.collision_right():
            if speed is None: 
                speed = self.speed
            self.direction = 1
            self.render(Point(self.center.x+speed, self.center.y))
    
    def move_up(self, speed: int=None):
        if not self.collision_ceiling():
            if speed is None: 
                speed = self.speed
            self.render(Point(self.center.x, self.center.y-speed))

    def move_down(self, speed: int=None):
        if not self.collision_ground():
            if speed is None: 
                speed = self.speed
            self.render(Point(self.center.x, self.center.y+speed))
        else:
            self.adjust_ground()

    def apply_gravity(self) -> None:
        if self.is_jumping or self.is_jumpkill:
            return 
        self.move_down()

    def jump(self) -> None:
        if self.is_jumpkill:
            self.is_jumping = False
            self.jump_tick += 1

            if self.collision_ceiling():
                self.jump_tick = 0
                self.is_jumpkill = False
            elif self.jump_tick <= 20:
                self.move_up(int(self.speed))
            else:
                self.jump_tick = 0
                self.is_jumpkill = False

        elif self.is_jumping:  
            self.jump_tick += 1
            
            if self.collision_ceiling():
                self.jump_tick = 0
                self.is_jumping = False
            elif self.jump_tick <= 10:
                self.move_up(int(self.speed*1.5))
            elif self.jump_tick <= 25:
                self.move_up(int(self.speed))
            elif self.jump_tick <= 35:
                self.move_up(int(self.speed*0.5))
            else:
                self.jump_tick = 0
                self.is_jumping = False

    def reset_jump(self):
        self.jump_tick = 0
        self.is_jumping = False
        self.is_jumpkill = False

    def kill(self):
        self.is_dead = True
        self.canvas.itemconfigure(self.canvas_id, image=self.image_map["dead"])
        self.canvas.tag_raise(self.canvas_id)
        time.sleep(.4)
        while True:
            if self.top_left.y > (self.canvas.master.HEIGHT + self.block_size): break
            self.render(Point(self.center.x, self.center.y+self.speed))
            self.canvas.master.update()
            time.sleep(.005)
