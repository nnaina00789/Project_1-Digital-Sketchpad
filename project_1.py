import tkinter as tk
from tkinter import ttk,colorchooser,filedialog
from PIL import ImageGrab
# fo saving the canvas as an image
# store global color and brush size
current_color="black"
current_brush_size=2
history=[]
# to store item IDs for undo functionality
active_tool="brush"
start_x=None
start_y=None
# functions
def draw(event):
    # draws freehand on the canvas if the brush is active
    # check if the brush is active
    if active_tool=="brush":
        x1,y1=(event.x-current_brush_size),(event.y-current_brush_size)
        x2,y2=(event.x+current_brush_size),(event.y+current_brush_size)
    # create an oval at the mouse position
        item_id=canvas.create_oval(x1,y1,x2,y2,fill=current_color,outline=current_color)
        history.append(item_id)
def change_brush_size(new_size):
    global current_brush_size
    current_brush_size=int(new_size)

def change_color(new_color):
    global current_color
    current_color=new_color

def activate_brush():
    global active_tool
    active_tool="brush"

def activate_line():
    global active_tool
    active_tool="line"

def use_eraser():
    activate_brush()
    # eraser is a type of brush
    change_color('white')

def choose_custom_color():
    color_code=colorchooser.askcolor(title='CHOOSE COLOR')
    if color_code and color_code[1]:
        change_color(color_code[1])

def clear_canvas():
    canvas.delete("all")
    history.clear()
#     clear undo history
# event handlers for mouse actions
def on_press(event):
    global start_x,start_y
    start_x=event.x
    start_y=event.y
def on_release(event):
    if active_tool=="line":
        end_x,end_y=event.x,event.y
        item_id=canvas.create_line(start_x,start_y,end_x,end_y,fill=current_color,width=current_brush_size*2)
        history.append(item_id)

def undo(event=None):
    if history:
        item_id=history.pop()
        canvas.delete(item_id)
def save_canvas():
    file_path=filedialog.asksaveasfilename(defaultextension='.png',filetypes=[("PNG files","*.png"),("All files","*.*")])
    if not file_path:
        return
    x=root.winfo_rootx()+canvas.winfo_rootx()
    y=root.winfo_rooty()+canvas.winfo_rooty()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    ImageGrab.grab().crop(x,y,x1,y1).save(file_path)
# UI setup
root=tk.Tk()
root.title("Digital Sketchpad")
controls_frame=ttk.Frame(root,padding=10)
controls_frame.pack(side='top',fill='x')
canvas=tk.Canvas(root,bg='white')
canvas.pack(fill='both',expand=True)
 # will make the canvas expand the window

# Add controls to the controls_frame
# brush slider
size_slider=ttk.Scale(controls_frame,from_=1,to=20,orient='horizontal',command=change_brush_size)
# size_slider.set(current_brush_size)
size_slider.pack(side='left',padx=5)
ttk.Label(controls_frame,text='Brush Size').pack(side='left')
# modified buttons
brush_btn=ttk.Button(controls_frame,text='Brush',command=activate_brush)
brush_btn.pack(side='left',padx=5)
line_btn=ttk.Button(controls_frame,text='Line',command=activate_line)
line_btn.pack(side='left',padx=5)
# color buttons
colors=['Red','Blue','Green','Yellow','Orange']
for color in colors:
#     use lambda to pass the color argument
    btn=ttk.Button(controls_frame,text=color.capitalize(),command=lambda c=color:(activate_brush(),change_color(c)))
    btn.pack(side='left',padx=5)
custom_color_btn=ttk.Button(controls_frame,text='Custom Color',command=choose_custom_color)
custom_color_btn.pack(side='left',padx=5)
eraser=ttk.Button(controls_frame,text="Eraser",command=use_eraser)
eraser.pack(side='left',padx=5)
undo_btn=ttk.Button(controls_frame,text="Undo",command=undo)
undo_btn.pack(side='right',padx=5)
save_btn=ttk.Button(controls_frame,text='Save',command=save_canvas)
save_btn.pack(side='right',padx=5)
clear_btn=ttk.Button(controls_frame,text='Clear',command=clear_canvas)
clear_btn.pack(side='right',padx=5)

    # binding of mouse events to the drawing functions
canvas.bind('<B1-Motion>',draw)
#     above for freehand drawing
canvas.bind('<ButtonPress-1>',on_press)
#     to start drawing a line
canvas.bind('<ButtonRelease-1>',on_release)
# to finish drawing a line
root.bind("<Control-z>",undo)
#     keyboard shortcut for undo

root.mainloop()