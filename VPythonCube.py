"""
Cameron Ladjevardi
05/19/17
CPSC 484 Assignment #5

Rubik's Cube created with VPython

======================================================================"""
from __future__ import division, print_function
from visual import *
import wx

scene = display(title='VPython Cube', x=0, y=0, width=750, height=750,
                center=(0, 0, 0), background=(1, 1, 1))

# Map keyboard keys to each face. Program starts facing blue.
# The commented numbers represet the cube if flattened on a numpad.
faces = {'d': (color.red, (1, 0, 0)),           #6  right
         'a': (color.orange, (-1, 0, 0)),       #4  left
         'c': (color.magenta, (0, 0, -1)),      #0  back
         'w': (color.yellow, (0, 1, 0)),        #8  top
         's': (color.blue, (0, 0, 1)),          #5  face
         'x': (color.green, (0, -1, 0))}        #2  bottom

# Text that informs the user of what key rotates which face.
topText = text(text = "W", pos =(-0.7,2.5,0),opacity = 0.5, depth=0.03, material = materials.unshaded,
               color = color.gray(0.5))
leftText = text(text = "A", pos =(-3.5,-0.5 ,0), depth=0.03, material = materials.unshaded,
                color = color.gray(0.5))
rightText = text(text = "D", pos =(2.5,-0.5 ,0), depth=0.03, material = materials.unshaded,
                 color = color.gray(0.5))
bottomText = text(text = "X", pos =(-0.5,-3.5 ,0), depth=0.03, material = materials.unshaded,
                  color = color.gray(0.4))
faceText = text(text = "S", pos =(-0.3,-0.5 ,2.5), depth=0.03, material = materials.unshaded,
                color = color.gray(0.5))
backText = text(text = "C", pos =(-0.4,-0.5 ,-2.5), depth=0.03, material = materials.unshaded,
                color = color.gray(0.5))
# Rotate the C so it isn't backwards when looking at the back of the cube.
backText.rotate(angle = pi, axis =(0,1,0),origin =(0.05,-0.5 ,-2.5))

# Create the colored squares on each face as well as the inner cubes
squares = []
for faceColor, axis in faces.values():
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            # Creates the colored squares.
            square = box(material = materials.unshaded, color = faceColor, pos = (x, y, 1.40),
                          length = 0.7, height = 0.7, width = 0.1)
            cosAngle = dot((0, 0, 1), axis)
            pivot = (cross((0, 0, 1), axis) if cosAngle == 0 else (1, 0, 0))
            square.rotate(angle = acos(cosAngle), axis = pivot, origin =(0, 0, 0))
            squares.append(square)

            # Creates the inner cubes.
            center = box(color = color.gray(0.1), material = materials.emissive,
                       pos = (x, y, 1), length = 0.85, height = 0.85, width = 0.85)
            center.rotate(angle = acos(cosAngle), axis = pivot, origin = (0, 0, 0))
            squares.append(center)
        
controls = 0
# Map keyboard to rotate respective faces.
while True:
    key = scene.kb.getkey()

    # If the controls haven't been displayed yet they will appear.   
    if controls == 0:
        wx.MessageBox("""
ROTATION: W, A, S, D, X, or C will rotate the respective face clockwise.
SHIFT: Holding SHIFT + ROTATION will spin the face counter-clockwise.
RIGHT MOUSE: Holding down the RMB and dragging allows you to rotate the camera.
MIDDLE MOUSE: Holding down the MMB and dragging allows you to zoom in or out.
""", 'CONTROLS', wx.OK)
        controls = 1
        
    if key.lower() in faces:
        faceColor, axis = faces[key.lower()]
        # Lowercase press rotates clockwise, uppcase press rotates counter-clockwise.
        angle = ((pi / 2) if key.isupper() else -pi / 2)
        for r in arange(0, angle, angle / 10):
            rate(60)
            for square in squares:
                if dot(square.pos, axis) > 0.5:
                    square.rotate(angle = angle / 10, axis = axis,
                                  origin = (0, 0, 0))
