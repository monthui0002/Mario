from PIL import Image
import glob, os


def main():
    print(glob.glob("*.py"))
    for infile in glob.glob("./img/*.png"):
        print(infile)
        im = Image.open(infile)
        im.save(infile)
    return 0


main()
