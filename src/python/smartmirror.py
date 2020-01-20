import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from tkinter import Tk, Label, Frame, TOP, LEFT, RIGHT, BOTTOM, BOTH, YES, NONE, N, S
from src.python.constants.common import APP_NAME, FULLSCREEN, BREAK, BLACK
from src.python.modules.message.message import Message
from src.python.modules.weather.weather import Weather
from src.python.modules.clock.clock import Clock
from src.python.modules.spotify.spotify import Spotify
from src.python.modules.transit.transit import Transit

class SmartMirror:

    def toggle_fullscreen(self, event=None):
        self.fullscreen_state = not self.fullscreen_state
        self.tk.attributes(FULLSCREEN, self.fullscreen_state)
        return BREAK

    def __init__(self):
        print("Initializing Smart Mirror")
        self.fullscreen_state = False
        self.tk = Tk()
        self.tk.configure(background=BLACK)
        self.topMostFrame = Frame(self.tk, background=BLACK, cursor = NONE)
        self.topFrame = Frame(self.topMostFrame, background=BLACK, cursor = NONE)
        self.bottomFrame = Frame(self.tk, background = BLACK, cursor = NONE)
        self.topMostFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.topFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)


        # message binding
        self.message = Message(self.topMostFrame)
        self.message.pack(side=TOP, anchor=N, pady=30)

        # weather binding
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=50)

        # transit binding
        self.transit = Transit(self.topFrame)
        self.transit.pack(side=RIGHT, anchor=N, padx=50)

        # clock binding
        self.clock = Clock(self.bottomFrame)
        self.clock.pack(side=RIGHT, anchor=S, padx=50, pady=30)

        # spotify binding
        self.spotify = Spotify(self.bottomFrame)
        self.spotify.pack(side=LEFT, anchor=S, padx=50, pady=30)

        # self.tk.bind("<c>", self.focus_clock)
        # self.tk.bind("<h>", self.focus_home)
        # self.tk.bind("<w>", self.focus_weather)

        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.toggle_fullscreen)
        ## OFF FOR TESTING
        #self.toggle_fullscreen(None)

if __name__ == '__main__':
    controller = SmartMirror()
    controller.tk.mainloop()