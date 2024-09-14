from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox
import math
from tkinter import Entry
import PIL.ImageGrab as ImageGrab
from PIL import Image, ImageTk
from PIL import ImageOps, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import asksaveasfile, asksaveasfilename


class PaintBrush:
    
    def __init__(self, width, height, title):
        self.screen = Tk()
        self.screen.title(title)
        self.screen.geometry(f"{width}x{height}")
        self.brush_color = 'black'
        self.last_x, self.last_y = None, None
        self.shape_id = None
        self.pen_size = 5
        self.is_pen = True
        self.polygon_sides = 3 
        self.magnifier_size = 200  # Size of the magnifier window
        self.magnifier_scale = 2  # Scale factor for magnification
        
        self.button_area = Frame(self.screen, width=width, height=100, bg="lightgray")
        self.button_area.pack()
        
        
        
        #done
        self.magnifier_button = Button(self.button_area, text="Magnifier", command=self.activate_magnifier, font=("Georgia", 12), bd=0, bg="white")
        self.magnifier_button.place(x=390, y=50)

        #done
        self.select_color_button = Button(self.button_area, text="Select Color", command=self.select_color, font=("Georgia", 12), bd=0, bg="white")
        self.select_color_button.place(x=1050, y=35)

        self.canvas = Canvas(self.screen, width=width, height=height, bg="white")
        self.canvas.pack()
        
        #done
        self.clear_button = Button(self.button_area, text="Clear", command=self.clear_canvas, font=("Georgia", 12), bd=0, bg="white")
        self.clear_button.place(x=10, y=10)
        
        #done
        self.pen_button = Button(self.button_area, text="Pen", command=self.use_pen, font=("Georgia", 12), bd=0, bg="white")
        self.pen_button.place(x=145, y=10)
        
        #done
        self.pen_size_slider = Scale(self.button_area, from_=1, to=10, orient=HORIZONTAL, label="Outline Size", command=self.set_pen_size)
        self.pen_size_slider.set(self.pen_size)
        self.pen_size_slider.place(x=1150, y=38)
        
        
        self.eraser_button = Button(self.button_area, text="Eraser", command=self.use_eraser, font=("Georgia", 12), bd=0, bg="white")
        self.eraser_button.place(x=340, y=10)

        #done
        self.color_buttons = []
        colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black']
        for i, color in enumerate(colors):
            button = Button(self.button_area, bg=color, width=3, command=lambda c=color: self.set_brush_color(c))
            button.place(x=1000 + i * 30, y=10)
            self.color_buttons.append(button)
            
        #done
        self.circle_button = Button(self.button_area, text="Circle", command=self.on_circle_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.circle_button.place(x=10, y=50)
        
        #done
        self.fill_button = Button(self.button_area, text="Fill", command=self.fill_pressed)
        self.fill_button.place(x=1010,y=50)
        
        #done
        self.picker_button = Button(self.button_area, text="Color Picker", command=self.picker_pressed)
        self.picker_button.place(x=1060,y=70)
        
        #done
        self.triangle_button = Button(self.button_area, text="Triangle", command=self.on_triangle_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.triangle_button.place(x=65, y=50)

        #done
        self.rectangle_button = Button(self.button_area, text="Rectangle", command=self.on_rectangle_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.rectangle_button.place(x=140, y=50)
        
        
        
        #done
        self.pentagon_button = Button(self.button_area, text="Pentagon", command=self.on_pentagon_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.pentagon_button.place(x=65, y=10)
        
        #done
        self.oval_button = Button(self.button_area, text="Oval", command=self.on_oval_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.oval_button.place(x=225, y=50)
        
        #done
        self.square_button = Button(self.button_area, text="Square", command=self.on_square_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.square_button.place(x=275, y=50)

        #done
        self.line_button = Button(self.button_area, text="Line", command=self.on_line_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.line_button.place(x=340, y=50)

        #done
        self.star_button = Button(self.button_area, text="Star", command=self.on_star_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.star_button.place(x=400, y=10)
        
        #done
        self.zoom_in_button = Button(self.button_area, text="Zoom In", command=self.zoom_in, font=("Georgia", 12), bd=0, bg="white")
        self.zoom_in_button.place(x=850, y=10)
        
        #done
        self.zoom_out_button = Button(self.button_area, text="Zoom Out", command=self.zoom_out, font=("Georgia", 12), bd=0, bg="white")
        self.zoom_out_button.place(x=850, y=50)

        #done
        self.hexagon_button = Button(self.button_area, text="Hexagon", command=self.on_hexagon_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.hexagon_button.place(x=260, y=10)

        #done
        self.polygon_slider = Scale(self.button_area, from_=3, to=10, orient=HORIZONTAL, label="Polygon Sides", command=self.set_polygon_sides)
        self.polygon_slider.set(self.polygon_sides)
        self.polygon_slider.place(x=500, y=20)

        #done
        self.polygon_button = Button(self.button_area, text="Polygon", command=self.on_polygon_pressed, font=("Georgia", 12), bd=0, bg="white")
        self.polygon_button.place(x=190, y=10)
        
        
        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas.bind("<ButtonRelease-1>", self.brush_draw_end)
        #self.canvas.bind("<Button-1>", self.write_text)

        def saveImage():
         try:
           fileLocation = filedialog.asksaveasfilename(defaultextension="jpg")
           frame_width = 1500
           frame_height = 980
           canvas_width = self.canvas.winfo_width()
           canvas_height = self.canvas.winfo_height()
           x = self.canvas.winfo_rootx() + (frame_width - canvas_width) // 2
           y = self.canvas.winfo_rooty() + (frame_height - canvas_height) // 2
           img = ImageGrab.grab(bbox=(x, y, x + canvas_width, y + canvas_height))
           img.save(fileLocation)
           showImage = messagebox.askyesno("Paint App", "Do you want to open the image?")
           if showImage:
               img.show()
         except Exception as e:
           messagebox.showinfo("Paint app:", "An error occurred")

        #done
        self.saveImageFrame = Frame(self.screen,height=10,width=10,relief=SUNKEN,borderwidth=3)                       
        self.saveImageFrame .place(x=940,y=10)
        saveButton=Button( self.saveImageFrame ,text='save',bg='white',width=5,command=saveImage).grid(row=0,column=0)
        
        #done
        self.load_button = Button(self.button_area, text="Load", command=self.load_canvas, font=("Georgia", 12), bd=0, bg="white")
        self.load_button.place(x=945, y=50)
        
        self.textval = StringVar()
        textentry = Entry(self.button_area, width=20, textvariable=self.textval)
        textentry.grid(row=4, column=4)
        
    def activate_magnifier(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.show_magnifier)
        self.canvas.bind("<ButtonRelease-1>", self.end_magnifier)
        
    def show_magnifier(self, event):
        magnification = 2  # Adjust the magnification factor as desired
        size = 150  # Adjust the size of the magnifier window as desired
        x = event.x - size // (2 * magnification)
        y = event.y - size // (2 * magnification)
        region = (
            x * magnification,
            y * magnification,
            (x + size) * magnification,
            (y + size) * magnification,
        )
        screenshot = ImageGrab.grab(bbox=region)
        screenshot = ImageOps.fit(screenshot, (size, size), Image.ANTIALIAS)
        screenshot = ImageEnhance.Brightness(screenshot).enhance(2.0)
        screenshot = ImageEnhance.Contrast(screenshot).enhance(1.2)
        screenshot = ImageEnhance.Color(screenshot).enhance(1.2)
        self.magnifier_image = ImageTk.PhotoImage(screenshot)
        self.canvas.create_image(event.x, event.y, image=self.magnifier_image)
    
    def zoom_in(self):
        self.canvas.scale("all", 0, 0, 1.2, 1.2)
    
    def zoom_out(self):
        self.canvas.scale("all", 0, 0, 0.8, 0.8)

    def picker_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.get_pixel_color)
        self.canvas.bind("<ButtonRelease-1>", self.end)
    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color   
    def get_pixel_color(self, event):
        x, y = event.x, event.y
        x_root, y_root = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        x_global, y_global = x_root + x, y_root + y
        screenshot = ImageGrab.grab()
        pixel_rgb = screenshot.getpixel((x_global, y_global))
        pixel_color = '#%02x%02x%02x' % pixel_rgb
        self.brush_color = pixel_color
            
    def fill_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.fill)
        self.canvas.bind("<ButtonRelease-1>", self.end)  
    def fill(self, event):
        shape = self.canvas.find_closest(event.x, event.y)
        if shape != 1:
            self.canvas.itemconfig(shape, fill=self.brush_color)
                                   
    
    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if file_path:
            image = Image.open(file_path)
            self.canvas.delete("all")
            self.canvas.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.canvas.image)
            
    def write_text(self, event):
        self.canva["cursor"] = "arrow"
        self.canva.create_text(event.x, event.y, text=self.textval.get())
        
    def on_oval_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_oval)
        self.canvas.bind("<ButtonRelease-1>", self.draw_oval_end)
    def draw_star(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius1 = abs(event.x - self.last_x)
        radius2 = abs(event.y - self.last_y)
        x_center = self.last_x + radius1
        y_center = self.last_y + radius2
        points = []
        angle = 2 * math.pi / 10
        for i in range(10):
            radius = radius1 if i % 2 == 0 else radius2
            x = x_center + radius * math.cos(i * angle)
            y = y_center + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_star_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def on_square_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_square)
        self.canvas.bind("<ButtonRelease-1>", self.draw_square_end)

    def on_line_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.draw_line_end)

    def on_star_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_star)
        self.canvas.bind("<ButtonRelease-1>", self.draw_star_end)

    def on_rectangle_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_rectangle_end)

    def on_pentagon_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_pentagon_end)

    def draw_rectangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_rectangle(self.last_x, self.last_y, event.x, event.y, outline=self.brush_color, width=self.pen_size,fill="")

    def draw_rectangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
        
    def on_fill_pressed(self):
        if self.shape_id is not None:
            self.canvas.itemconfig(self.shape_id, fill=self.brush_color)

    def draw_pentagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        angle = 2 * math.pi / 5
        points = []
        for i in range(5):
            x = self.last_x + radius * math.cos(i * angle)
            y = self.last_y + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.pen_size,fill="")

    def draw_pentagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def use_pen(self):
        self.is_pen = True
        self.canvas.bind("<B1-Motion>", self.brush_draw)

    def use_eraser(self):
        self.is_pen = False
        self.canvas.bind("<B1-Motion>", self.eraser_draw)

    def set_pen_size(self, size):
        self.pen_size = int(size)

    def set_brush_color(self, color):
        self.brush_color = color

    def on_circle_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_circle_end)

    def on_triangle_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_triangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_triangle_end)

    def draw_circle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        x1, y1 = (self.last_x - radius), (self.last_y - radius)
        x2, y2 = (self.last_x + radius), (self.last_y + radius)
        self.shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline=self.brush_color, width=self.pen_size)

    def draw_circle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_triangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3, y3 = (self.last_x - (event.x - self.last_x)), event.y
        self.shape_id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, outline=self.brush_color, width=self.pen_size,fill="")

    def draw_triangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def select_color(self):
        selected_color = colorchooser.askcolor()
        if selected_color[1] is not None:
            self.brush_color = selected_color[1]

    def clear_canvas(self):
        self.canvas.delete("all")

    def run(self):
        self.screen.mainloop()

    def draw_oval(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_oval(self.last_x, self.last_y, event.x, event.y, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_oval_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_square(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        side = min(abs(event.x - self.last_x), abs(event.y - self.last_y))
        x1, y1 = self.last_x, self.last_y
        x2, y2 = self.last_x + side, self.last_y + side
        self.shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_square_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def draw_line(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.brush_color, width=self.pen_size)

    def draw_line_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def brush_draw(self, event):
        if not self.is_pen:
            return
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.pen_size, capstyle=ROUND, fill=self.brush_color)
        self.last_x, self.last_y = event.x, event.y
        
    def eraser_draw(self, event):
        if self.is_pen:
            return
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=self.pen_size, capstyle=ROUND, fill="white")
        self.last_x, self.last_y = event.x, event.y

    def brush_draw_end(self, event):
        self.last_x, self.last_y = None, None

    def set_polygon_sides(self, sides):
        self.polygon_sides = int(sides)

    def on_polygon_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_polygon_end)

    def draw_polygon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return

        points = self.calculate_polygon_points(event.x, event.y, self.polygon_sides)
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_polygon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def calculate_polygon_points(self, x, y, sides):
        angle = 2 * math.pi / sides
        radius = abs(self.last_x - x) + abs(self.last_y - y)
        points = []
        for i in range(sides):
            point_x = x + radius * math.cos(i * angle)
            point_y = y + radius * math.sin(i * angle)
            points.append((point_x, point_y))
        return points

    def on_hexagon_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_hexagon_end)
    def draw_hexagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        side = min(abs(event.x - self.last_x), abs(event.y - self.last_y))
        x_center = self.last_x + side
        y_center = self.last_y + side
        points = []
        angle = (2 * math.pi) / 6
        for i in range(6):
            x = x_center + side * math.cos(i * angle)
            y = y_center + side * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_hexagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

    def set_polygon_sides(self, sides):
        self.polygon_sides = int(sides)
        if self.polygon_sides == 9:
            self.polygon_button = Button(self.button_area, text="Polygon", command=self.on_polygon_pressed, font=("Georgia", 12), bd=0, bg="white")
            self.polygon_button.place(x=650, y=50)
        else:
            if hasattr(self, "polygon_button"):
                self.polygon_button.destroy()

    def on_polygon_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_polygon_end)

    def draw_polygon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)
        angle = 2 * math.pi / self.polygon_sides
        points = []
        for i in range(self.polygon_sides):
            x = self.last_x + radius * math.cos(i * angle)
            y = self.last_y + radius * math.sin(i * angle)
            points.append((x, y))
        self.shape_id = self.canvas.create_polygon(points, outline=self.brush_color, width=self.pen_size, fill="")

    def draw_polygon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
    def fill_color(self, event):
        x, y = event.x, event.y
        target_color = self.canvas.getpixel((x, y))
        if target_color != self.brush_color:
            self._fill_recursive(x, y, target_color)

    def _fill_recursive(self, x, y, target_color):
        current_color = self.canvas.getpixel((x, y))
        if current_color != target_color or current_color == self.brush_color:
            return
        self.canvas.putpixel((x, y), self.brush_color)
        self._fill_recursive(x + 1, y, target_color)
        self._fill_recursive(x - 1, y, target_color)
        self._fill_recursive(x, y + 1, target_color)
        self._fill_recursive(x, y - 1, target_color)

    def on_fill_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.fill_color)
    def clear_canvas(self):
        self.canvas.delete("all")
        self.last_x, self.last_y = None, None

PaintBrush(1500, 1000, "Paint Brush App").run()