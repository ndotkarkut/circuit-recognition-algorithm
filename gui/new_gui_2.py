from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FUNCTION DEFINITIONS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def screen_geometry(width,height):
    # Ensures the main window is always in 
    # the middle of the screen     
    screen_size =  (main.winfo_screenwidth(),main.winfo_screenheight())
    x = int(screen_size[0]/2 - width/2)
    y = int(screen_size[1]/2 - height/2)

    return f"{width}x{height}+{x}+{y}"

def upload():
    # Function to Ask User to Upload an Image
    global raw_img,raw_img_label
    global process_image_button

    filetypes = (("png","*.png"),("jpeg","*.jpg"),("bmp","*.bmp"),("all files","*.*"))
    main.filename =  filedialog.askopenfilename(title = "Select an Image",filetypes = filetypes)

    if main.filename:
        try:
            raw_img_label.grid_forget()
        except:
            pass   
        win_width = main.winfo_width() 
        win_height = main.winfo_height()
        temp_img = ImageTk.PhotoImage(Image.open(main.filename))
        img_width = temp_img.width()
        img_height = temp_img.height()

        if img_width >= 0.7*win_width:
            coeff = (0.5*win_width) / img_width 
            img_width = int(0.45*(win_width))
            img_height = int(coeff * img_height)

        if img_height >= 0.9*win_height:
            coeff = (0.5*win_height) / img_width 
            img_height = int(0.7*(win_height))
            img_width = int(coeff * img_width)


        raw_img = Image.open(main.filename).resize((img_width,img_height),Image.ANTIALIAS)
        raw_img = ImageTk.PhotoImage(raw_img)
        # raw_img = ImageTk.PhotoImage(Image.open(main.filename))
        raw_img_label = Label(image = raw_img)
        raw_img_label.grid(row = 1, column = 0,pady=20,sticky = "N")

        try:
            process_image_button.grid_forget()
        except:
            pass 
        process_image_button = Button(main,text="Process the Image",padx = 48, bd = '10',activebackground = "#00FF00",bg="#FFFFFF",font=button_fonts, command = process)
        process_image_button.grid(row = 0, column = 1,pady = 10,sticky = "N")  

def process():
        # Function to Ask User to Upload an Image
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

        if img_width >= 0.7*win_width:
            coeff = (0.5*win_width) / img_width 
            img_width = int(0.45*(win_width))
            img_height = int(coeff * img_height)

        if img_height >= 0.9*win_height:
            coeff = (0.5*win_height) / img_width 
            img_height = int(0.7*(win_height))
            img_width = int(coeff * img_width)


        raw_img1 = Image.open(main.filename).resize((img_width,img_height),Image.ANTIALIAS)
        raw_img1 = ImageTk.PhotoImage(raw_img1)
        # raw_img = ImageTk.PhotoImage(Image.open(main.filename))
        raw_img_label1 = Label(image = raw_img1)
        raw_img_label1.grid(row = 1, column = 1,pady=20,sticky = "N")
 
def resize(e):
    global bg_img1,resized_bg_img,new_bg
    global upload_image_button, process_image_button
    global upload_image_button_canvas,process_image_button_canvas

    # Resizing the Back Ground Image
    bg_img1 = Image.open("icons\\png_files\\background1.png")
    resized_bg_img = bg_img1.resize((e.width,e.height),Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg_img)
    main_canvas.create_image(0,0,image = new_bg, anchor = "nw")

    # Resizing the Buttons
    x_mulp = 0.2735
    y_mult = 0.0532

    new_x = e.width  * x_mulp
    new_y = e.height * y_mult
    

    # main_canvas.delete(upload_image_button_canvas)
    # main_canvas.delete(process_image_button_canvas)
    print(int(e.width/2 - new_x/2) )
    print(int(e.width/2 - new_x/2))
    print()

    upload_image_button_canvas = main_canvas.create_window(int(e.width/2 - new_x/2), 100, anchor = "center",window = upload_image_button)
    process_image_button_canvas = main_canvas.create_window(int(e.width/2 - new_x/2), 140,anchor = "n",window = process_image_button)
    # upload_image_button_canvas = main_canvas.create_window(int(e.width/2 - new_x/2), int(e.width/2 - new_x/2),window = upload_image_button)
    # process_image_button_canvas = main_canvas.create_window(int(e.width/2 - new_x/2), int(e.width/2 - new_x/2),window = process_image_button)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CREATING MAIN WINDOW
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
main = Tk()
main.title("CRA: Circuit Recognition Algorithm'")
main.geometry(screen_geometry(900,700))
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