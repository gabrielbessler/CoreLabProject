from PIL import Image, ImageTk
import sys
from tkinter import filedialog
import tkinter as tk
import cv2
import random

# cv2 - opencv (used for image processing)
import numpy as np

LARGE_FONT = ("Trebuchet MS", 14)
FONT_SMALL = ("Trebuchet MS", 1)


class PhotoEditor():

    def __init__(self, name=""):
        ''' Initializes the photo editor '''
        self.show_data = False
        self.show_output = False
        self.check_arguments()
        self.disp("Creating GUI...")

        # Gets the image name from the user, and then displays the image
        if name == "":
            self.get_from_user()

        if self.show_output:
            img.show()

    def get_from_user(self):
        ''' Uses the terminal to get an image name from the user '''
        while True:
            img_name = input("What is the name of the picture? ")
            try:
                img = Image.open(img_name)
                break
            except Exception as e:
                print(f"Could not find image {img_name}. Error Code: {e}")

    def unsharp_masking(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies an unsharp masking on the given range '''
        self.disp(f"Unsharp Masking Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")

        new_img = img
        return new_img

    def median_filter(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies a median filter on the specific range //'''
        self.disp(f"Median Filter Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        open_cv_image = np.array(new_img) #convert the image to a format that can be use by open_cv
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.medianBlur(open_cv_image, 3)

        # convert into Image
        im = Image.fromarray(blur)
        return im

    # TODO: make x_1 xmax, and y_1 ymax
    def box_blur(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Implements box blur on a given range '''
        self.disp(f"Box Blur Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        open_cv_image = np.array(new_img) #convert the image to a format that can be use by open_cv
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.boxFilter(open_cv_image, -1, (3,3))

        # convert into Image
        im = Image.fromarray(blur)
        return im

    def add_noise(self, img, num_times=25000):
        pix = img.load()
        pix[0, 0] = (0, 0, 0)
        for i in range(num_times):
            y = random.randint(0, img.size[0]-1)
            x = random.randint(0, img.size[1]-1)
            try:
                if random.randint(0, 1) == 0:
                    pix[y, x] = (255, 255, 255)
                else:
                    pix[y, x] = (0, 0, 0)
            except:
                print(x, y)

        return img

    def gaussian_blur(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies a gaussian blur on the specified region '''
        self.disp(f"Gaussian Blur Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        open_cv_image = np.array(new_img) #convert the image to a format that can be use by open_cv
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.GaussianBlur(open_cv_image, (5, 5), 3)

        # convert into Image
        im = Image.fromarray(blur)
        return im

    def flip(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Rotates the image by 180 degrees '''
        self.disp(f"Flip Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")

        if (x_1 > img.size[0] or y_1 > img.size[1]):
            print("Error - Out of Bounds")
            return

        region = img.crop((x_0, y_0, x_1, y_1))
        region = region.transpose(Image.ROTATE_180)
        new_pic = img
        new_pic.paste(region, (x_0, y_0, x_1, y_1))
        return new_pic

    def get_meta_data(self, img):
        '''
        Returns the format, size, and mode (RBG, etc.) associate with a PIL image
        object
        '''
        global show_data
        return f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}"

    def check_arguments(self):
        ''' Checks for the arguments written in CMD '''
        if '-v' in sys.argv or '--verbose' in sys.argv:
            self.show_data = True
            print("In verbose mode")

        if '-s' in sys.argv or '--show_output' in sys.argv:
            self.show_output = True

    def disp(self, msg):
        if self.show_data:
            print(msg)


class PhotoGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.b_key = False  # Box blur
        self.g_key = False  # Gauss blur
        self.f_key = False  # Flip
        self.u_key = False  # Unsharp Masking
        self.m_key = False  # Median Filter

        ''' Creates the display for the frames in the photo editor '''
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        frame.bind("<KeyPress>", self.key_down)
        frame.bind("<KeyRelease>", self.key_up)
        frame.bind("<Button-1>", self.press)
        frame.bind("<Button-3>", self.right_click)

        self.frames["StartPage"] = frame

        frame.grid(row=0, column=0, stick="nsew")
        self.show_frame("StartPage")

    def key_down(self, event):
        ''' Prints out keys pressed on the StartPage '''
        # TODO: optimize using dictionary
        if event.char == "b":
            if not self.b_key:
                self.frames["StartPage"].box_blur()
            self.b_key = True
        elif event.char == "g":
            if not self.g_key:
                self.frames["StartPage"].gaussian_blur()
            self.g_key = True
        elif event.char == "f":
            if not self.f_key:
                self.frames["StartPage"].flip()
            self.f_key = True
        elif event.char == "u":
            if not self.u_key:
                self.frames["StartPage"].unsharp_masking()
            self.u_key = True
        elif event.char == "m":
            if not self.m_key:
                self.frames["StartPage"].median_filter()
            self.m_key = True

    def key_up(self, event):
        if event.char == "b":
            self.b_key = False
        elif event.char == "g":
            self.g_key = False
        elif event.char == "f":
            self.f_key = False
        elif event.char == "u":
            self.u_key = False
        elif event.char == "m":
            self.m_key = False

    def press(self, event):
        ''' Prints out the location of mouse clicks on the StartPage '''
        # frame.focus_set() TODO
        print("left at", event.x, event.y)

    def right_click(self, event):
        print("right click at", event.x, event.y)

    def show_frame(self, controller):
        # Load the frame in from the dictionary where we store all frames
        frame = self.frames[controller]
        # Bring the frame to the front
        frame.tkraise()
        frame.focus_set()  # TODO: Why does this work?

    def set_size(self, width=500, height=500):
        self.width = width
        self.height = height
        self.frames["StartPage"].set_size(self.width, self.height)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        '''
        Creates the frame used for the StartPage (the main page in the program)
        '''

        self.parent = parent
        self.width = 500
        self.height = 500

        tk.Frame.__init__(self, parent, bg="#EEEEEE")

        label = tk.Label(self, text="Off-Brand Photoshop", font=LARGE_FONT, bg="#EEEEEE", fg="#4286f4")
        label.grid(row=0, column=0, sticky="W", padx=(15,0) )

        button = tk.Button(self, text="Choose Image", command=self.choose_file, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=10, pady=6)
        button2 = tk.Button(self, text="Copy", command=self.copy_img, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=15, pady=6)
        button3 = tk.Button(self, text="Save", command=self.save, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=10, pady=6)
        button4 = tk.Button(self, text="Save as...", command=self.save_as, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=10, pady=6)
        button5 = tk.Button(self, text="Undo", command=self.undo, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=10, pady=6)

        button.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button2.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button2.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button3.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button3.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button4.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button4.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button5.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button5.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))

        button.grid(row=0, column=5, padx=0, pady=(15,10), sticky="E")
        button2.grid(row=0, column=6, padx=0, pady=(15,10), sticky="E")
        button3.grid(row=0, column=7, padx=0, pady=(15,10), sticky="E")
        button4.grid(row=0, column=8, padx=0, pady=(15,10), sticky="E")
        button5.grid(row=0, column=9, padx=(0, 14), pady=(15,10), sticky="E")

        self.curr_image = Image.open("C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg") \
            .resize((self.width, self.width), Image.ANTIALIAS)
        self.prev_image = None
        self.curr_dir = "C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg"
        self.prev_dir = None

        self.tkimg = ImageTk.PhotoImage(self.curr_image)
        self.prev_tkimg = None

        self.panel = tk.Label(self, image=self.tkimg, bd=0)
        self.panel.grid(row=1, column=0, pady=6, padx=15, columnspan=10, rowspan=15)

        button6 = tk.Button(self, text="Box Blur", command=self.box_blur, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=28, pady=5)
        button7 = tk.Button(self, text="Gaussian Blur", command=self.gaussian_blur, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=15, pady=5)
        button8 = tk.Button(self, text="Flip", command=self.flip, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=40, pady=5)
        button9 = tk.Button(self, text="Unsharp Masking", command=self.unsharp_masking, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=5, pady=5)
        button10 = tk.Button(self, text="Median Filter", command=self.median_filter, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=15, pady=5)
        button11 = tk.Button(self, text="Add Noise", command=self.add_noise, bg="#4286f4", fg="#ffffff", borderwidth=1, padx=22, pady=5)

        button6.grid(row=1, column=10, padx=(0, 14), pady=0)
        button7.grid(row=2, column=10, padx=(0, 14), pady=5)
        button8.grid(row=3, column=10, padx=(0, 14), pady=0)
        button9.grid(row=4, column=10, padx=(0, 14), pady=5)
        button10.grid(row=5, column=10, padx=(0, 14), pady=0)
        button11.grid(row=6, column=10, padx=(0, 14), pady=5)

        button6.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button6.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button7.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button7.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button8.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button8.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button9.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button9.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button10.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button10.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))
        button11.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
        button11.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))

        self.w = tk.Scale(self, from_=0, to=250000)
        self.w.grid(row=7, column=10, padx=0, pady=0)

        label_one = tk.Label(self, text="X-Start: ", font=LARGE_FONT, bg="#505050", fg="#ffffff")
        label_two = tk.Label(self, text="X-End: ", font=LARGE_FONT, bg="#505050", fg="#ffffff")
        label_three = tk.Label(self, text="Y-Start: ", font=LARGE_FONT, bg="#505050", fg="#ffffff")
        label_four = tk.Label(self, text="Y-End: ", font=LARGE_FONT, bg="#505050", fg="#ffffff")

        self.editor = PhotoEditor("C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg")
        self.label2 = tk.Label(self, text="Metadata: null", font=LARGE_FONT, bg="#EEEEEE", fg="#4286f4")
        self.label2.grid(row=16, column=0, pady=0, columnspan=10)

        label_new = tk.Label(self, text=" ", font=FONT_SMALL, bg="#EEEEEE", fg="#4286f4")
        label_new.grid(row=17, column=0, sticky="W", pady=0)

        self.update_metadata()

    def set_size(self, width, height):
        self.width = width
        self.height = height
        self.update_image(self.curr_dir)

    def update_metadata(self):
        self.label2.config(text=f"{self.editor.get_meta_data(self.curr_image)}")

    def add_noise(self):
        new_image = self.editor.add_noise(self.curr_image, self.w.get())
        self.update_image(new_image, mode="2")

    def undo(self):
        if self.prev_dir is not None:
            self.update_image(self.prev_dir)

    def copy_img(self):
        ''' '''
        self.parent.clipboard_clear()
        self.parent.clipboard_append('Copying picture')
        self.parent.update()

    def save(self, filename=""):
        ''' '''
        pass

    def save_as(self):
        ''' '''
        pass

    def unsharp_masking(self):
        '''  Calls the unsharp masking function in the photo editor class '''
        new_image = self.editor.unsharp_masking(self.curr_image)
        self.update_image(new_image, mode="2")

    def median_filter(self):
        ''' Calls the median filter function in the photo editor class '''
        new_image = self.editor.median_filter(self.curr_image)
        self.update_image(new_image, mode="2")

    def box_blur(self):
        ''' Calls the box_blur function in the photo editor class '''
        new_image = self.editor.box_blur(self.curr_image)
        self.update_image(new_image, mode="2")

    def gaussian_blur(self):
        ''' Calls the gaussian function in the photo editor class '''
        new_image = self.editor.gaussian_blur(self.curr_image)
        self.update_image(new_image, mode="2")

    def flip(self):
        ''' Calls the flip function in the photo editor class '''
        new_image = self.editor.flip(self.curr_image)
        self.update_image(new_image, mode="2")

    def update_image(self, image_name, mode="Image Name"):
        ''' Given an image_name, displays the new picture and updates all of the variables
        in the current frame '''
        # Store the old data
        self.prev_image = self.curr_image
        self.prev_dir = self.curr_dir
        self.prev_tkimg = self.tkimg

        if mode == "Image Name":
            # Set the new data
            self.curr_dir = image_name
            self.curr_image = Image.open(image_name) \
                .resize((int(self.width), int(self.height)), Image.ANTIALIAS)
        else:
            self.curr_dir = self.prev_dir
            self.curr_image = image_name

        self.tkimg = ImageTk.PhotoImage(self.curr_image)
        self.panel.config(image=self.tkimg)
        self.update_metadata()

    def choose_file(self):
        ''' Opens that dialog that lets the user put in a file name, and then
        updates the image accordingly '''
        filename = filedialog.askopenfilename(initialdir="/", title="Select \
            file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.update_image(filename)


def init():
    ''' Initializes the GUI for the photo editor '''
    pic_width = 500
    pic_height = 500
    for i in sys.argv:
        if i[:2] == "-w":
            pic_width = i[3:]
        elif i[:2] == '-h':
            pic_height = i[3:]

    photo_editor = PhotoGUI()
    photo_editor.set_size(pic_width, pic_height)
    photo_editor.frames['StartPage'].update_image(photo_editor.frames['StartPage'].curr_image, mode="2")
    photo_editor.title("Photoshep - 17 Day Free Trial (12 flex dollars to purchase) ")
    photo_editor.iconbitmap("icon.ico")
    photo_editor.mainloop()


if __name__ == "__main__":
    init()
