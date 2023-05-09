#This is about twice as slow as no diag motion (since each tile checks twice as many tiles)
#But it is more likely to find a path because it has more movement options

from tkinter import *
import random
import math
import sys
import time
import csv

#Note: You can left click and drag to add obstructions in white space.

#OPTIONS
#Configure in options.txt, just change True/False or the number. Don't move stuff.
#If using custom maze, set use_custom_maze = True and it will overwrite all options except printing time and distance.
#Only works if you have the "maze.csv" file in the same folder as this script
#Leave "seed = " for random, do "seed = something" to seed it.
#Recommendations: For 1920x1080 screen
#Tile width >= 5, below 5 it crashes. Max is like 500 but that's 3 tiles. 150 max probably.
#Obstruction chance between 0 and 0.5. Above 0.5 it's almost guaranteed no paths. Even 0.5 is pretty bad.

with open("options.txt","r") as file:
    options = file.readlines()

use_custom_maze = options[12].split(" = ")[1]
if use_custom_maze == "True\n":
    use_custom_maze = True
else:
    use_custom_maze = False

if not use_custom_maze:
    #Leave seed blank in options to not seed it.
    seed = options[0].split(" = ")[1]
    if seed != "\n":
        random.seed(seed)

    min_tile_size = int(options[8].split(" = ")[1])
    max_tile_size = int(options[9].split(" = ")[1])

    #Obstruction chance is between 0 and 1, multiply by 100 for the % chance
    min_obstruction_chance = float(options[10].split(" = ")[1])
    max_obstruction_chance = float(options[11].split(" = ")[1])

    #If you don't randomize, it uses the values tile_width and obstruction_chance in options.txt
    randomize_tile_size_and_num_obstructions = options[1].split(" = ")[1]
    if randomize_tile_size_and_num_obstructions == "True\n":
        tile_width = random.randint(min_tile_size,max_tile_size)
        obstruction_chance = random.uniform(min_obstruction_chance,max_obstruction_chance)
    else:
        tile_width = int(options[5].split(" = ")[1])
        obstruction_chance = float(options[6].split(" = ")[1])

    #If you randomize, it takes up 33-90% of you screen, otherwise it's just 90%
    randomize_x_y_size = options[2].split(" = ")[1]
    if randomize_x_y_size == "True\n":
        randomize_x_y_size = True
    else:
        randomize_x_y_size = False


    #If you want the start and target as far from each other as possible.
    make_on_opposite_sides = options[7].split(" = ")[1]
    if make_on_opposite_sides == "True\n":
        make_on_opposite_sides = True
    else:
        make_on_opposite_sides = False
else:
    randomize_x_y_size = False
    make_on_opposit_sides = False
    with open("maze.csv", "r") as file:
        reader = csv.reader(file)
        topvars = next(reader)
        tile_width = int(topvars[0])
        x_width = int(topvars[1])
        y_width = int(topvars[2])
        del reader


#These two are independent of using a custom maze
#You can print the distance from the starting tile on every tile searched.
show_distances = options[3].split(" = ")[1]
if show_distances == "True\n":
    show_distances = True
else:
    show_distances = False

#Prints completion time (Including white screen) to terminal
print_completion_time = options[4].split(" = ")[1]
if print_completion_time == "True\n":
    print_completion_time = True
else:
    print_completion_time = False



start_time = time.time()


def searchnear(tile):
    global unsearched
    global tiles
    global canvas
    global target_found

    canvas.update()
    target_found = False
    while tile != target_tile:
        unsearched.remove(tile)
        canvas.itemconfigure(tile[0], fill = "#CCCC55")
        if tile == start_tile:
            canvas.itemconfigure(tile[0], fill = "#11DD11")

        
        ind = tiles.index(tile)
        valids = []
        current_distance = tile[3]
        ups = True
        downs = True
        lefts = True
        rights = True

        if ind%y_width == 0:
            ups = False
        if (ind+1)%y_width == 0:
            downs = False
        if 0 <= ind < y_width:
            lefts = False
        if x_width*y_width - 1 - y_width <= ind < x_width*y_width:
            rights = False

        if lefts and ups:
            left_up = tiles[ind - y_width - 1]
            if not left_up[1] and not left_up[2]:
                new_dist = current_distance + 2
                if new_dist < left_up[3]:
                    left_up[3] = new_dist
                valids.append(left_up)
        else:
            left_up = False
        if lefts:
            left = tiles[ind - y_width]
            if not left[1] and not left[2]:
                new_dist = current_distance + 1
                if new_dist < left[3]:
                    left[3] = new_dist
                valids.append(left)
        else:
            left = False
        if lefts and downs:
            left_down = tiles[ind - y_width + 1]
            if not left_down[1] and not left_down[2]:
                new_dist = current_distance + 2
                if new_dist < left_down[3]:
                    left_down[3] = new_dist
                valids.append(left_down)
        else:
            left_down = False
        if ups:
            up = tiles[ind - 1]
            if not up[1] and not up[2]:
                new_dist = current_distance + 1
                if new_dist < up[3]:
                    up[3] = new_dist
                valids.append(up)
        else:
            up = False
        if downs:
            down = tiles[ind + 1]
            if not down[1] and not down[2]:
                new_dist = current_distance + 1
                if new_dist < down[3]:
                    down[3] = new_dist
                valids.append(down)
        else:
            down = False
        if rights and ups:
            right_up = tiles[ind + y_width - 1]
            if not right_up[1] and not right_up[2]:
                new_dist = current_distance + 2
                if new_dist < right_up[3]:
                    right_up[3] = new_dist
                valids.append(right_up)
        else:
            right_up = False
        if rights:
            right = tiles[ind + y_width]
            if not right[1] and not right[2]:
                new_dist = current_distance + 1
                if new_dist < right[3]:
                    right[3] = new_dist
                valids.append(right)
        else:
            right = False
        if rights and downs:
            right_down = tiles[ind + y_width + 1]
            if not right_down[1] and not right_down[2]:
                new_dist = current_distance + 2
                if new_dist < right_down[3]:
                    right_down[3] = new_dist
                valids.append(right_down)
        else:
            right_down = False
        
        tile[2] = True

        for unsearched_tile in valids:
            if not unsearched_tile[2] and unsearched_tile not in unsearched:
                unsearched.append(unsearched_tile)
            canvas.itemconfigure(unsearched_tile[0], fill = "blue")
            if show_distances:
                canvas.create_text(getx1(unsearched_tile[0])+tile_width//2,gety1(unsearched_tile[0])+tile_width//2, text = f"{unsearched_tile[3]}")
            canvas.update()

        try:
            next_tile = unsearched[0]
            min = next_tile[3]
            for possible in unsearched:
                if possible[3] < min and not possible[2]:
                    min = possible[3]
                    next_tile = possible
                
            if next_tile == target_tile:
                target_found = True
                canvas.itemconfigure(next_tile[0], fill = "#FF00FF")
                #canvas.update()
                searchforpath(target_tile)
                root.quit()
                del unsearched
                return 0

            tile = next_tile
        except:
            if not target_found:
                canvas.create_text(root_width//2,root_height//2, text = "No possible paths!", font = "Helvetica 30 bold", fill = "red")
                root.quit()
                return 0
    

path = []
def searchforpath(tile):
    global path
    global canvas
    

    while tile != start_tile:
        ups = True
        downs = True
        lefts = True
        rights = True
        ind = tiles.index(tile)
        valids = []
        if ind%y_width == 0:
            ups = False
        if (ind+1)%y_width == 0:
            downs = False
        if 0 <= ind < y_width:
            lefts = False
        if x_width*y_width - 1 - y_width <= ind < x_width*y_width:
            rights = False

        if lefts and ups:
            left_up = tiles[ind - y_width - 1]
            if not left_up[1]:
                valids.append(left_up)
        else:
            left_up = False
        if lefts:
            left = tiles[ind - y_width]
            if not left[1]:
                valids.append(left)
        else:
            left = False
        if lefts and downs:
            left_down = tiles[ind - y_width + 1]
            if not left_down[1]:
                valids.append(left_down)
        else:
            left_down = False
        if ups:
            up = tiles[ind - 1]
            if not up[1]:
                valids.append(up)
        else:
            up = False
        if downs:
            down = tiles[ind + 1]
            if not down[1]:
                valids.append(down)
        else:
            down = False
        if rights and ups:
            right_up = tiles[ind + y_width - 1]
            if not right_up[1]:
                valids.append(right_up)
        else:
            right_up = False
        if rights:
            right = tiles[ind + y_width]
            if not right[1]:
                valids.append(right)
        else:
            right = False
        if rights and downs:
            right_down = tiles[ind + y_width + 1]
            if not right_down[1]:
                valids.append(right_down)
        else:
            right_down = False

        try:
            guess = valids[0]
            min = guess[3]
            for possible_tile in valids:
                if possible_tile[3] < min:
                    min = possible_tile[3]
                    guess = possible_tile

            path.append(guess)
            canvas.itemconfigure(guess[0], fill = "#FF00FF")
            canvas.update()
            if guess == start_tile:
                for path_tile in path:
                    canvas.itemconfigure(path_tile[1], fill = "#FF00FF")
                canvas.update()
                root.quit()
                if print_completion_time:
                    print(f"Completed in {time.time() - start_time} seconds")
                return path
            else:
                tile = guess
        except:
            if print_completion_time:
                print(f"Completed in {time.time() - start_time} seconds")
            root.quit()
            return path






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
    x = event.x
    y = event.y

    for tile in tiles:
        if getx1(tile[0]) <= x <= getx2(tile[0]) and gety1(tile[0]) <= y <= gety2(tile[0]):
            print(tiles[tiles.index(tile)])
            if not tile[1] and not tile[2] and tile != target_tile and tile != start_tile:
                tile[1] = True
                canvas.itemconfigure(tile[0], fill = "#222222")


root = Tk()

background_color = "#FFFFFF"



#Tiles take up anywhere from 1/3 to 99% of the screen in width, 1/3 to 90% in height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
max_tiles_x = (screen_width*0.99)//tile_width
min_tiles_x = (screen_width//3)//tile_width
max_tiles_y = (screen_height*0.9)//tile_width
min_tiles_y = (screen_height//3)//tile_width
if randomize_x_y_size:
    x_width = random.randint(min_tiles_x,max_tiles_x)
    y_width = random.randint(min_tiles_y,max_tiles_y)
else:
    x_width = int(max_tiles_x)
    y_width = int(max_tiles_y)
root_width = x_width * tile_width
root_height = y_width * tile_width
sys.setrecursionlimit(10**7)


root.geometry(f"{root_width}x{root_height}+0+0")
canvas = Canvas(root, bg = background_color, height = root_height, width = root_width)

if not use_custom_maze:
    #Tiles is a 2D list.
    #0 is the tile, 1 is if it's an obstruction, 2 is if it's been searched, 3 is the distance associated
    tiles = []
    for i in range(x_width):
        for j in range(y_width):
            new_rect = canvas.create_rectangle(tile_width*i,tile_width*j,tile_width*i+tile_width-1,tile_width*j+tile_width-1,fill = background_color, outline = "#666666", width = 1)
            tiles.append([new_rect, False, False, sys.maxsize])


    for i in tiles:
        obstruct = random.uniform(0,1)
        if obstruct <= obstruction_chance:
            canvas.itemconfigure(i[0], fill = "#222222")
            i[1] = True


    target_tile = random.choice(tiles)
    if target_tile[1]:
        while target_tile[1]:
            target_tile = random.choice(tiles)
    if make_on_opposite_sides:
        target_tile = tiles[0]
        target_tile[1] = False
    canvas.itemconfigure(target_tile[0], fill = "red")


    start_tile = random.choice(tiles)
    if (canvas.coords(start_tile[0]) == canvas.coords(target_tile[0])) or start_tile[1]:
        while (canvas.coords(start_tile[0]) == canvas.coords(target_tile[0])) or start_tile[1]:
            start_tile = random.choice(tiles)
    if make_on_opposite_sides:
        start_tile = tiles[-1]
        start_tile[1] = False
    canvas.itemconfigure(start_tile[0], fill = "#11DD11")
    start_tile[3] = 0
else:
    #Tiles is a 2D list.
    #0 is the tile, 1 is if it's an obstruction, 2 is if it's been searched, 3 is the distance associated
    tiles = []
    for i in range(x_width):
        for j in range(y_width):
            new_rect = canvas.create_rectangle(tile_width*i,tile_width*j,tile_width*i+tile_width-1,tile_width*j+tile_width-1,fill = background_color, outline = "#666666", width = 1)
            tiles.append([new_rect, False, False, sys.maxsize])
    start_tile = tiles[-1]
    start_tile[3] = 0
    target_tile = tiles[0]

    with open("maze.csv", "r") as file:
        reader = csv.reader(file)
        #skip first row since it's just numbers
        next(reader)
        for row in reader:
            if row[1] == "1":
                tiles[int(row[0]) - 1][1] = True
                canvas.itemconfigure(tiles[int(row[0]) - 1][0], fill = "#222222")
            elif row[2] == "1":
                start_tile = tiles[int(row[0]) - 1]
                canvas.itemconfigure(start_tile[0], fill = "#11DD11")
                start_tile[3] = 0
            elif row[3] == "1":
                target_tile = tiles[int(row[0]) - 1]
                canvas.itemconfigure(target_tile[0], fill = "red")

unsearched = [start_tile]


canvas.bind("<B1-Motion>",makeobstruction)

canvas.pack()
searchnear(start_tile)
root.mainloop()





