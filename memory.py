import simpleguitk as simplegui
import random

numbers_list = []
exposed = []
state = 0
index1 = -1
index2 = -1
turns = 0


# helper function to initialize globals
def new_game():
    global numbers_list, turns, state, exposed
    exposed = []
    turns = 0
    label.set_text("Turns = " + str(turns))
    numbers_list = [0, 1, 2, 3, 4, 5, 6, 7]
    numbers_list.extend(numbers_list)
    random.shuffle(numbers_list)
    for i in range(len(numbers_list)):
        exposed.append(False)


# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, numbers_list, turns, index1, index2
    if state == 0:
        index1 = pos[0] // 50
        exposed[index1] = True
        state = 1
    elif state == 1:
        temp = pos[0] // 50
        if not exposed[temp]:
            state = 2
            index2 = pos[0] // 50
            if not exposed[index2]:
                exposed[index2] = True
                turns += 1
                label.set_text("Turns = " + str(turns))
    else:
        temp = pos[0] // 50
        if not exposed[temp]:
            if numbers_list[index1] != numbers_list[index2]:
                exposed[index1] = False
                exposed[index2] = False
            index1 = pos[0] // 50
            if not exposed[index1]:
                exposed[index1] = True
            state = 1


# cards are logically 50x100 pixels in size
def draw(canvas):
    global numbers_list
    for i in range(len(numbers_list)):
        canvas.draw_text(str(numbers_list[i]), (10 + 50 * i, 75), 50, 'White')
    for i in range(len(exposed)):
        if not exposed[i]:
            canvas.draw_polygon([[50 * i, 0], [50 + 50 * i, 0], [50 + 50 * i, 100], [50 * i, 100]], 2, "White", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
