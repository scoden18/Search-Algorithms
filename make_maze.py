from tkinter import *
import csv

#This is for drawing your own custom maze to use for the search algorithms.
#Left click and drag to draw obstructions, right click and drag to erase them.
#Shift+Left click to place start (green), shift + Right click to place target (red).
#Right click+drag erasing can also erase start and target.
#You must decide tile size and how much of the screen the window takes up.
#If you make a custom maze, its properties will override the ones in options.txt
#When done drawing, press enter on the keyboard and the maze is automatically written to maze.csv
#The file has to be called "maze.csv" since that's what the program looks for
#I included some examples, just rename to "maze.csv" to see them


tile_width = 20
percent_screen_x = 0.99
percent_screen_y = 0.9
background_color = "#FFFFFF"

def getx1(self):
    tempcoords = canvas.coords(self)
    return tempcoords[0]


def gety1(self):
    tempcoords = canvas.coords(self)
    return tempcoords[1]


def getx2(self):
    tempcoords = canvas.coords(self)
    return tempcoords[2]


def gety2(self):
    tempcoords = canvas.coords(self)
    return tempcoords[3]

def makeobstruction(event):
    try:
        x = event.x
        y = event.y
        tile = canvas.find_overlapping(x,y,x,y)
        if "obstruction" not in canvas.gettags(tile):
            canvas.dtag(tile[0], "start")
            canvas.dtag(tile[0], "target")
            canvas.addtag_withtag("obstruction", tile)
            canvas.itemconfigure(tile[0], fill = "#222222")
    except:
        pass


def erasetile(event):
    try:
        x = event.x
        y = event.y

        tile = canvas.find_overlapping(x,y,x,y)
        canvas.dtag(tile[0], "obstruction")
        canvas.dtag(tile[0], "start")
        canvas.dtag(tile[0], "target")
        canvas.itemconfigure(tile[0], fill = background_color)
    except:
        pass

def setstart(event):
    try:
        x = event.x
        y = event.y

        canvas.itemconfigure("start", fill = background_color)
        canvas.dtag("start", "start")
        tile = canvas.find_overlapping(x,y,x,y)
        canvas.dtag(tile[0], "obstruction")
        canvas.dtag(tile[0], "start")
        canvas.dtag(tile[0], "target")
        canvas.addtag_withtag("start", tile[0])
        canvas.itemconfigure(tile[0], fill = "#11DD11")
    except:
        pass

def settarget(event):
    try:
        x = event.x
        y = event.y

        canvas.itemconfigure("target", fill = background_color)
        canvas.dtag("target", "target")
        tile = canvas.find_overlapping(x,y,x,y)
        canvas.dtag(tile[0], "obstruction")
        canvas.dtag(tile[0], "start")
        canvas.dtag(tile[0], "target")
        canvas.addtag_withtag("target", tile[0])
        canvas.itemconfigure(tile[0], fill = "red")
    except:
        pass

def writemaze(event):
    global tiles
    start_exists = False
    target_exists = False
    maze = []
    #Writes tile position and tags to csv if it's an obstruction, start, or target. If it's nothing, doesn't write anything to keep file size down.
    for tile in tiles:
        tile_tags = canvas.gettags(tile)
        if "obstruction" in tile_tags:
            maze.append([tile,1,0,0])
        elif "start" in tile_tags:
            maze.append([tile,0,1,0])
            start_exists = True
        elif "target" in tile_tags:
            maze.append([tile,0,0,1])
            target_exists = True

    if not start_exists or not target_exists:
        root.destroy()
        raise Exception("You must place a start and target!")

    with open("maze.csv", "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow([tile_width,x_width,y_width])
        writer.writerows(maze)

    root.quit()

    print("Maze successfully created!")



root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_width = int((screen_width*percent_screen_x)//tile_width)
y_width = int((screen_height*percent_screen_y)//tile_width)
root_width = int(x_width * tile_width)
root_height = int(y_width * tile_width)

root.geometry(f"{root_width}x{root_height}+0+0")
canvas = Canvas(root, bg = background_color, height = root_height, width = root_width)

#List of all tiles, in order of top to bottom, left to right.
tiles = []
for i in range(x_width):
    for j in range(y_width):
        new_rect = canvas.create_rectangle(tile_width*i,tile_width*j,tile_width*i+tile_width-1,tile_width*j+tile_width-1,fill = background_color, outline = "#666666", width = 1)
        tiles.append(new_rect)


canvas.bind("<B1-Motion>", makeobstruction)
canvas.bind("<B3-Motion>", erasetile)
canvas.bind("<Shift-Button-1>", setstart)
canvas.bind("<Shift-Button-3>", settarget)
root.bind("<KeyPress-Return>", writemaze)
canvas.pack()
root.focus_force()
root.mainloop()

