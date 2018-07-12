import sys
from PIL import Image

def imageToArray(filename):
    img = Image.open(filename)
    binary=[1 if c==(0,0,0) else 0 for c in img.getdata()]  # convert all black pixels to 1s and other pixels to zero
    text=""
    for i, b in enumerate(binary):
        if i%img.size[0]==0:
            text+="["
        text+=str(b)
        if (i+1)%img.size[0]==0:
            text+="]"
            if i+1<len(binary):
                text+=",\n"
        else:
            text+=", "

    return "["+text+"]"

if __name__ == "__main__":
    if len(sys.argv)>1:
        print(imageToArray(sys.argv[1]))  # get image filename from console arguments
    else:
        print(imageToArray(input("image to convert: ")))  # get image file name from console input
