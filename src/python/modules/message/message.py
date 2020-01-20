from src.python.modules.message.message_constants import GOOD_MORNING, GOOD_AFTERNOON, GOOD_EVENING, MESSAGE_REFRESH_RATE, MESSAGE_TEXT_SIZE, DEFAULT_MESSAGE
from src.python.constants.user_config import USER_FIRST_NAME, UI_LOCALE
from src.python.constants.common import BLACK, WHITE, MULI_BOLD
from tkinter import Frame, Label, TOP, N
import time
from src.python.util.common_utility import setlocale

class Message(Frame):

    def get_message(self):
        with setlocale(UI_LOCALE):
            message = ''
            hour_of_day = int(time.strftime('%H'))
            if hour_of_day > 4 and hour_of_day <= 11:
                message = GOOD_MORNING % USER_FIRST_NAME
            elif hour_of_day < 18:
                message =  GOOD_AFTERNOON % USER_FIRST_NAME
            else:
                message = GOOD_EVENING % USER_FIRST_NAME
            self.message_label.config(text=message)
            self.after(MESSAGE_REFRESH_RATE, self.get_message)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg=BLACK)
        self.message_label = Label(self, text=DEFAULT_MESSAGE, font=(MULI_BOLD, MESSAGE_TEXT_SIZE), fg=WHITE, bg=BLACK)
        self.message_label.pack(side=TOP, anchor=N, padx=10)
        self.get_message()