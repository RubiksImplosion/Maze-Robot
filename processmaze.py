pil = True
try:
    from PIL import Image
except ImportError:
    pil = False
    
import pprint, os

def genBitmap(path):
    if pil:
        image = Image.open(path)
        width = image.width
        height = image.height
        data = image.getdata()

        bitmap = []
        for h in range(1,height-1):
            row = []
            for w in range(1,width-1):
                row.append(data[h*height+w])
            bitmap.append(row)

        return bitmap
    else:
        return [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
                [4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

#pprint.pprint(genBitmap(r"C:\Users\cs207846\OneDrive - Lamar Consolidated ISD\Programs\Python\Maze Solver\mazes\maze1.bmp"))


def updateImage():
    bitmap = "small"
    path = os.path.dirname(os.path.abspath(__file__)) + r"\mazes\{}.bmp".format(bitmap)
    image = Image.open(path)
    image.putpixel((1,1),0)
    image.putpixel((1,3),0)
    image.save(os.path.dirname(os.path.abspath(__file__)) + r"\{}.bmp".format(bitmap))


