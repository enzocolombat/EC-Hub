"""Display a 3D cube whose rotation follows gyroscope data received by TCP."""

import socket   # Provides the TCP client used to receive Raspberry Pi sensor data.
import json      # Decodes each JSON line sent by the server.
import threading     # Runs network reception without freezing the graphics loop.
import pygame   # Creates the display window and handles window events.
from pygame.locals import *      # Imports Pygame constants such as DOUBLEBUF, OPENGL, and QUIT.
from OpenGL.GL import *     # Imports OpenGL drawing and matrix functions.
from OpenGL.GLU import *    # Imports GLU helpers such as perspective projection.


    # Shared gyroscope angles used by the receiver thread and the render loop.
angles = [0, 0, 0]   # Stores accumulated rotations around X, Y, and Z.
lock = threading.Lock()   # Protects angles when two threads access them at the same time.

def recevoir_donnees():     # Receives gyroscope packets from the Raspberry Pi server.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Creates a TCP/IPv4 client socket.
    client.connect(('192.168.1.172', 5000))     # Connects to the Raspberry Pi on port 5000.
    buffer = ""      # Keeps partial data until a full newline-terminated JSON packet arrives.
    while True:     # Keeps listening for sensor data for as long as the program runs.
        data = client.recv(1024).decode()     # Reads up to 1024 bytes and converts them to text.
        buffer += data      # Adds the newly received text to any unfinished previous packet.
        while "\n" in buffer:    # Processes every complete JSON line currently available.
            line, buffer = buffer.split("\n", 1)      # Splits one complete packet from the remaining buffer.
            try:      # Keeps the receiver alive even if one packet is malformed.
                d = json.loads(line)    # Converts the JSON text into a Python dictionary.
                with lock:      # Locks shared angle data while updating it.
                    angles[0] += d['gx'] * 0.05     # Integrates gyroscope X speed into an X rotation angle.
                    angles[1] += d['gy'] * 0.05     # Integrates gyroscope Y speed into a Y rotation angle.
                    angles[2] += d['gz'] * 0.05     # Integrates gyroscope Z speed into a Z rotation angle.
            except Exception:     # Ignores bad packets so the display keeps running.
                pass     # Drops the unreadable packet without stopping the receiver.

# Start receiving sensor data in the background before opening the 3D loop.
t = threading.Thread(target=recevoir_donnees, daemon=True)  # Builds a daemon thread for network reception.
t.start()  # Starts the receiver thread immediately.

# Cube geometry: eight vertices, six faces, and one color per face.
vertices = [  # Lists the 3D coordinates of each cube corner.
    [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],  # Back face corners.
    [1, -1, 1],  [1, 1, 1],  [-1, -1, 1], [-1, 1, 1]  # Front face corners.
]
faces = [  # Lists each cube face as indexes into the vertices list.
    [0, 1, 2, 3], [3, 2, 7, 6], [6, 7, 5, 4],  # Three faces of the cube.
    [4, 5, 1, 0], [1, 5, 7, 2], [4, 0, 3, 6]  # Three remaining faces of the cube.
]
colors = [  # Gives each face a different RGB color.
    [1, 0, 0], [0, 1, 0], [0, 0, 1],  # Red, green, and blue faces.
    [1, 1, 0], [1, 0, 1], [0, 1, 1]  # Yellow, cyan, and magenta faces.
]

def draw_cube():  # Draws the cube once using the current OpenGL matrix.
    glBegin(GL_QUADS)  # Starts drawing quadrilateral faces.
    for i, face in enumerate(faces):  # Iterates over each face with its color index.
        glColor3fv(colors[i])  # Selects the color for the current face.
        for v in face:  # Iterates over the four vertex indexes of the face.
            glVertex3fv(vertices[v])  # Sends one corner of the face to OpenGL.
    glEnd()  # Finishes the quadrilateral drawing batch.

pygame.init()  # Initializes Pygame before creating the window.
screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)  # Creates an OpenGL window with double buffering.
pygame.display.set_caption("Cube 3D - MPU6050")  # Sets the window title.
gluPerspective(45, 800 / 600, 0.1, 50.0)  # Configures a perspective camera.
glTranslatef(0, 0, -5)  # Moves the cube away from the camera so it is visible.

while True:  # Runs the render loop until the user closes the window.
    for event in pygame.event.get():  # Reads pending Pygame window events.
        if event.type == QUIT:  # Detects a window close request.
            pygame.quit()  # Shuts down Pygame cleanly.
            quit()  # Ends the Python process.

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clears the screen before drawing the next frame.
    glPushMatrix()  # Saves the current transform so cube rotation does not accumulate visually.
    with lock:  # Locks angles while reading them for rendering.
        glRotatef(angles[0], 1, 0, 0)  # Applies rotation around the X axis.
        glRotatef(angles[1], 0, 1, 0)  # Applies rotation around the Y axis.
        glRotatef(angles[2], 0, 0, 1)  # Applies rotation around the Z axis.
    draw_cube()  # Draws the cube with the current rotations.
    glPopMatrix()  # Restores the transform for the next frame.
    pygame.display.flip()  # Swaps the back buffer to the screen.
    pygame.time.wait(10)  # Waits briefly to avoid burning CPU unnecessarily.
