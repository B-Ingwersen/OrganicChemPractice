
from tkinter import *
from organicMolecule import *

canvas_width = 800
canvas_height = 500

def sizechange(event):
    canvas.delete(ALL)
    global canvas_width, canvas_height
    w,h = event.width,event.height
    canvas_width = w
    canvas_height = h
    m.draw(canvas, canvas_width, canvas_height)
    keyPress(None)

textInput = ""
cursorLocation = 0
lastText = None
def keyPress(event):
    global textInput, cursorLocation, lastText, m
    keyCode = 0
    if event is not None:
        keyCode = event.keycode
    color = "#cccccc"
    if keyCode == 22:
        if cursorLocation != 0:
            textInput = textInput[:cursorLocation - 1] + textInput[cursorLocation:]
            cursorLocation -= 1
    elif keyCode in range(24,34) or keyCode in range(38,47) or keyCode in range(52,62) or keyCode in range(10,21) or keyCode in [65]:
        textInput = textInput[:cursorLocation] + event.char + textInput[cursorLocation:]
        cursorLocation += 1
    elif keyCode in [83,113]:
        if cursorLocation > 0:
            cursorLocation -= 1
    elif keyCode in [85,114]:
        if cursorLocation < len(textInput):
            cursorLocation += 1
    
    elif keyCode == 36:
        if textInput == m.name:
            textInput = ""
            cursorLocation = 0
            canvas.delete(ALL)
            m = organicMolecule("")
            m.draw(canvas, canvas_width, canvas_height)
        else:
            color = "#fc8080"
    elif keyCode == 23:
        print(m.name)
        textInput = ""
        cursorLocation = 0
        canvas.delete(ALL)
        m = organicMolecule("")
        m.draw(canvas, canvas_width, canvas_height)

    printText = textInput[:cursorLocation] + "_" + textInput[cursorLocation:]
    width = 600
    x = canvas_width / 2 - width / 2
    y = canvas_height - 30
    canvas.create_rectangle(x,y,x+width,y+20, fill=color)
    newText = canvas.create_text(x + 5, y + 2, text=printText, anchor='nw')
    if lastText != None:
        canvas.delete(lastText)
    lastText = newText

root = Tk()

frame = Frame(root, width = canvas_width,height = canvas_height)
frame.bind('<Configure>', sizechange)
root.bind('<Key>', keyPress)
frame.pack(fill=BOTH, expand=YES)

canvas = Canvas(frame, bg = 'white', width = canvas_width, height = canvas_height)
canvas.pack(fill=BOTH, expand=YES)

m = organicMolecule("");
m.generateRandom()
m.draw(canvas, canvas_width, canvas_height)

root.mainloop()
