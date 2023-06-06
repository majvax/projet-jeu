from rich.traceback import install; install()


import tkinter
from tkinter import ttk

from components.game import Game
from modules.sound import play_sound

from PIL import ImageTk, Image
import sys
import time

class Settings(tkinter.Toplevel):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.geometry("500x300")

        self.focus_set()
        self.master.attributes('-disabled', True)
        self.attributes('-topmost', True)        
        self.protocol("WM_DELETE_WINDOW", self.close)

        self.resolution_combobox = ttk.Combobox(
            self, 
            values=[
                "3840x2160 - not tested",
                "2560x1440 - not tested",
                "1920x1080 - recommended",
                "1760x990 - not tested",
                "1600x900 - not tested",
                "1440x810 - not tested",
                "1280x720 - optimal",
                "960x540 - low end pc"
                ],
            )
        self.resolution_combobox.pack(padx=(40, 40), anchor="w",)

        self.fullscreen_label = tkinter.Label(self, text="if fullscreen, make sure to select to resultion that match your own\n screen resolution otherwise, it will not work properly")
        self.fullscreen_label.pack(padx=(40, 40), anchor="w",)

        self.fullscreen_checkbox = ttk.Checkbutton(self, text="fullscreen", state=False)
        self.fullscreen_checkbox.pack(padx=(40, 40), anchor="w",)
        
        self.apply_btn = tkinter.Button(self, text="Apply !", command=self.apply_settings)
        self.apply_btn.pack(padx=(40, 40), anchor="w",)

        self.tkinter_version_label = tkinter.Label(self, text=f"tkinter {str(tkinter.TkVersion)}", fg="gray30")
        self.tkinter_version_label.pack(padx=(40, 40), anchor="w",)


    def close(self, event=None):
        self.master.attributes('-disabled', False)
        self.destroy()

    def apply_settings(self, event=None):
        resolution = self.resolution_combobox.get().strip().split("-")[0].strip().split("x")
        fullscreen = True if "selected" in self.fullscreen_checkbox.state() else False

        self.master.change_resolution(resolution, fullscreen)
        self.close()

class Credit(tkinter.Toplevel):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.geometry("500x300")

        self.label = tkinter.Label(
            self,
            text="Dehez Guillaume\nDevivier Elie\nJuliette",
            font=("Helvetica", 30))
        self.label.pack()


class Window(tkinter.Tk):
    def __init__(self) -> None:
        super().__init__("Super Mario Bros", None, "Super Mario Bros", True, True, None)
        
        self.WIDTH, self.HEIGHT = 1280, 720
        
        # self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
    
        self.frame = MainFrame(self, self.WIDTH, self.HEIGHT)
        self.frame.pack()


        self.bind_all("<Escape>", self.close)

    def change_resolution(self, resolution: tuple | list, fullscreen: bool) -> None:
        self.WIDTH, self.HEIGHT = int(resolution[0]), int(resolution[1])
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        if fullscreen:
            self.attributes("-fullscreen", True)
        else: 
            self.attributes("-fullscreen", False)
        
        self.frame.destroy()
        self.frame = MainFrame(self, self.WIDTH, self.HEIGHT)
        self.frame.pack()

    def close(self, event=None) -> None:
        sys.exit()
    
    def start_game(self) -> None:
        self.frame.destroy()
        self.update()


        self.unbind_all("<Up>")
        self.unbind_all("<Down>")
        self.unbind_all("<Right>")
        while True:
            game = Game(self, self.WIDTH, self.HEIGHT)
            game.place(relx=.5, rely=.5, anchor="center")
            game.start()
        


class MainFrame(tkinter.Frame):
    def __init__(self, master, width, height, *args, **kwargs):
        super().__init__(master, width=width, height=height, *args, **kwargs)

        self.WIDTH, self.HEIGHT = width, height

        self.canvas = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()

        self.image = ImageTk.PhotoImage(Image.open("resources/images/menu.png").resize((self.WIDTH, self.HEIGHT), Image.Resampling.LANCZOS))
        self.canvas.create_image(0, 0, image=self.image, anchor=tkinter.NW)

        self.play_btn = self.canvas.create_text(self.WIDTH/2 - 100, self.HEIGHT/2 - 80, text="> Play", justify="left", anchor=tkinter.W, font=("Helvetica", 50, "bold", "italic"), fill="white")
        self.settings_btn = self.canvas.create_text(self.WIDTH/2 - 100, self.HEIGHT/2, text="Settings", justify="left", anchor=tkinter.W, font=("Helvetica", 50, "bold"), fill="white")
        self.credit_btn = self.canvas.create_text(self.WIDTH/2 - 100, self.HEIGHT/2 + 80, text="Credit", justify="left", anchor=tkinter.W, font=("Helvetica", 50, "bold"), fill="white")

        self.option = 0

        self.bind_all("<Up>", self.select_up)
        self.bind_all("<Down>", self.select_down)
        self.bind_all("<Right>", self.select)


    def select_up(self, event):
        play_sound("resources/sound/fireball.wav", False)
        if not self.option == 0:
            self.option -= 1
            if self.option == 1:
                self.canvas.itemconfigure(self.settings_btn, text=f"> Settings", font=("Helvetica", 50, "bold", "italic"))
                self.canvas.itemconfigure(self.credit_btn, text=f"Credit", font=("Helvetica", 50, "bold")) 
            else:
                self.canvas.itemconfigure(self.play_btn, text=f"> Play", font=("Helvetica", 50, "bold", "italic"))
                self.canvas.itemconfigure(self.settings_btn, text=f"Settings", font=("Helvetica", 50, "bold")) 

    def select_down(self, event):
        play_sound("resources/sound/fireball.wav", False)
        if not self.option == 2:
            self.option += 1
            if self.option == 1:
                self.canvas.itemconfigure(self.settings_btn, text=f"> Settings", font=("Helvetica", 50, "bold", "italic"))
                self.canvas.itemconfigure(self.play_btn, text=f"Play", font=("Helvetica", 50, "bold")) 
            else:
                self.canvas.itemconfigure(self.credit_btn, text=f"> Credit", font=("Helvetica", 50, "bold", "italic"))
                self.canvas.itemconfigure(self.settings_btn, text=f"Settings", font=("Helvetica", 50, "bold")) 


    def select(self, event):
        play_sound("resources/sound/fireball.wav", False)
        match self.option:
            case 0:
                self.master.start_game()
            case 1:
                Settings(self.master).mainloop()
            case 2:
                Credit(self.master).mainloop()


