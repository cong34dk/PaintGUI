from tkinter import * 
from tkinter import ttk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk 
from os import path 
import sys

class Paint(Tk): 
    def __init__(self): 
        super().__init__()
        parent_folder = path.dirname(sys.argv[0])
        self.iconbitmap(path.join(parent_folder, 'paint_icon.ico'))
        self.resizable(False, False)

        self.create_widgets()
        self.binding_events()
        self.pen_color = 'black'
        self.eraser_color = "white"

        self.canvas.update_idletasks()
        self.bg_rect_id = self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="white", tags=("bg",))

    def change_color(self, color): 
        self.pen_color = color 

    def create_widgets(self): 
        # Create container widgets 
        self.color_frame = LabelFrame(self, labelanchor='n', text="Color", bd=4, relief=RIDGE)
        self.color_frame.grid(row=0, column=0, pady=10, padx=10)

        self.func_frame = Frame(self)
        self.func_frame.grid(row=1, column=0, pady=10, padx=10)

        self.size_frame = LabelFrame(self, labelanchor='n', text="Size", relief=RIDGE, bd=4)
        self.size_frame.grid(row=2, column=0, pady=10, padx=10)

        # Create the canvas widget 
        self.canvas = Canvas(self, bd=4, relief=GROOVE, bg='white', height=550, width=700, cursor='crosshair')
        self.canvas.grid(row=0, column=1, rowspan=3, padx=10)

        # Create color to color frame 
        colors = ['black', 'gray', 'red', 'green', 'blue', 'purple', 'pink', 'lightblue', 'orange', 'cyan', 'magenta', 'yellow']
        colors_iter = iter(colors)
        for r in range(6): 
            for c in range(2): 
                color = next(colors_iter)
                Button(self.color_frame, bg=color, width=3, borderwidth=2, relief=RIDGE, command=lambda col=color: self.change_color(col)).grid(row=r, column=c)

        # Create function buttons for func_frame 
        self.eraser_btn = Button(self.func_frame, text="Eraser", width=8, bd=4, relief=RIDGE, command=lambda: self.eraser())
        self.clear_btn = Button(self.func_frame, text="Clear", width=8, bd=4, relief=RIDGE, command=lambda: self.clear())
        self.save_btn = Button(self.func_frame, text="Save", width=8, bd=4, relief=RIDGE, command=lambda: self.save())
        self.canvas_btn = Button(self.func_frame, text="Canvas", width=8, bd=4, relief=RIDGE, command=lambda: self.canvas_color())
        self.open_btn = Button(self.func_frame, text="Open", width=8, bd=4, relief=RIDGE, command=lambda: self.open())

        self.eraser_btn.grid(row=0, column=0)
        self.clear_btn.grid(row=1, column=0)
        self.save_btn.grid(row=2, column=0)
        self.canvas_btn.grid(row=3, column=0)
        self.open_btn.grid(row=4, column=0)

        # Create a Scale widget for size_frame 
        self.size_scale = ttk.Scale(self.size_frame, orient=VERTICAL, from_=50, to=0, length=170)
        self.size_scale.set(10)
        self.size_scale.grid(row=0, column=0, padx=15)

    def binding_events(self): 
        self.canvas.bind("<Button-1>", self.locate_xy)
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

    def locate_xy(self, event): 
        self.current_x = event.x 
        self.current_y = event.y 

    def draw_on_canvas(self, event): 
        x0, y0 = self.current_x, self.current_y  
        x1, y1 = event.x, event.y 
        self.canvas.create_line(x0, y0, x1, y1, width=self.size_scale.get(), fill=self.pen_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36, tags=("obj",))

        self.current_x = event.x 
        self.current_y = event.y  

    def eraser(self): 
        self.pen_color = self.eraser_color 

    def clear(self): 
        self.canvas.delete(("obj",))

    def canvas_color(self): 
        canvas_color = colorchooser.askcolor()[1]

        if self.bg_rect_id: 
            self.canvas.delete(self.bg_rect_id)

        self.bg_rect_id = self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=canvas_color)
        self.canvas.tag_lower(self.bg_rect_id, "all")
        self.eraser_color = canvas_color 

    def save(self): 
        try: 
            file_name = filedialog.asksaveasfilename(defaultextension='.ps', filetypes=[("PostScript", ".ps")])
            if not file_name: 
                return 

            self.canvas.postscript(colormode="color", file=file_name)
            
        except Exception as e: 
            messagebox.showerror(
                title="Error", 
                message="Some error occurs !"
            )

    def open(self):
        try:  
            filename = filedialog.askopenfilename()
            if not filename: 
                return 

            img = Image.open(filename)
            img = img.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))

            self.canvas.image = ImageTk.PhotoImage(img)

            iden = self.canvas.create_image(
                0, 0, 
                image = self.canvas.image,
                anchor="nw",
                tag="obj"
            )
        except: 
            messagebox.showerror("Error", "Can't open this file in HPaint")
        
if __name__ == "__main__": 
    app = Paint()
    app.mainloop()