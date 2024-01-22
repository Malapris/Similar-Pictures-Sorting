from itertools import product
from pathlib import Path

from PIL import Image, ImageChops
import sys
import os.path
import shutil

chemin=""
threshold=0.0815
noir=Image.new(mode="RGB", size=(16,16),color="black")

def summarise(img: Image.Image) -> Image.Image:
    """Summarise an image into a 16 x 16 image."""
    resized = img.resize((16, 16))
    # resized.show()
    return resized


def difference(img1: Image.Image, img2: Image.Image) -> float:
    """Find the difference between two images."""

    diff = ImageChops.difference(img1, img2)

    acc = 0
    width, height = diff.size
    for w, h in product(range(width), range(height)):
        r, g, b = diff.getpixel((w, h))
        acc += (r + g + b)

    average_diff = acc / (width * height)
    normalised_diff = average_diff
    return normalised_diff


def explore_directory(path: Path) -> None:
    """Find images in a directory and compare them all."""

    files = (
        list(path.glob("*.jpg")) + list(path.glob("*.jpeg")) + list(path.glob("*.png"))
    )
    diffs = {}

    summaries = [(file, summarise(Image.open(file).convert('RGB'))) for file in files]

    # print (summaries)

    for (f1, i1) in (summaries):
        key = tuple(sorted([str(f1)]))
        # if key in diffs:
            # continue

        diff = difference(i1, noir)
        # print("===> ",key, diff)
        diffs[key] = diff


    i=1
    
    # print()
    # print("===========KEYS===========")
    # print( diffs )
    
    print()
    print("===========KEYS===========")

    ssorted = dict(sorted(diffs.items(), key=lambda item: item[1]))
    #print ("SSORTED : ",ssorted)

    with open(os.path.join(chemin,'fssort.ini'), 'w') as f:
        for i in ssorted:
            print (i[0], diffs[i])
            f.write(i[0]+'\n')
    f.close()
    
    
    return 


if __name__ == "__main__":
    print(sys.argv[1])
    chemin=sys.argv[1]
    explore_directory(Path(sys.argv[1]))
