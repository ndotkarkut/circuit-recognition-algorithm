from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
import subprocess

from numpy.core.fromnumeric import resize

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION DEFINITIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
img_path = ''

# Define the size of the main Window
# And Ensure it's always in the middle
def screen_geometry(width,height):

    screen_size =  (main.winfo_screenwidth(),main.winfo_screenheight())
    x = int(screen_size[0]/2 - width/2)
    y = int(screen_size[1]/2 - height/2)

    return f"{width}x{height}+{x}+{y}"

# Resize Uploaded image to fit the size of the main window
def resize_image(raw_image):

    win_width, win_height = main.winfo_width(), main.winfo_height()
    img_width, img_height = raw_image.size

    if img_width >= 0.7*win_width:
        coeff = (0.5*win_width) / img_width 
        img_width = int(0.45*(win_width))
        img_height = int(coeff * img_height)

    if img_height >= 0.8*win_height:
        coeff = (0.5*win_height) / img_width 
        img_height = int(0.7*(win_height))
        img_width = int(coeff * img_width)
 
    resized_image = raw_image.resize((img_width,img_height),Image.ANTIALIAS)
    return resized_image

# Prompts user to upload an Image
def upload():
    
    global raw_img,raw_img_label
    global process_image_button
    global img_path

    filetypes = (("png","*.png"),("jpeg","*.jpg"),("bmp","*.bmp"),("all files","*.*"))
    #main.filename =  filedialog.askopenfilename(title = "Select an Image",filetypes = filetypes)
    img_path = filedialog.askopenfilename(title="Select an Image", filetypes=filetypes)

    # if main.filename:
    if img_path:
        try:
            raw_img_label.grid_forget()
            process_image_button.grid_forget()
        except:
            pass   

        raw_img = resize_image(Image.open(img_path))
        raw_img = ImageTk.PhotoImage(raw_img)
        raw_img_label = Label(main, image = raw_img)
        raw_img_label.grid(row = 1, column = 0,pady=20,sticky = "N")

        process_image_button = Button(main,text="Process the Image",padx = 48, bd = '10',activebackground = "#00FF00",bg="#FFFFFF",font=button_fonts, command = process)
        process_image_button.grid(row = 0, column = 1,pady = 10,sticky = "N")  

# Runs through
def process():
    global img_path
    global final_image
    global final_img_label, output_img_label
    
    print(img_path)
    try:
        final_img_label.grid_forget()
        output_img_label.grid_forget()
    except:
        pass
    
    yolo_process = ['./darknet', 'detector', 'test', 'objsenior_new.data', 'yolov4-objsenior_new.cfg',
                    'yolov4-objsenior_last_new2.weights', '-dont_show', '-ext_output', '-out', 'results.json', str(img_path)]

    # result = subprocess.run([sys.executable, "-c", "print('ocean')"])
    result = subprocess.run(yolo_process, check=True,
                            cwd='..', stdout=subprocess.PIPE)
    
    # write result into output file to be used for finding the recognized boxes 
    with open('../predictions.txt', 'w') as out_file:
        out_file.write(result.stdout.decode())
    
    imaging_process = ['python3', '../img_proc/test.py', f'-path={img_path}']
    
    output = subprocess.run(imaging_process, cwd='.', check=True, stdout=subprocess.PIPE)
    print(output.stdout.decode())
    final_image = resize_image(Image.open("../finished_image.png"))
    final_image = ImageTk.PhotoImage(final_image)
    final_img_label = Label(main, image=final_image)
    final_img_label.grid(row=1, column=1, pady=20, sticky="N")
    
    output_img_label = Label(main, text=output.stdout)
    output_img_label.grid(row=2, column=1, pady=20, sticky="N")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATING MAIN WINDOW
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main = Tk()
main.title("CRA: Circuit Recognition Algorithm")
main.geometry(screen_geometry(950,800))
# main.iconbitmap("./icons/2.ico")

Grid.columnconfigure(main,0,weight=1)
Grid.columnconfigure(main,1,weight=1)
main.configure(bg='#A9A9A9')
# Grid.rowconfigure(main,0,weight=1)
# Grid.rowconfigure(main,1,weight=1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# BUTTONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
button_fonts = ("Helvetica",15,"bold")

upload_image_button = Button(main,text="Upload Image", padx = 72,bd = '10',activebackground = "#00FF00",bg="#FFFFFF",font=button_fonts, command = upload)
upload_image_button.grid(row = 0, column = 0,pady = 10,sticky = "N")

process_image_button = Button(main,text="Process the Image",padx = 48, bd = '10',activebackground = "#00FF00",bg="#FFFFFF",font=button_fonts, command = process, state = DISABLED)
process_image_button.grid(row = 0, column = 1,pady = 10,sticky = "N")  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main.mainloop()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~