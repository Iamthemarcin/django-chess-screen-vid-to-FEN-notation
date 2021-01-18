import operator
import os

from PIL import Image, ImageChops



def remove_background(input):
    filename, file_extenstion = os.path.splitext(input)
    im = Image.open(input)
    newImgData = []
    blackColor = (255, 255, 255, 255)
    whiteColor = (0, 0, 0, 255)
    width, height = im.size
    top_right = im.getdata()[width-1]
    print('prawa gora ' + str(top_right))
    bt_left = im.getdata()[-1* width]
    print('lewa dol ' + str(bt_left))
    top_left = im.getdata()[0]
    print('lewa gora ' + str(top_left))

    for pixel in im.getdata():
        if pixel == (240, 221, 179, 255) or pixel == (185, 137, 95, 255) or pixel == (161, 171, 56, 255):
            newImgData.append((240, 221, 179, 255))
        else:
            newImgData.append(pixel)
            print(pixel)
    newim = Image.new(im.mode, im.size)
    newim.putdata(newImgData)
    newim.show()
    return newim.save('../MainPage/static/images/chess_pieces/white_pawn.png')


w = remove_background('../media/images/Zrzut_ekranu_z_2020-12-07_23-56-06-4-5.png')

from PIL import Image
import os

def imgcrop(input, xPieces, yPieces):
    filename, file_extension = os.path.splitext(input)
    im = Image.open(input)
    im.resize((256, 256),Image.BOX)
    imgwidth, imgheight = im.size
    #print('dupaaaa' + str(imgwidth),str(imgheight))
    height = imgheight/yPieces
    width = imgwidth/xPieces
    colours = {}
    for pixel in im.getdata():
        if pixel in colours.keys():
            colours[pixel] += 1
        else:
            colours[pixel] = 0
    x = sorted(colours.items(), key=(lambda i: i[1]))
    print(x[-1][0])
    print(x[-2][0])

    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            #print(box)
            a = im.crop(box)
            #try:
                #a.save(filename + "-" + str(i) + "-" + str(j) + file_extension)
            #except:
                #pass

#imgcrop('/home/marcin/Chess/src/media/images/Zrzut_ekranu_z_2020-12-07_23-56-06.png',8,8)