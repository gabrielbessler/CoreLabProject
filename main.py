
from tkinter import filedialog
from PIL import Image, ImageTk
from scipy import linalg
import tkinter as tk
import numpy as np
import random
import sys
import cv2

LARGE_FONT = ("Trebuchet MS", 14)
FONT_SMALL = ("Trebuchet MS", 1)

# BUG 1: Does not working when running through iPython


class SVDCompression():

    def __init__(self, img, k_value):
        ''' Initializes the SVD compressor by taking in
        the image and necessary k value '''
        self.image = img
        self.k_val = k_value

    def do_svd(self):
        # TODO
        new_image = self.RGB_to_greyscale()
        eigenvalues = self.get_eigenvalues(new_image.load())
        singularvalues = self.eigenvalues_to_singularvalues(eigenvalues)

    def RGB_to_greyscale(self):
        ''' Takes an image in the standard RGB format
        and returns a representation of the image in
        grayscale by averaging the red, green, and blue
        values '''
        size = self.image.size
        new_image = self.image
        pix = new_image.load()
        for x in range(size[0]):
            for y in range(size[1]):
                new_value = sum(pix[x, y]) // 3
                pix[x, y] = (new_value, new_value, new_value)

        # now we have the grayscale image in np_array
        np_array = np.array(new_image, dtype=np.float64)[:, :, 0]

        U, sigma, V = np.linalg.svd(np_array)

        for i in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
            reconstimg = np.matrix(U[:, :i]) * np.diag(sigma[:i]) * np.matrix(V[:i, :])
            m.pyplot.imshow(reconstimg, cmap='gray')
            m.pyplot.title = "n = %s" % i
            m.pyplot.title(title)
            m.pyplot.plt.show()

        # TEMPORARY - TODO: REMOVE
        np_array = np.array(new_image, dtype=np.float64)[:, :, 0]
        np_array_t = np_array.transpose()
        # square_boi = np_array * np_array_t
        square_boi = np.dot(np_array.transpose(), np_array)
        L = self.get_eigenvalues(square_boi)
        eigenvalues, eigenvectors = (L[0], L[1])
        singular_values = self.eigenvalues_to_singularvalues(eigenvalues)

        return new_image

    def get_eigenvalues(self, M):
        ''' Takes some NxN list (matrix) M and returns all of its eigenvalues '''
        return linalg.eigh(M)

    def eigenvalues_to_singularvalues(self, L):
        ''' Takes a list of eigevalues and then converts them to
            singular values in decreasing order '''
        try:
            return sorted([i**.5 for i in L])[::-1]
        except:
            raise ValueError()


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
        open_cv_image = np.array(new_img)  # convert the image to a format that
        # can be used by open_cv
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.GaussianBlur(open_cv_image, (5, 5), 10.0)
        # Takes weighted sum of two arrays
        unsharp_image = cv2.addWeighted(open_cv_image, 1.5, blur, -0.5, 0,
                                        open_cv_image)

        # Convert into Image
        im = Image.fromarray(unsharp_image)
        return im

    def custom_kernel(self, img, kernel, scale=1):
        self.disp(f"{kernel} colved on img")
        new_img = img
        # Convert the image to a format that can be use by open_cv
        open_cv_image = np.array(new_img)
        # Open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR
        blur = cv2.filter2D(open_cv_image, -1, scale*kernel)

        # Convert into Image
        im = Image.fromarray(blur)
        return im

    def median_filter(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Applies a median filter on the specific range //'''
        self.disp(f"Median Filter Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        # Convert the image to a format that can be use by open_cv
        open_cv_image = np.array(new_img)
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.medianBlur(open_cv_image, 3)

        # Convert into Image
        im = Image.fromarray(blur)
        return im

    def box_blur(self, img, x_0=0, y_0=0, x_1=500, y_1=500):
        ''' Implements box blur on a given range '''
        self.disp(f"Box Blur Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        # Convert the image to a format that can be use by open_cv
        open_cv_image = np.array(new_img)
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.boxFilter(open_cv_image, -1, (3, 3))

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
        # Convert the image to a format that can be use by open_cv
        open_cv_image = np.array(new_img)

        # cv2.getGaussianKernel() will show the kernel used for this
        blur = cv2.GaussianBlur(open_cv_image, (5, 5), 3)

        # convert into Image
        im = Image.fromarray(blur)
        return im

    def bilateral_filter(self, img, x_0=0, y_0=0, x_1=800, y_1=600):
        self.disp(f"Gaussian Blur Applied on ({x_0}, {y_0}), ({x_1}, {y_1})")
        new_img = img
        open_cv_image = np.array(new_img)  # convert the image to a format that
        #  can be use by open_cv
        # open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR

        blur = cv2.bilateralFilter(open_cv_image, 20, 15, 80, 80)

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
        Returns the format, size, and mode (RBG, etc.) associate with a PIL
        image object
        '''
        return f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}"

    def check_arguments(self):
        ''' Checks for the arguments written in CMD '''
        if '-v' in sys.argv or '--verbose' in sys.argv:
            self.show_data = True
            print("In verbose mode")

        if '-s' in sys.argv or '--show_output' in sys.argv:
            self.show_output = True

    def disp(self, msg):
        ''' Print out data '''
        if self.show_data:
            print(msg)


class PhotoGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        ''' Creates the main Tkinter GUI '''
        # Box Blur, Gauss Blur, Flip, Unsharp Masking, Median Filter, Add Noise
        # SVDCompression
        self.keys = {'b_key': False, 'g_key': False, 'f_key': False,
                     'u_left': False, 'm_left': False, 'a_key': False,
                     'z_key': False, 'x_key': False, 'i_key': False,
                     'c_key': False, 's_key': False}

        # Creates the display for the frames
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a variable to store all of the frames in
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
        if event.char == "b":
            if not self.keys['b_key']:
                self.frames["StartPage"].box_blur()
            self.keys['b_key'] = True
        elif event.char == "g":
            if not self.keys['g_key']:
                self.frames["StartPage"].gaussian_blur()
            self.keys['g_key'] = True
        elif event.char == "f":
            if not self.keys['f_key']:
                self.frames["StartPage"].flip()
            self.keys['f_key'] = True
        elif event.char == "u":
            if not self.keys['u_key']:
                self.frames["StartPage"].unsharp_masking()
            self.keys['u_key'] = True
        elif event.char == "m":
            if not self.keys['m_key']:
                self.frames["StartPage"].median_filter()
            self.keys['m_key'] = True
        elif event.char == "z":
            if not self.keys['z_key']:
                print("increasing noise")
            self.keys['z_key'] = True
        elif event.char == 'x':
            if not self.keys['x_key']:
                print("decreasing noise")
            self.keys['x_key'] = True
        elif event.char == 'i':
            if not self.keys['i_key']:
                self.frames["StartPage"].bilateral_filter()
        elif event.char == 'c':
            if not self.keys['c_key']:
                self.frames["StartPage"].custom_kernel()
        elif event.char == 's':
            if not self.keys['s_key']:
                self.frames["StartPage"].svd()

    def key_up(self, event):
        ''' Runs whenever any key is pressed and the main display is on focus
        '''
        if event.char == "b":
            self.keys['b_key'] = False
        elif event.char == "g":
            self.keys['g_key'] = False
        elif event.char == "f":
            self.keys['f_key'] = False
        elif event.char == "u":
            self.keys['u_key'] = False
        elif event.char == "m":
            self.keys['m_key'] = False
        elif event.char == "z":
            self.keys['z_key'] = False
        elif event.char == 'x':
            self.keys['x_key'] = False
        elif event.char == "i":
            self.keys['i_key'] = False
        elif event.char == "c":
            self.keys['c_key'] = False
        elif event.char == "s":
            self.keys['s_key'] = False

    def press(self, event):
        ''' Prints out the location of mouse clicks on the StartPage '''
        print("left at", event.x, event.y)

    def right_click(self, event):
        ''' Runs every time the right mouse button is pressed '''
        print("right click at", event.x, event.y)

    def show_frame(self, controller):
        ''' Shows the given frame '''
        # Load the frame in from the dictionary where we store all frames
        frame = self.frames[controller]
        # Bring the frame to the front
        frame.tkraise()
        frame.focus_set()

    def set_size(self, width=500, height=500):
        ''' Takes a width and height and sets the startPage frame to that size
        '''
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
        self.BUTTON_COLOR = "#4286f4"
        self.BUTTON_HIGHLIGHT = "#ffffff"

        tk.Frame.__init__(self, parent, bg="#EEEEEE")

        label = tk.Label(self, text="Off-Brand Photoshop", font=LARGE_FONT,
                         bg="#EEEEEE", fg=self.BUTTON_COLOR)
        label.grid(row=0, column=0, sticky="W", padx=(15, 0))

        button = tk.Button(self, text="Choose Image", command=self.choose_file,
                           bg=self.BUTTON_COLOR, fg=self.BUTTON_HIGHLIGHT,
                           borderwidth=1, padx=10, pady=6)
        button2 = tk.Button(self, text="Copy", command=self.copy_img,
                            bg=self.BUTTON_COLOR, fg=self.BUTTON_HIGHLIGHT,
                            borderwidth=1, padx=15, pady=6)
        button3 = tk.Button(self, text="Save", command=self.save,
                            bg=self.BUTTON_COLOR, fg=self.BUTTON_HIGHLIGHT,
                            borderwidth=1, padx=10, pady=6)
        button4 = tk.Button(self, text="Save as...", command=self.save_as,
                            bg=self.BUTTON_COLOR, fg=self.BUTTON_HIGHLIGHT,
                            borderwidth=1, padx=10, pady=6)
        button5 = tk.Button(self, text="Undo", command=self.undo,
                            bg=self.BUTTON_COLOR, fg=self.BUTTON_HIGHLIGHT,
                            borderwidth=1, padx=10, pady=6)

        for i in [button, button2, button3, button4, button5]:
            i.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
            i.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))

        button_padding = (15, 10)

        button.grid(row=0, column=5, padx=0, pady=button_padding,
                    sticky="E")
        button2.grid(row=0, column=6, padx=0, pady=button_padding,
                     sticky="E")
        button3.grid(row=0, column=7, padx=0, pady=button_padding,
                     sticky="E")
        button4.grid(row=0, column=8, padx=0, pady=button_padding,
                     sticky="E")
        button5.grid(row=0, column=9, padx=(0, 14), pady=button_padding,
                     sticky="E")

        demo_dir = "C:/Users/Gabe/Documents/Programming/Photoshep/demo1.jpg"

        self.curr_image = Image.open(demo_dir) \
            .resize((self.width, self.width), Image.ANTIALIAS)
        self.prev_image = None
        self.curr_dir = demo_dir
        self.prev_dir = None

        self.tkimg = ImageTk.PhotoImage(self.curr_image)
        self.prev_tkimg = None

        self.panel = tk.Label(self, image=self.tkimg, bd=0)
        self.panel.grid(row=1, column=0, pady=6, padx=15, columnspan=10,
                        rowspan=15)

        button6 = tk.Button(self, text="Box Blur", command=self.box_blur,
                            bg="#4286f4", fg="#ffffff", borderwidth=1, padx=28,
                            pady=5)
        button7 = tk.Button(self, text="Gaussian Blur",
                            command=self.gaussian_blur, bg="#4286f4",
                            fg="#ffffff", borderwidth=1, padx=15, pady=5)
        button8 = tk.Button(self, text="Rotate180", command=self.flip,
                            bg="#4286f4", fg="#ffffff", borderwidth=1,
                            padx=20, pady=5)
        button9 = tk.Button(self, text="Unsharp Masking",
                            command=self.unsharp_masking, bg="#4286f4",
                            fg="#ffffff", borderwidth=1, padx=5, pady=5)
        button10 = tk.Button(self, text="Median Filter",
                             command=self.median_filter, bg="#4286f4",
                             fg="#ffffff", borderwidth=1, padx=15, pady=5)
        button12 = tk.Button(self, text="Bilateral Filter",
                             command=self.bilateral_filter, bg="#4286f4",
                             fg="#ffffff", borderwidth=1, padx=15, pady=5)
        button11 = tk.Button(self, text="Add Noise", command=self.add_noise,
                             bg="#4286f4", fg="#ffffff", borderwidth=1,
                             padx=22, pady=5)
        button13 = tk.Button(self, text="Custom Kernel",
                             command=self.kernel_custom, bg="#4286f4",
                             fg="#ffffff", borderwidth=1, padx=13, pady=5)
        button14 = tk.Button(self, text="SVD Compression",
                             command=self.svd, bg="#4286f4",
                             fg="#ffffff", borderwidth=1, padx=13, pady=5)

        button6.grid(row=1, column=10, padx=(0, 14), pady=0)
        button7.grid(row=2, column=10, padx=(0, 14), pady=5)
        button8.grid(row=3, column=10, padx=(0, 14), pady=0)
        button9.grid(row=4, column=10, padx=(0, 14), pady=5)
        button10.grid(row=5, column=10, padx=(0, 14), pady=0)
        button11.grid(row=6, column=10, padx=(0, 14), pady=5)
        button12.grid(row=7, column=10, padx=(0, 14), pady=5)
        button13.grid(row=8, column=10, padx=(0, 14), pady=5)
        button14.grid(row=9, column=10, padx=(0, 14), pady=5)

        for i in [button6, button7, button8, button9, button10, button11,
                  button12, button13, button14]:
            i.bind("<Enter>", lambda x: x.widget.config(bg="#083D91"))
            i.bind("<Leave>", lambda x: x.widget.config(bg="#4286f4"))

        self.input_kernel = tk.Text(self, height=2, width=12)
        self.input_kernel.grid(row=10, column=10, padx=0, pady=0)

        self.w = tk.Scale(self, from_=0, to=250000)
        self.svd_scale = tk.Scale(self, from_=0, to=1000)
        self.w.grid(row=11, column=10, padx=0, pady=0)
        self.svd_scale.grid(row=11, column=11, padx=0, pady=0)

        link = "C:/Users/Gabe/Desktop/CoreLabProject/CoreLabProject/demo2.jpg"
        self.editor = PhotoEditor(link)
        self.label2 = tk.Label(self, text="Metadata: null", font=LARGE_FONT,
                               bg="#EEEEEE", fg="#4286f4")
        self.label2.grid(row=16, column=0, pady=0, columnspan=10)

        label_new = tk.Label(self, text=" ", font=FONT_SMALL, bg="#EEEEEE",
                             fg="#4286f4")
        label_new.grid(row=17, column=0, sticky="W", pady=0)

        self.update_metadata()

    def set_size(self, width, height):
        ''' Changes the size of the image currently being displayed
        '''
        self.width = width
        self.height = height
        self.update_image(self.curr_dir)

    def update_metadata(self):
        ''' Reloads the metadata displayed about the image
        '''
        s = f"{self.editor.get_meta_data(self.curr_image)}"
        self.label2.config(text=s)

    def kernel_custom(self):
        ''' Allows the user to input a custom kernel that will be convolved
            with the picture '''
        s = self.input_kernel.get("1.0", "end-1c")
        s = [int(i) for i in s]
        if s == []:
            # default is laplacian kernel
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
                              dtype=np.int32)
            total = 1
        else:
            total = 1 / sum(s[:9])
            kernel = np.array([[s[0], s[1], s[2]], [s[3], s[4], s[5]], [s[6],
                              s[7], s[8]]], dtype=np.int32)

        new_image = self.editor.custom_kernel(self.curr_image, kernel, total)
        self.update_image(new_image, mode="2")

    def svd(self):
        '''
        Allows the user to select the k value that will be used. The image will
        be compressed by doing SVD decomposition and then taking the first k
        terms (refer to documentation for indepth explanation).
        '''
        svd_handler = SVDCompression(self.curr_image, self.svd_scale.get())
        new_image = svd_handler.RGB_to_greyscale()
        self.update_image(new_image, mode="2")

    def add_noise(self):
        ''' Calls the function in the editor to add noise to the image w/
        the number of pixels given by the slider '''
        new_image = self.editor.add_noise(self.curr_image, self.w.get())
        self.update_image(new_image, mode="2")

    def undo(self):
        ''' Set the current image to be the previously saved image '''
        if self.prev_dir is not None:
            self.update_image(self.prev_dir)

    def copy_img(self):
        ''' TODO: currently not working '''
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.curr_dir)
        self.parent.update()

    def save(self, filename=""):
        ''' Saves a file given a filename '''
        if filename == "":
            if self.curr_dir is None:
                filename = self.save_as()
            else:
                filename = self.curr_dir

        self.curr_image.save(filename)

    def save_as(self):
        ''' Opens the file browser so that the user can select a place
        to save the current image '''
        try:
            filename = filedialog.askopenfilename(initialdir="/", title="Select \
                file", filetypes=(("jpeg files", "*.jpg"),
                                  ("all files", "*.*")))
            self.save(filename)
        except:
            pass

    def bilateral_filter(self):
        ''' Calls the bilateral filter function in the editor '''
        new_image = self.editor.bilateral_filter(self.curr_image)
        self.update_image(new_image, mode="2")

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
        new_image = self.editor.flip(self.curr_image, 0, 0,
                                     self.curr_image.size[0],
                                     self.curr_image.size[1])
        self.update_image(new_image, mode="2")

    def update_image(self, image_name, mode="Image Name"):
        ''' Given an image_name, displays the new picture and updates all of
        the variables in the current frame '''
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
        try:
            filename = filedialog.askopenfilename(initialdir="/", title="Select \
                file", filetypes=(("jpeg files", "*.jpg"),
                                  ("all files", "*.*")))
            self.update_image(filename)
        except:
            pass


def init():
    ''' Initializes the GUI for the photo editor '''
    # Default width and height for the image
    pic_width = 500
    pic_height = 500

    # Check if the user specified a custom image size
    for i in sys.argv:
        if i[:2] == "-w":
            pic_width = i[3:]
        elif i[:2] == '-h':
            pic_height = i[3:]

    photo_editor = PhotoGUI()
    photo_editor.set_size(pic_width, pic_height)
    photo_editor.frames['StartPage'].update_image(
        photo_editor.frames['StartPage'].curr_image, mode="2")
    title_text = "Photoshep - 17 Day Free Trial (12 flex dollars to purchase) "
    photo_editor.title(title_text)
    photo_editor.iconbitmap("icon.ico")
    photo_editor.mainloop()


if __name__ == "__main__":
    init()
