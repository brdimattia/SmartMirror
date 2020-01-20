from tkinter import Frame, Label, LEFT, RIGHT, TOP, NW, SE, N, E, S, W, SW, Canvas
from src.python.constants.common import BLACK, WHITE, ICON_LOOKUP, MULI, MULI_EXTRABOLD, FRANK_RUHL_LIBRE_BLACK
from src.python.util.common_utility import get_ip, get_location, convert_fahrenheit_to_celcius, convert_fahrenheit_to_kelvin
from src.python.constants.user_config import WEATHER_API_TOKEN, WEATHER_UNIT, WEATHER_LANG, TEMPERATURE_UNIT
from src.python.modules.weather.weather_constants import TEMPERATURE_TEXT_SIZE, DEGREE_SIGN, DEGREE_UNIT_TEXT_SIZE, WEATHER_DETAILS_TEXT_SIZE, HUMIDITY, WEATHER_REQUEST_ENDPOINT, WEATHER_REFRESH_RATE, FAHRENHEIT, CELCIUS, KELVIN
from PIL import Image, ImageTk
import requests
import json
import traceback

class Weather(Frame):

    def render_ui(self, update_fields):
        if "icon" in update_fields:
            self.set_icon()
        if "temperature" in update_fields:
            self.temperature_canvas.delete("all")
            self.temperature_text = self.temperature_canvas.create_text(0, -48, text=self.temperature, fill=WHITE, font=(MULI_EXTRABOLD, TEMPERATURE_TEXT_SIZE), anchor=NW)  
            self.temperature_bounding_box = self.temperature_canvas.bbox(self.temperature_text)
            self.temperature_canvas.configure(width=self.temperature_bounding_box[2], height=self.temperature_bounding_box[3]-30)
        if "humidity" in update_fields:
            self.humidity_canvas.delete("all")
            self.humidity_text = self.humidity_canvas.create_text(0, -8, text="Humidity: %d%%" % self.humidity, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), anchor=NW)  
            self.humidity_bounding_box = self.humidity_canvas.bbox(self.humidity_text)
            self.humidity_canvas.configure(width=self.humidity_bounding_box[2], height=self.humidity_bounding_box[3]-8)
        if "forecast" in update_fields:
            self.forecast_canvas.delete("all")
            self.forecast_text = self.forecast_canvas.create_text(0, -8, text=self.forecast, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), anchor=NW)  
            self.forecast_bounding_box = self.forecast_canvas.bbox(self.forecast_text)
            self.forecast_canvas.configure(width=self.forecast_bounding_box[2], height=self.forecast_bounding_box[3]-8)

    def set_icon(self):
        self.icon_canvas.delete(all)
        if self.icon_id in ICON_LOOKUP:
            icon_path = ICON_LOOKUP[self.icon_id]
        if icon_path is not None:
            self.icon_canvas.delete("all")
            self.icon = Image.open(icon_path)
            self.icon = self.icon.resize((110, 110), Image.ANTIALIAS)
            self.icon = self.icon.convert('RGB')
            self.icon = ImageTk.PhotoImage(self.icon)
            self.icon_canvas.create_image(0, 0, image=self.icon, anchor=NW)
        else:
            print("No icon path for id: %s" % icon_path)

    def update_weather(self):
        try:
            weather_req_url = WEATHER_REQUEST_ENDPOINT % (WEATHER_API_TOKEN, self.latitude, self.longitude, WEATHER_LANG, WEATHER_UNIT)
            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)
            update_fields = []
            if TEMPERATURE_UNIT == CELCIUS:
                latest_temperature = convert_fahrenheit_to_celcius(int(weather_obj['currently']['temperature']))
            elif TEMPERATURE_UNIT == KELVIN:
                latest_temperature = convert_fahrenheit_to_kelvin(int(weather_obj['currently']['temperature']))
            else:
                latest_temperature = int(weather_obj['currently']['temperature'])
            if self.temperature != latest_temperature:
                update_fields.append("temperature")
                self.temperature = latest_temperature
            if self.forecast != weather_obj['currently']['summary']:
                update_fields.append("forecast")
                self.forecast = weather_obj['currently']['summary']
            if self.humidity != weather_obj['currently']['humidity']:
                update_fields.append("humidity")
                self.humidity = int(float(weather_obj['currently']['humidity']) * 100)
            if self.icon_id != weather_obj['currently']['icon']:
                update_fields.append("icon")
                self.icon_id = weather_obj['currently']['icon']
            self.render_ui(update_fields)
        except Exception as e:
            traceback.print_exc()
            print("Error: %s. Cannot get weather." % e)
        self.after(WEATHER_REFRESH_RATE, self.update_weather)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg=BLACK, height=100)

        self.ip = get_ip()
        self.longitude, self.latitude, self.city_region = get_location(self.ip)
        self.temperature = None
        self.forecast = None
        self.icon_id = None
        self.humidity = None
        self.current_icon_path = None


        self.icon_canvas = Canvas(self, bg=BLACK, height=110, width=110, bd=0, highlightthickness=0)
        self.icon_canvas.grid(row=0, column=0, rowspan=3, columnspan=2, sticky=SE, padx=10)

        self.temperature_canvas = Canvas(self, bg=BLACK, height=110, width=150, bd=0, highlightthickness=0)
        self.temperature_canvas.grid(row=0, column=2, rowspan=3, columnspan=3, sticky=SW)

        self.degree_unit_canvas = Canvas(self, bg=BLACK, bd=0, highlightthickness=0)
        self.degree_unit_canvas.grid(row=0, column=5, rowspan=3, columnspan=1, sticky=NW)
        self.degree_unit_text = self.degree_unit_canvas.create_text(0, -20, text="%s%s" % (DEGREE_SIGN, TEMPERATURE_UNIT), fill=WHITE, font=(MULI_EXTRABOLD, DEGREE_UNIT_TEXT_SIZE), anchor=NW)  
        self.degree_unit_bounding_box = self.degree_unit_canvas.bbox(self.degree_unit_text)
        self.degree_unit_canvas.configure(width=self.degree_unit_bounding_box[2], height=self.degree_unit_bounding_box[3]-12)

        self.forecast_canvas = Canvas(self, bg=BLACK, bd=0, highlightthickness=0)
        self.forecast_canvas.grid(row=0, column=6, rowspan=1, columnspan=5, sticky=SW, padx=20)

        self.humidity_canvas = Canvas(self, bg=BLACK, bd=0, highlightthickness=0)
        self.humidity_canvas.grid(row=1, column=6, rowspan=1, columnspan=5, sticky=SW, padx=20)

        self.city_region_canvas = Canvas(self, bg=BLACK, bd=0, highlightthickness=0)
        self.city_region_canvas.grid(row=2, column=6, rowspan=1, columnspan=5, sticky=SW, padx=20)
        self.city_region_text = self.city_region_canvas.create_text(0, -8, text=self.city_region, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), anchor=NW)  
        self.city_region_bounding_box = self.city_region_canvas.bbox(self.city_region_text)
        self.city_region_canvas.configure(width=self.city_region_bounding_box[2], height=self.city_region_bounding_box[3]-8)

        # self.outside_frame = Frame(self, bg=BLACK, height=110)
        # self.outside_frame.pack(side=TOP, fill=None, expand=False)
        # self.icon_label = Label(self.outside_frame, bg=BLACK)
        # self.icon_label.grid(row = 0, column = 0, sticky = S, pady=30) 
        # self.temperature_frame = Frame(self.outside_frame, bg=BLACK)
        # self.temperature_frame.grid(row = 0, column = 1, sticky = S) 
        # self.details_frame = Frame(self.outside_frame, bg=BLACK)
        # self.details_frame.grid(row = 0, column = 2, sticky = S, pady=20, padx=5) 
        # self.temperature_label = Label(self.temperature_frame, font=(MULI_EXTRABOLD, TEMPERATURE_TEXT_SIZE), fg=WHITE, bg=BLACK)
        # self.temperature_label.grid(row = 0, column = 0, sticky = S) 
        # self.degree_unit_label = Label(self.temperature_frame, font=(MULI_EXTRABOLD, DEGREE_UNIT_TEXT_SIZE), fg=WHITE, bg=BLACK)
        # self.degree_unit_label.grid(row = 0, column = 1, sticky = S, pady=75) 
        # self.degree_unit_label.config(text="%s%s" % (DEGREE_SIGN, TEMPERATURE_UNIT))
        # self.forecast_label = Label(self.details_frame, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), fg=WHITE, bg=BLACK)
        # self.forecast_label.grid(row = 0, column = 0, sticky = W) 
        # self.humidity_label = Label(self.details_frame, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), fg=WHITE, bg=BLACK)
        # self.humidity_label.grid(row = 1, column = 0, sticky = W) 
        # self.city_region_label = Label(self.details_frame, font=(FRANK_RUHL_LIBRE_BLACK, WEATHER_DETAILS_TEXT_SIZE), fg=WHITE, bg=BLACK)
        # self.city_region_label.grid(row = 2, column = 0, sticky = W)

        self.update_weather()