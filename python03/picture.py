import cv2
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class ImageProcessor:
    def __init__(self):
        self.root = Tk()
        self.root.title("Image Filter App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)      
        self.original_image = None
        self.adjusted_image = None 
        self.create_widgets()
        
    def create_widgets(self):
        select_button = Button(self.root, text="Select Image", command=self.select_image)
        select_button.pack(pady=10)     
        brightness_label = Label(self.root, text="Brightness:")
        brightness_label.pack()    
        self.brightness_slider = Scale(self.root, from_=-100, to=100, orient=HORIZONTAL, command=self.apply_filter)
        self.brightness_slider.pack()        
        contrast_label = Label(self.root, text="Contrast:")
        contrast_label.pack()       
        self.contrast_slider = Scale(self.root, from_=0.1, to=2.0, resolution=0.1, orient=HORIZONTAL, command=self.apply_filter)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack()       
        self.canvas = Canvas(self.root, width=800, height=600)
        self.canvas.pack()      
        save_button = Button(self.root, text="Save As", command=self.save_image)
        save_button.pack()
        
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.adjusted_image = self.original_image.copy()
            self.show_image()
            
    def apply_filter(self, event=None):
        brightness_value = self.brightness_slider.get()
        contrast_value = self.contrast_slider.get()       
        self.adjusted_image = cv2.convertScaleAbs(self.original_image, alpha=brightness_value / 50, beta=contrast_value)
        self.show_image()
        
    def show_image(self):
        resized_image = cv2.resize(self.adjusted_image, (800, 600))       
        pil_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)) 
        self.image = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("adjusted_image")
        self.canvas.create_image(0, 0, anchor=NW, image=self.image, tags="adjusted_image")
        
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Image", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, self.adjusted_image)
            messagebox.showinfo("Save", "Image saved successfully.")
            
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            
            
if __name__ == "__main__":
    image_processor = ImageProcessor()
    image_processor.root.mainloop()
