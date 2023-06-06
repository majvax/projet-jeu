from PIL import Image, ImageOps
import sys


if __name__ == "__main__":
    asset = Image.open(sys.argv[1])
    img = asset.crop((int(sys.argv[2])*16, int(sys.argv[3])*16, int(sys.argv[4])*16, int(sys.argv[5])*16))
    if "--flip" in sys.argv:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    
    
    img.save(sys.argv[6])
