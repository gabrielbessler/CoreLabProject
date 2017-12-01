from PIL import Image, ImageTk
import sys
from tkinter import filedialog
import tkinter as tk


LARGE_FONT = ("Verdana", 12)


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
        new_img = img
        return new_img

    def median_filter(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies a median filter on the specific range //'''
        new_img = img
        return new_img

    # TODO: make x_1 xmax, and y_1 ymax
    def box_blur(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Implements box blur on a given range '''
        if (x_1 > img.size[0] or y_1 > img.size[1]):
            print("Error - Out of Bounds")
            return

        if self.show_data:
            print(f"Box Blur Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")

        region = img.crop((x_0, y_0, x_1, y_1))
        region = region.transpose(Image.ROTATE_180)
        new_pic = img
        new_pic.paste(region, (x_0, y_0, x_1, y_1))
        return new_pic

    def gaussian_blur(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies a gaussian blur on the specified region '''
        new_img = img
        return new_img

    def flip(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Rotates the image by 180 degrees '''
        new_img = img
        return new_img

    def get_meta_data(self, img):
        '''
        Returns the format, size, and mode (RBG, etc.) associate with a PIL image
        object
        '''
        global show_data
        return (im.format, im.size, im.mode)

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
        ''' Creates the display for the frames in the photo editor '''
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames["StartPage"] = frame

        frame.grid(row=0, column=0, stick="nsew")
        self.show_frame("StartPage")

    def show_frame(self, controller):
        # Load the frame in from the dictionary where we store all frames
        frame = self.frames[controller]
        # Bring the frame to the front
        frame.tkraise()

    def set_size(self, width=500, height=500):
        pass


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        '''
        Creates the frame used for the StartPage (the main page in the program)
        '''

        self.parent = parent

        tk.Frame.__init__(self, parent, bg="#505050")

        label = tk.Label(self, text="Off-Brand Photoshop", font=LARGE_FONT, bg="#505050", fg="#ffffff")
        label.pack(padx=10, pady=10)

        label2 = tk.Label(self, text="Metadata: null", font=LARGE_FONT, bg="#505050", fg="#ffffff")
        label2.pack(padx=10, pady=10, side=tk.LEFT)

        button = tk.Button(self, text="Choose Image", command=self.choose_file, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button2 = tk.Button(self, text="Copy", command=self.copy_img, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button3 = tk.Button(self, text="Save", command=self.save, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button4 = tk.Button(self, text="Save as...", command=self.save_as, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button5 = tk.Button(self, text="Undo", command=self.undo, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)

        button.pack(padx=10, pady=10)
        button2.pack(padx=10, pady=10)
        button3.pack(padx=10, pady=10)
        button4.pack(padx=10, pady=10)
        button5.pack(padx=10, pady=10)

        self.curr_image = Image.open("C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg") \
            .resize((500, 500), Image.ANTIALIAS)
        self.prev_image = None
        self.curr_dir = "C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg"
        self.prev_dir = None

        self.tkimg = ImageTk.PhotoImage(self.curr_image)
        self.prev_tkimg = None

        self.panel = tk.Label(self, image=self.tkimg)
        self.panel.pack(padx=20)

        button2 = tk.Button(self, text="Box Blur", command=self.box_blur, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button2.pack(side=tk.LEFT, padx=20, pady=10)

        button3 = tk.Button(self, text="Gaussian Blur", command=self.gaussian_blur, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button4 = tk.Button(self, text="Flip", command=self.flip, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button5 = tk.Button(self, text="Unsharp Masking", command=self.unsharp_masking, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        button6 = tk.Button(self, text="Median Filter", command=self.median_filter, bg="#000099", fg="#ffffff", borderwidth=0, padx=5, pady=5)
        # Pack all
        for i in [button3, button4, button5, button6]:
            i.pack(side=tk.LEFT, padx=20)

        self.editor = PhotoEditor("C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg")

    def undo(self):
        if self.prev_dir != None:
            update_image(self.prev_dir)

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
        self.update_image(new_image)

    def median_filter(self):
        ''' Calls the median filter function in the photo editor class '''
        new_image = self.editor.median_filter(self.curr_image)
        self.update_image(new_image)

    def box_blur(self):
        ''' Calls the box_blur function in the photo editor class '''
        new_image = self.editor.box_blur(self.curr_image)
        self.update_image(new_image)

    def gaussian_blur(self):
        ''' Calls the gaussian function in the photo editor class '''
        new_image = self.editor.gaussian_blur(self.curr_image)
        self.update_image(new_image)

    def flip(self):
        ''' Calls the flip function in the photo editor class '''
        new_image = self.editor.flip(self.curr_image)
        self.update_image(new_image)

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
                .resize((500, 500), Image.ANTIALIAS)
        else:
            self.curr_dir = self.prev_dir
            self.curr_image = image_name

        self.tkimg = ImageTk.PhotoImage(self.curr_image)
        self.panel.config(image=self.img)

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
        elif i[:2] == 'h':
            pic_height = i[3:]

    photo_editor = PhotoGUI()
    photo_editor.set_size(pic_width, pic_height)
    photo_editor.title("Photoshep")
    photo_editor.iconbitmap("icon.ico")
    photo_editor.mainloop()


if __name__ == "__main__":
    init()
