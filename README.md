# Plato
This project is a game in 2d based on the graphical interface tkiner. This Project has been made because of school.

## 💾 Installation

```
git clone https://github.com/majvax/projet-jeu.git
cd projet-jeu
pip install -R requirements.txt
```
##### Due to some problems, it will try to install all of the 4 depencies supported by pydub for the play method in pydub, got random error while installing only one package. I agree it's not optimal but it is the only workaround i found

## 👍 Contributing

### New Entity
to add new entities, simply go to the folder called "entities" and create a new file which will contain your code
```python
from entities.entity import Entity
from modules.helper import Point

class YourEntity(Entity):
    def __init__(
        self, 
        coordinate: Point, 
        canvas: tkinter.Canvas, 
        block_size: int, 
        lvl: list[str]
    ) -> None:

        image_map = {
            "normal": ImageTk.PhotoImage(
            Image.open(
                "resources/images/path_to_your_image"
                ).resize((block_size, block_size), Image.Resampling.LANCZOS))
        }

        speed = int(2 * self.block_size/40)
        super().__init__(coordinate, canvas, block_size, image_map, speed, lvl)
    

    def animate(self):
        while True:
            if self.direction:
                pass
            
            time.sleep(.05)
```
- `coordinate` represent the starting coordinate (Point)
- `canvas` is the tkinter.Canvas defined in Game.py
- `block_size` represent the size of a block, it is used to upscale or downscale window
- `lvl` is the current level the player is evolve in
- `image_map` is a dict containing Image. Used to animate your Entity
##### See entities/goomba.py for a concrete exemple

### New level
Currently there is no way to go to a level to an another. However, i'm working on it.

Levels are represented by a file, which make it easy to create and use. They are located in resources\niveaux.
Here is an exemple:
```
A                                                                                                            A
A                                                                                                            A
A                                                                                                            A
A              123                                                                                           A
A              456                                                                                           A
A                                                                                                            A
A                                                                                                            A
A                                      123                                                                   A
A                                      456                                                                   A
A                           g                                     123                                        A
A                          BBB                                    456                                        A
A                                                        g                                                   A
A                                                        B  B               g g                              A
A               B  B  B                   BBB           BB  BB            BBBBBBBB                           A
A                                                      BBB  BBB                                              A
A m                                                   BBBB  BBBB                                             A
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
```
##### Each letter/number have his own representation
- "A" stands for Air, which is a collision block who do not have image
- "F" stand for the ground, collision with a texture
- "B" are standard block
- "g" are gooba 
- 1-6 are for the clouds
- ...
##### Only Uppercase letter are collision, it make it simpler to track of in code 



## 💀 Bugs

##### Feel free to pull a request when you found a bug.

#### Known bugs:
- checking collision between the player and other Entity not working properly

## 🔥 TODO
- [] new ntities
- [] better menu
- [] lvl management
- [] flags pole
- [] rewrite some of the code to be less junk
