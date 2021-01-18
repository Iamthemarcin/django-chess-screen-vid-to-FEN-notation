from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm, VideoForm
import numpy as np
import shutil
import os
from pathlib import Path
from PIL import Image, ImageChops
import operator
from celery import group
import cv2







def main_page(request, *args, **kwargs):
    return render(request, "index.html", {})


BASE_DIR = str(Path(__file__).resolve().parent.parent)


def image_upload_view(request):


    """Process images uploaded by users"""
    if request.method == 'POST':

        if "image" in request.POST:
            image_form = ImageForm(request.POST, request.FILES, prefix="image")
            if image_form.is_valid():
                path = os.path.join(BASE_DIR + '/media/images')
                shutil.rmtree(path)
                image_form.save()
                # Get the current instance object to display in the template
                img_obj = image_form.instance
                i1 = Image.open(BASE_DIR + img_obj.Img.url)
                i1.resize((256, 256), Image.ANTIALIAS)
                notation = imgcrop(BASE_DIR + img_obj.Img.url, 8, 8)
                notation += ' w KQkq - 0 1'

            video_form = VideoForm(prefix="video")
            return render(request, 'index.html',
                          {'image_form': image_form, 'video_form': video_form, 'img_obj': img_obj, 'notation': notation})

        # DLA WIDEŁO--------------------------------------------------------------------------------------------------
        elif "video" in request.POST:
            video_form = VideoForm(request.POST, request.FILES, prefix="video")
            if video_form.is_valid():
                path = os.path.join(BASE_DIR + '/media/videos')
                shutil.rmtree(path)
                video_form.save()
                video_obj = video_form.cleaned_data['Vid']
                video_path = path + '/' + str(video_obj)
                make_frames(video_path)




            image_form = ImageForm(prefix="image")
            return render(request, 'index.html', {'image_form': image_form, 'video_form': video_form})

    else:
        image_form = ImageForm(prefix="image")
        video_form = VideoForm(prefix="video")
        return render(request, 'index.html', {'image_form': image_form, 'video_form': video_form})


def make_frames(video_path):
    capture = cv2.VideoCapture(video_path)
    directory, name = os.path.split(video_path)
    print('wideło ' + str(video_path))
    print(directory)
    frame = 1
    saved_count = 0
    rate = 10
    im = Image.open('/home/marcin/Chess/src/media/images/Zrzut_ekranu_z_2020-12-01_18-23-55.png')
    while frame:
        _, image = capture.read()
        if frame % rate == 0:
                    save_path = os.path.join(directory, "{:05d}.jpg".format(frame))
                    if image is not None:
                        cv2.imwrite(save_path, image)
                    saved_count += 1
        frame += 1
        if frame > 500:
            break
    capture.release()

    return saved_count

def get_backgrounds(im):
    colours = {}

    for pixel in im.getdata():
        if pixel in colours.keys():
            colours[pixel] += 1
        else:
            colours[pixel] = 0
    x = sorted(colours.items(), key=(lambda i: i[1]))
    bg1 = x[-1][0]
    bg2 = x[-2][0]
    bg5 = x[-5][0]
    return bg1, bg2, bg5


def square_operations(square, bg):
    differences = {}
    directory = (BASE_DIR + '/static/images/chess_pieces')
    a = remove_background(square, bg[0], bg[1], bg[2])
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".png"):
            im2_src = os.path.join(directory, filename)
            im2 = Image.open(im2_src)
            difference = compare_images(a, im2)
            differences[filename] = difference

    x = min(differences.items(), key=operator.itemgetter(1))[0]
    if x == 'empty_square.png' and differences[x] > 5:
        differences['empty_square.png'] = 99
        x = min(differences.items(), key=operator.itemgetter(1))[0]

    return x


def imgcrop(input, xPieces, yPieces):
    differences = {}
    directory = (BASE_DIR + '/MainPage/static/images/chess_pieces')
    im = Image.open(input)
    backgrounds = get_backgrounds(im)

    imgwidth, imgheight = im.size
    height = imgheight/yPieces
    width = imgwidth/xPieces
    debug_position = []
    position = []
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            square = im.crop(box)
            g = square_operations(square, backgrounds)
            position.append(g)
            #a.save(filename + "-" + str(i) + "-" + str(j) + file_extension)

    notation = names_to_notation(position)
    #print(debug_position)`

    return notation


def remove_background(im, bg1, bg2, bg5):
    new_img_data = []
    # width, height = im.size
    # top_right = im.getdata()[width-1]
    # bt_left = im.getdata()[-1* width]
    # top_left = im.getdata()[0]
    if bg1[0] < bg2[0]:
        bg1, bg2 = bg2, bg1



    for pixel in im.getdata():
        if pixel == bg1 or pixel == bg2 or pixel == bg5:
            new_img_data.append(bg1)

        else:
            new_img_data.append(pixel)
    new_im = Image.new(im.mode, im.size)
    new_im.putdata(new_img_data)

    return new_im


def compare_images(i1, i2):

    size = i2.size
    i1 = i1.resize(size)

    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())

    dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    y = (dif / 255.0 * 100) / ncomponents
    return y




def names_to_notation(position):

    to_FEN_notation = {'white_rook.png': 'R', 'black_rook.png': 'r', 'white_bishop.png': 'B', 'black_bishop.png': 'b',
                       'white_queen.png': 'Q', 'black_queen.png': 'q','white_knight.png': 'N', 'black_knight.png': 'n',
                       'white_king.png':'K', 'black_king.png':'k', 'white_pawn.png': 'P', 'black_pawn.png': 'p',
                       'empty_square.png': 1}

    fen_notation = []
    for i in position:
        if i in to_FEN_notation.keys():
            fen_notation.append(to_FEN_notation[i])

    i = 8
    while i < len(fen_notation):
        fen_notation.insert(i, '/')
        i += (8 + 1)
    print(fen_notation)

    finished_fen = []
    value = 0
    repeated = False
    fen_notation.append('eh,lazy fix')
    for i in range(len(fen_notation)-1):
        if type(fen_notation[i]) == int and type(fen_notation[i + 1]) == int:
            repeated = True
            value += 1
        elif type(fen_notation[i]) != int:
            finished_fen.append(fen_notation[i])
        elif not repeated:
            finished_fen.append(value + 1)
            value = 0
        repeated = False


    print(finished_fen)
    stringify = ''.join([str(elem) for elem in finished_fen])
    return stringify

