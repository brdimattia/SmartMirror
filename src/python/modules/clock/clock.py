
from tkinter import Frame, Canvas, SE, SW, NW
from src.python.constants.common import BLACK, WHITE, FRANK_RUHL_LIBRE_BLACK, MULI_LIGHT
from src.python.modules.clock.clock_constants import TIME_TEXT_SIZE, DATE_TEXT_SIZE, AM_PM_TEXT_SIZE, TIME_REFRESH_RATE
from src.python.util.common_utility import setlocale
from src.python.constants.user_config import UI_LOCALE, TIME_FORMAT
import time as pytime


class Clock(Frame):
    
    def update_time(self):
        with setlocale(UI_LOCALE):
            if TIME_FORMAT == 12:
                time_update = pytime.strftime('%I:%M') #hour in 12h format
            else:
                time_update = pytime.strftime('%H:%M') #hour in 24h format

            date_update = pytime.strftime("%m.%d.%y")
            am_pm_update = pytime.strftime("%p")
            if time_update != self.current_time:
                self.current_time = time_update
                self.time_canvas.delete("all")
                self.time_text = self.time_canvas.create_text(0, -40, text=self.current_time, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, TIME_TEXT_SIZE), anchor=NW)  
                self.time_bounding_box = self.time_canvas.bbox(self.time_text)
                self.time_canvas.configure(width=self.time_bounding_box[2], height=self.time_bounding_box[3]-50)
            if date_update != self.current_date:
                self.current_date = date_update
                self.date_canvas.delete("all")
                self.date_text = self.date_canvas.create_text(0, -10, text=self.current_date, fill=WHITE, font=(MULI_LIGHT, DATE_TEXT_SIZE), anchor=NW)  
                self.date_bounding_box = self.date_canvas.bbox(self.date_text)
                self.date_canvas.configure(width=self.date_bounding_box[2], height=self.date_bounding_box[3]-10)
            if am_pm_update != self.current_am_pm:
                self.current_am_pm = am_pm_update
                self.am_pm_canvas.delete("all")
                self.am_pm_text = self.am_pm_canvas.create_text(0, -25, text=self.current_am_pm, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, AM_PM_TEXT_SIZE), anchor=NW)  
                self.am_pm_bounding_box = self.am_pm_canvas.bbox(self.am_pm_text)
                self.am_pm_canvas.configure(width=self.am_pm_bounding_box[2], height=self.am_pm_bounding_box[3]-30)
            
            self.after(TIME_REFRESH_RATE, self.update_time)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg=BLACK)        
        
        self.current_time = None
        self.current_am_pm = None
        self.current_date = None

        self.time_canvas = Canvas(self, bg=BLACK, height=150, width=450, bd=0, highlightthickness=0)
        self.time_canvas.grid(row=0, column=0, rowspan=3, columnspan=2, sticky=SE, padx=20)
        self.time_text = self.time_canvas.create_text(0, -40, text=self.current_time, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, TIME_TEXT_SIZE), anchor=NW)  
        self.time_bounding_box = self.time_canvas.bbox(self.time_text)
        self.time_canvas.configure(width=self.time_bounding_box[2], height=self.time_bounding_box[3]-50)

        self.date_canvas = Canvas(self, bg=BLACK, height=50, width=160, bd=0, highlightthickness=0)
        self.date_canvas.grid(row=0, column=2, rowspan=1, columnspan=1, sticky=SW)
        self.date_text = self.date_canvas.create_text(0, -10, text=self.current_date, fill=WHITE, font=(MULI_LIGHT, DATE_TEXT_SIZE), anchor=NW)  
        self.date_bounding_box = self.date_canvas.bbox(self.date_text)
        self.date_canvas.configure(width=self.date_bounding_box[2], height=self.date_bounding_box[3]-10)

        self.am_pm_canvas = Canvas(self, bg=BLACK, height=100, width=160, bd=0, highlightthickness=0)
        self.am_pm_canvas.grid(row=1, column=2, rowspan=1, columnspan=1, sticky=SW)
        self.am_pm_text = self.am_pm_canvas.create_text(0, -25, text=self.current_am_pm, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, AM_PM_TEXT_SIZE), anchor=NW)  
        self.am_pm_bounding_box = self.am_pm_canvas.bbox(self.am_pm_text)
        self.am_pm_canvas.configure(width=self.am_pm_bounding_box[2], height=self.am_pm_bounding_box[3]-30)

        self.update_time()


    