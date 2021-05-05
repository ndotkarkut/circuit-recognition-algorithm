import tkinter as tk
from tkinter import *
import tkinter.font as font
import tkinter.filedialog
import cv2 as cv2
from PIL import ImageTk, Image
import os
import subprocess
import sys

# iimg = cv2.imread('../circuit1.jpg')
# cv2.imshow('image', iimg)
# cv2.waitKey(0)
browseFile = None


def select_image():
    global img, browseFile
    browseFile = tk.filedialog.askopenfilename()
    print(browseFile)

    if len(browseFile) > 0:
        raw_img = cv2.imread(browseFile)
        x_dim, y_dim, z_dim = raw_img.shape

        pil_img = Image.open(browseFile)
        resized_pil_img = pil_img.resize((int(x_dim / 4), int(y_dim / 4)))
        # raw_img.resize((1, 1), Image.NEAREST)
        # loading the image
        img = ImageTk.PhotoImage(resized_pil_img)

        # arranging application parameters
        canvas = tk.Canvas(main_window, width=250, height=250)

        # arranging application parameters
        # canvas = tk.Canvas(main_window, width=x_dim, height=y_dim)
        canvas.create_image(135, 0, anchor=N, image=img)
        canvas.pack()


def run_proc():
    global browseFile
    global prediction_img

    if browseFile != None:
        yolo_process = ['./darknet', 'detector', 'test', 'objsenior_new.data', 'yolov4-objsenior_new.cfg',
                        'yolov4-objsenior_last_new.weights', '-dont_show', '-ext_output', '-out', 'results.json', str(browseFile)]

        # result = subprocess.run([sys.executable, "-c", "print('ocean')"])
        result = subprocess.run(yolo_process, check=True,
                                cwd='..', stdout=subprocess.PIPE)
        
        # write result into output file to be used for finding the recognized boxes 
        with open('../predictions.txt', 'w') as out_file:
            out_file.write(result.stdout.decode())

        # print(result.stdout)
        
        raw_img = cv2.imread('../predictions.jpg')
        x_dim, y_dim, z_dim = raw_img.shape

        pil_img = Image.open('../predictions.jpg')
        resized_pil_img = pil_img.resize((int(x_dim / 4), int(y_dim / 4)))

        # loading the image
        prediction_img = ImageTk.PhotoImage(resized_pil_img)

        # arranging application parameters
        pred_canvas = tk.Canvas(main_window, width=250, height=250)

        # arranging application parameters
        # canvas = tk.Canvas(main_window, width=x_dim, height=y_dim)
        pred_canvas.create_image(135, 0, anchor=N, image=prediction_img)
        pred_canvas.pack()
    else:
        print('No image uploaded. Please upload an image')
        return


main_window = tk.Tk()
main_window.geometry('750x750')
main_window.title('CRA: Circuit Recognition Algorithm')


# main label for image upload
label_font = font.Font(family='Calibri', size=25)
upload_label = tk.Label(
    main_window, text='Upload your circuit image now', font=label_font)
upload_label.pack()

# button to submit uploaded image
upload_button = Button(main_window, text='Upload Image', command=select_image, width=50,
                       height=4, bg='#33CC33', fg='#FFFFFF')
upload_button.pack()

# button to run image processing
proc_button = Button(main_window, text='Process Image', command=run_proc, width=50,
                     height=4, bg='#33CC33', fg='#FFFFFF')
proc_button.pack()

# # arranging application parameters
# canvas = tk.Canvas(main_window, width=500, height=250)

# # arranging image parameters in the application
# canvas.create_image(135, 20, anchor=S, image=img)
# canvas.pack()

main_window.mainloop()
