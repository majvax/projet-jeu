from rich.traceback import install; install()

import tkinter.ttk
import tkinter

from modules.helper import Point
from modules.helper import kill_thread 
from modules.sound import play_sound


from entities.player import Player
from entities.goomba import Goomba



import threading
from PIL import Image, ImageTk

class Game(tkinter.Frame):
    def __init__(self, master, width, height, *args, **kwargs):
        super().__init__(master, height=height, width=width, *args, **kwargs)
        # RESOLUTION AVAILABLE
        # [screen width]x[screen height]@[block size]
        # 3840×2160@120
        # 2560×1440@80
        # 1920x1080@60
        # 1760x990@55
        # 1600x900@50
        # 1440x810@45   
        # 1280x720@40
        # 960x540@30
        self.theme = play_sound("resources/sound/main-theme.wav", False)


        match width:
            case 3840:
                self.ratio = 120
            case 2560:
                self.ratio = 80
            case 1920:
                self.ratio = 60
            case 1760:
                self.ratio = 55
            case 1600:
                self.ratio = 50
            case 1440:
                self.ratio = 45
            case 1280:
                self.ratio = 40
            case 960:
                self.ratio = 30
            case _:
                self.ratio = 40


        self.WIDTH = width
        self.HEIGHT = height

        self.tickrate = 10
        self.tickcount = 0
        self.jumptickcount = 0
        self.keys = []

        self.threads = []
        self.img_F = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/block.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_B = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/brick.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_1 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage1.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_2 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage2.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_3 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage3.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_4 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage4.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_5 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage5.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))
        self.img_6 = ImageTk.PhotoImage(Image.open("resources/images/tiles_set/nuage6.png").resize((self.ratio, self.ratio), Image.Resampling.LANCZOS))


        # setup game variable
        self.current_level = self.load_level("resources/niveaux/1.lvl")
        self.canvas = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT, scrollregion=(0, 0, self.ratio*len(self.current_level[0]), self.HEIGHT), bg="#6b8cff")
        self.canvas.place(relx=.5, rely=.5, anchor="center")

        # Setup Entities
        self.player = None
        self.koopa = []
        self.goombas = []

        self.draw_level()

        # bind all keys
        self.bind_all("<KeyPress>", self.handle_keypress)
        self.bind_all("<KeyRelease>", self.handle_keyrelease)
        # self.bind_all("<Escape>", self.exit)

    def handle_keypress(self, event: tkinter.Event) -> None:
        if event.keysym.lower() not in self.keys:
            self.keys.append(event.keysym.lower())

    def handle_keyrelease(self, event: tkinter.Event) -> None:
        if event.keysym.lower() in self.keys:
            self.keys.remove(event.keysym.lower())

    def load_level(self, filename: str):
        with open(filename, "r", encoding="utf8") as file:
            return [i.replace("\n", "") for i in file.readlines()]

    def draw_level(self) -> None:
        for row in range(len(self.current_level)):
            for column in range(len(self.current_level[row])):

                match self.current_level[row][column]:
                    case "F":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_F, anchor=tkinter.NW)
                    case "B":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_B, anchor=tkinter.NW)
                    case "1":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_1, anchor=tkinter.NW)
                    case "2":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_2, anchor=tkinter.NW)
                    case "3":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_3, anchor=tkinter.NW)
                    case "4":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_4, anchor=tkinter.NW)
                    case "5":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_5, anchor=tkinter.NW)
                    case "6":
                        self.canvas.create_image(column*self.ratio, row*self.ratio, image=self.img_6, anchor=tkinter.NW)
                    case "m":
                        self.player = Player(Point(column*self.ratio, row*self.ratio), self.canvas, self.ratio, self.current_level)
                    case "g":
                        self.goombas.append(Goomba(Point(column*self.ratio, row*self.ratio), self.canvas, self.ratio, self.current_level))

        self.canvas.update()


    def start(self) -> None:
        self.after(50, self.animate)
        self.after(80, self.start_entities_animation)

        self.mainloop()

    def animate(self) -> None:
        if "up" in self.keys:
            if not self.player.is_jumping and self.player.collision_ground():
                self.player.is_jumping = True
                play_sound("resources/sound/big-jump.wav", False)

        if "right" in self.keys:
            self.player.move_right()

        if "left" in self.keys:
            self.player.move_left()

        if not "left" in self.keys and not "right" in self.keys and not "up" in self.keys:
            self.player.reset()

        self.player.jump()
        self.player.apply_gravity()

        self.tickcount += 1

        for goomba in self.goombas:
            goomba: Goomba = goomba
            if goomba.direction: 
                goomba.move_right()
            else:
                goomba.move_left()
            goomba.move_down()

            col, game_over = goomba.check_collision(self.player)
            if col:
                if game_over:
                    self.stop_game()
                    return
                else:
                    play_sound("resources/sound/kick.wav", False)
                    goomba.kill()
                    self.goombas.remove(goomba)
                    self.player.reset_jump()
                    self.player.is_jumpkill = True

        self.after(self.tickrate, self.animate)

    def start_entities_animation(self):
        t = threading.Thread(target=self.player.animate, daemon=True)
        t.start()
        self.threads.append(t)
        for goomba in self.goombas:
            t = threading.Thread(target=goomba.animate, daemon=True)
            t.start()
            self.threads.append(t)

    def kill_threads(self):
        for thread in self.threads:
            kill_thread(thread)

    def stop_game(self):
        kill_thread(self.theme)
        self.kill_threads()
        thread = play_sound("resources/sound/death.wav", False)
        self.player.kill()
        thread.join()
        self.exit()

    def exit(self, event=None):
        self.quit()




