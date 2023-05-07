#With few obstructions, this is about twice as fast as with diag motion (since each tile checks half as many tiles)
#But it is less likely to find a path because it has fewer movement options

from tkinter import *
import random
import math
import sys
import time



#Note: You can left click and drag to add obstructions in white space.

#OPTIONS
#Configure in options.txt, just change True/False or the number. Don't move stuff.
#Leave "seed = " for random, do "seed = something" to seed it.
#Recommendations: For 1920x1080 screen
#Tile width >= 5, below 5 it crashes. Max is like 500 but that's 3 tiles. 150 max probably.
#Obstruction chance between 0 and 0.5. Above 0.5 it's almost guaranteed no paths. Even 0.5 is pretty bad.

with open("options.txt","r") as file:
    options = file.readlines()

#Leave seed blank in options to not seed it.
seed = options[0].split(" = ")[1]
if seed != "\n":
    random.seed(seed)

#If you don't randomize, it uses the values tile_width and obstruction_chance in options.txt
randomize_tile_size_and_num_obstructions = options[1].split(" = ")[1]
if randomize_tile_size_and_num_obstructions == "True\n":
    tile_width = random.randint(20,50)
    obstruction_chance = random.uniform(0,0.4)
else:
    tile_width = int(options[5].split(" = ")[1])
    obstruction_chance = float(options[6].split(" = ")[1])

#If you randomize, it takes up 33-90% of you screen, otherwise it's just 90%
randomize_x_y_size = options[2].split(" = ")[1]
if randomize_x_y_size == "True\n":
    randomize_x_y_size = True
else:
    randomize_x_y_size = False

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

#If you want the start and target as far from each other as possible.
make_on_opposite_sides = options[7].split(" = ")[1]
if make_on_opposite_sides == "True":
    make_on_opposite_sides = True
else:
    make_on_opposite_sides = False




start_time = time.time()


#Loops, searching tiles next to the current one, picks another tile, does it again.
#Better to use a while loop than recursive function calls because of the recursion limit.
def searchnear(tile):
    global unsearched
    global tiles
    global canvas
    global target_found

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

        #If it's on edges, don't check certain nearby tiles
        if ind%y_width == 0:
            ups = False
        if (ind+1)%y_width == 0:
            downs = False
        if 0 <= ind < y_width:
            lefts = False
        if x_width*y_width - 1 - y_width <= ind < x_width*y_width:
            rights = False

        #Appends nearby tiles to list if they're not obstructions and haven't been searched yet
        if lefts:
            left = tiles[ind - y_width]
            if not left[1] and not left[2]:
                new_dist = current_distance + 1
                if new_dist < left[3]:
                    left[3] = new_dist
                valids.append(left)
        else:
            left = False
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
        if rights:
            right = tiles[ind + y_width]
            if not right[1] and not right[2]:
                new_dist = current_distance + 1
                if new_dist < right[3]:
                    right[3] = new_dist
                valids.append(right)
        else:
            right = False
        
        #Tile has been searched
        tile[2] = True

        #Nearby valid tiles are now considered unsearched
        for unsearched_tile in valids:
            if not unsearched_tile[2] and unsearched_tile not in unsearched:
                unsearched.append(unsearched_tile)
            canvas.itemconfigure(unsearched_tile[0], fill = "blue")
            if show_distances:
                canvas.create_text(getx1(unsearched_tile[0])+tile_width//2,gety1(unsearched_tile[0])+tile_width//2, text = f"{unsearched_tile[3]}")
            canvas.update()

        try:
            #Guess a next tile, check all unsearched tiles (blue ones) to see which is closest to the start, search that one next.
            next_tile = unsearched[0]
            min = next_tile[3]
            for possible in unsearched:
                if possible[3] < min and not possible[2]:
                    min = possible[3]
                    next_tile = possible
                
            #If target is found, search for the shortest path back to the start
            if next_tile == target_tile:
                target_found = True
                canvas.itemconfigure(next_tile[0], fill = "#FF00FF")
                #canvas.update()
                searchforpath(target_tile)
                root.quit()
                del unsearched
                return 0

            if not next_tile[2]:
                tile = next_tile
        except:
            if not target_found:
                #canvas.create_text(root_width//2,root_height//2, text = "No possible paths!", font = "Helvetica 31 bold", fill = "black")
                canvas.create_text(root_width//2,root_height//2, text = "No possible paths!", font = "Helvetica 30 bold", fill = "red")
                root.quit()
                return 0
    

#Given the target tile, finds the shortest path back to the start tile
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

        #Which ones to ignore
        if ind%y_width == 0:
            ups = False
        if (ind+1)%y_width == 0:
            downs = False
        if 0 <= ind < y_width:
            lefts = False
        if x_width*y_width - 1 - y_width <= ind < x_width*y_width:
            rights = False

        #Checking nearby
        if lefts:
            left = tiles[ind - y_width]
            if not left[1]:
                valids.append(left)
        else:
            left = False
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
        if rights:
            right = tiles[ind + y_width]
            if not right[1]:
                valids.append(right)
        else:
            right = False

        try:
            #Guess next tile, take the one with the lowest distance from the start.
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
                #Do I even need this lmao
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

#Turns white tile into obstruction with click and drag. Doesn't work on start/target or searched tiles
def makeobstruction(event):
    x = event.x
    y = event.y

    for tile in tiles:
        if getx1(tile[0]) <= x <= getx2(tile[0]) and gety1(tile[0]) <= y <= gety2(tile[0]):
            #print(tiles.index(tile))
            if not tile[1] and not tile[2] and tile != target_tile and tile != start_tile:
                tile[1] = True
                canvas.itemconfigure(tile[0], fill = "#222222")


#tkinter widget
root = Tk()

background_color = "#FFFFFF"



#Tiles take up anywhere from 1/3 to 99% of the screen in width, 1/3 to 90% in height if the randomize option is true
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

#Tiles is a 2D list.
#For each list, 0 is the tile, 1 is if it's an obstruction, 2 is if it's been searched, 3 is the distance from the start.
tiles = []
for i in range(x_width):
    for j in range(y_width):
        new_rect = canvas.create_rectangle(tile_width*i,tile_width*j,tile_width*i+tile_width,tile_width*j+tile_width,fill = background_color, outline = "#666666", width = 2)
        #Distance from start is originally unknown so it's assigned the max possible value.
        tiles.append([new_rect, False, False, sys.maxsize])


#Randomly makes obstructions
for i in tiles:
    obstruct = random.uniform(0,1)
    if obstruct <= obstruction_chance:
        canvas.itemconfigure(i[0], fill = "#222222")
        i[1] = True


#Randomly chooses target tile
target_tile = random.choice(tiles)
if target_tile[1]:
    while target_tile[1]:
        target_tile = random.choice(tiles)
if make_on_opposite_sides:
    target_tile = tiles[0]
    target_tile[1] = False
canvas.itemconfigure(target_tile[0], fill = "red")


#Randomly chooses start tile
start_tile = random.choice(tiles)
if (canvas.coords(start_tile[0]) == canvas.coords(target_tile[0])) or start_tile[1]:
    while (canvas.coords(start_tile[0]) == canvas.coords(target_tile[0])) or start_tile[1]:
        start_tile = random.choice(tiles)
if make_on_opposite_sides:
    start_tile = tiles[-1]
    start_tile[1] = False
canvas.itemconfigure(start_tile[0], fill = "#11DD11")
start_tile[3] = 0

#Originally, only the start tile is considered unsearched.
unsearched = [start_tile]

#Makes makeobstruction work
canvas.bind("<B1-Motion>",makeobstruction)
canvas.pack()
searchnear(start_tile)
root.mainloop()