from itertools import product
from pathlib import Path

from PIL import Image, ImageChops
import sys
import os.path
import shutil

chemin=""
threshold=0.0815

def summarise(img: Image.Image) -> Image.Image:
    """Summarise an image into a 16 x 16 image."""
    resized = img.resize((16, 16))
    return resized


def difference(img1: Image.Image, img2: Image.Image) -> float:
    """Find the difference between two images."""

    diff = ImageChops.difference(img1, img2)

    acc = 0
    width, height = diff.size
    for w, h in product(range(width), range(height)):
        r, g, b = diff.getpixel((w, h))
        acc += (r + g + b) / 3

    average_diff = acc / (width * height)
    normalised_diff = average_diff / 255
    return normalised_diff


def explore_directory(path: Path) -> None:
    """Find images in a directory and compare them all."""

    files = (
        list(path.glob("*.jpg")) + list(path.glob("*.jpeg")) + list(path.glob("*.png"))
    )
    diffs = {}

    summaries = [(file, summarise(Image.open(file).convert('RGB'))) for file in files]

    for (f1, sum1), (f2, sum2) in product(summaries, repeat=2):
        key = tuple(sorted([str(f1), str(f2)]))
        if f1 == f2 or key in diffs:
            continue

        diff = difference(sum1, sum2)
        #print(key, diff)
        diffs[key] = diff


    i=1
    
    print()
    print("===========KEYS===========")
    print(diffs.keys())
    
    print()
    print("Near-duplicates found:")
    print("======================")
    #print(os.path.split(chemin)[0])

    for key, diff in diffs.items():
        if diff < float(threshold):
            print (key) 
            
            fa=os.path.split(key[0])[1]
            fb=os.path.split(key[1])[1]
            
            dd=os.path.join(chemin,os.path.splitext(os.path.basename(key[0]))[0]+"_group")
            
            print(dd)
            print(fa)
            print(fb)
            if not os.path.exists(dd) and ( os.path.exists(key[0]) or os.path.exists(key[1]) ):
                os.mkdir(dd)
                if os.path.exists(key[0]):
                    shutil.move(key[0],os.path.join(dd,fa))
                if os.path.exists(key[1]):
                    shutil.move(key[1],os.path.join(dd,fb))
            
            i=i+1

    print ("Couples : ",i)

if __name__ == "__main__":
    print(sys.argv[1])
    chemin=sys.argv[1]
    explore_directory(Path(sys.argv[1]))
