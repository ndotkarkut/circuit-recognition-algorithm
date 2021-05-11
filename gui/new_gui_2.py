from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION DEFINITIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

    filetypes = (("png","*.png"),("jpeg","*.jpg"),("bmp","*.bmp"),("all files","*.*"))
    main.filename =  filedialog.askopenfilename(title = "Select an Image",filetypes = filetypes)

    if main.filename:
        try:
            raw_img_label.grid_forget()
            process_image_button.grid_forget()
        except:
            pass   

        raw_img = resize_image(Image.open(main.filename))
        raw_img = ImageTk.PhotoImage(raw_img)
        raw_img_label = Label(image = raw_img)
        raw_img_label.grid(row = 1, column = 0,pady=20,sticky = "N")

        process_image_button = Button(main,text="Process the Image",padx = 48, bd = '10',activebackground = "#00FF00",bg="#FFFFFF",font=button_fonts, command = process)
        process_image_button.grid(row = 0, column = 1,pady = 10,sticky = "N")  

# Runs through
def process():
    global raw_img1,raw_img_label1


    filetypes = (("png","*.png"),("jpeg","*.jpg"),("bmp","*.bmp"),("all files","*.*"))
    main.filename =  filedialog.askopenfilename(title = "Select an Image",filetypes = filetypes)

    if main.filename:
        try:
            raw_img_label1.grid_forget()
        except:
            pass   
        win_width = main.winfo_width() 
        win_height = main.winfo_height()
        temp_img1 = ImageTk.PhotoImage(Image.open(main.filename))
        img_width = temp_img1.width()
        img_height = temp_img1.height()

        raw_img1 = resize_image(Image.open(main.filename))
        raw_img1 = ImageTk.PhotoImage(raw_img1)
        # raw_img = ImageTk.PhotoImage(Image.open(main.filename))
        raw_img_label1 = Label(image = raw_img1)
        raw_img_label1.grid(row = 1, column = 1,pady=20,sticky = "N")
        raw_img_label2 = Label(image = raw_img1)
        raw_img_label2.grid(row = 2, column = 1,pady=20,sticky = "N")
 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATING MAIN WINDOW
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main = Tk()
main.title("CRA: Circuit Recognition Algorithm")
main.geometry(screen_geometry(950,800))
main.iconbitmap("icons\\1.ico")
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