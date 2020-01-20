# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow, spotipy

from Tkinter import *
import locale
import threading
import time
import datetime
import requests
import json
import traceback
import spotipy
import spotipy.util as util
from PIL import Image, ImageTk
from contextlib import contextmanager
import skywriter
import signal
import os


# Run these commands as part of setup
# pip install spotipy
# pip install --upgrade git+https://github.com/happyleavesaoc/spotipy@connect-api
# TODO: Figure out how to add real spotipy to requirements
# export SPOTIPY_CLIENT_ID='f776e00490d14fedb7c3757aa1e410c7'
# export SPOTIPY_CLIENT_SECRET='cac4c4fbb6a34a2c8829382eb32886ee'
# export SPOTIPY_REDIRECT_URI='https://www.google.com'

LOCALE_LOCK = threading.Lock()
# CLOCK GLOBAL VARS
ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
CLOCK_REFRESH_RATE = 200 # 0.2 seconds
# WEATHER GLOBAL VARS
geo_ip_token = '9e3dd33fa5a321f55fffa91eb39ff13e' # create an account at http://ipstack.com
weather_api_token = 'fd7b89f72fd29be98d6c2d75a4ca5156' # create account at https://darksky.net/dev/
weather_lang = 'en' # see https://darksky.net/dev/docs/forecast for full list of language parameters values
weather_unit = 'us' # see https://darksky.net/dev/docs/forecast for full list of unit parameters values
WEATHER_REFRESH_RATE = 600000 # 10 Minutes
latitude = None # '42.5051' # Set this if IP location lookup does not work for you (must be a string)
longitude = None # '71.2047' # Set this if IP location lookup does not work for you (must be a string)
# SPOTIFY GLOBAL VARS
SPOTIFY_USERNAME = 'brdimattia'
SPOTIFY_REFRESH_RATE = 1000 # 1 Second
SPOTIFY_REQUEST_TIMEOUT = 10 # 10 seconds
# MESSAGE GLOBAL VARS
USER_FIRST_NAME = 'Ben'
MESSAGE_REFRESH_RATE = 3600000 # 1 hour
# UI GLOBAL VARS
xxlarge_text_size = 170
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 16
xsmall_text_size = 8
# Skywriter GLOBAL VARS
skywriter_scope = None

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png",  # hail
    'spotify': 'assets/Spotify.png' # Spotify logo

}

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class LargeClock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', xxlarge_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black", wraplength=500, justify="left")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.get_current_weather()

    def get_ip(self):
        try:
            ip_url = "http://api.ipify.org?format=json"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_current_weather(self):
        try:
            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://api.ipstack.com/%s?access_key=%s" % (self.get_ip(), geo_ip_token)
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)
                lat = location_obj['latitude']
                lon = location_obj['longitude']
                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)
            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]
            icon_id = weather_obj['currently']['icon']
            icon2 = None
            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]
            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((100, 100), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()

        self.after(WEATHER_REFRESH_RATE, self.get_current_weather)

    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32


class LargeWeather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        self.forecast = ''
        self.location = ''
        self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=TOP, anchor=W)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=N)
        self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl.pack(side=LEFT, anchor=N, padx=20)
        self.currentlyLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.currentlyLbl.pack(side=TOP, anchor=W)
        self.forecastLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black", wraplength=900, justify="left")
        self.forecastLbl.pack(side=TOP, anchor=W)
        self.locationFrame = Frame(self, bg="black")
        self.locationFrame.pack(side=TOP, anchor=W)
        self.locationLbl = Label(self.locationFrame, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.locationLbl.pack(side=TOP, anchor=W)
        self.day_of_week = ''
        self.dayOWLbl = Label(self.locationFrame, text=self.day_of_week, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=W)


        self.parentFrame = self
        self.weatherJson =self.get_hourly_weather()
        self.hourlyFrame = self.getHourlyFrame(self.parentFrame, self.weatherJson)
        self.hourlyFrame.pack(side=TOP, anchor=N)

    def get_ip(self):
        try:
            ip_url = "http://api.ipify.org?format=json"
            req = requests.get(ip_url)
            ip_json = json.loads(req.text)
            return ip_json['ip']
        except Exception as e:
            traceback.print_exc()
            return "Error: %s. Cannot get ip." % e

    def get_hourly_weather(self):
        with setlocale(ui_locale):
            day_of_week = time.strftime('%A')
            self.dayOWLbl.config(text=day_of_week)
        try:
            if latitude is None and longitude is None:
                # get location
                location_req_url = "http://api.ipstack.com/%s?access_key=%s" % (self.get_ip(), geo_ip_token)
                r = requests.get(location_req_url)
                location_obj = json.loads(r.text)
                lat = location_obj['latitude']
                lon = location_obj['longitude']
                location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            else:
                location2 = ""
                # get weather
                weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)
            r = requests.get(weather_req_url)
            weather_obj = json.loads(r.text)

            degree_sign= u'\N{DEGREE SIGN}'
            temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            currently2 = weather_obj['currently']['summary']
            forecast2 = weather_obj["hourly"]["summary"]
            icon_id = weather_obj['currently']['icon']
            icon2 = None
            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]
            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((200, 200), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(image=photo)
                    self.iconLbl.image = photo
            else:
                # remove image
                self.iconLbl.config(image='')

            if self.currently != currently2:
                self.currently = currently2
                self.currentlyLbl.config(text=currently2)
            if self.forecast != forecast2:
                self.forecast = forecast2
                self.forecastLbl.config(text=forecast2)
            if self.temperature != temperature2:
                self.temperature = temperature2
                self.temperatureLbl.config(text=temperature2)
            if self.location != location2:
                if location2 == ", ":
                    self.location = "Cannot Pinpoint Location"
                    self.locationLbl.config(text="Cannot Pinpoint Location")
                else:
                    self.location = location2
                    self.locationLbl.config(text=location2)
        except Exception as e:
            traceback.print_exc()

        self.after(WEATHER_REFRESH_RATE, self.update_weather_json)
        return weather_obj

    def update_weather_json(self):
        self.weatherJson = self.get_hourly_weather()
        self.hourlyFrame = self.getHourlyFrame(self.parentFrame, self.weatherJson)

    def getHourlyFrame(self, parent, hourlyJson):
        hourlyFrame = Frame(parent, bg="black")
        topSeparator = Frame(hourlyFrame, height=1, width=1000, bg="white")
        topSeparator.pack(padx=5, pady=3)
        degree_sign= u'\N{DEGREE SIGN}'
        for hourJson in hourlyJson['hourly']['data']:
            epochTime = datetime.datetime.fromtimestamp(hourJson['time'])
            hour = epochTime.hour
            ap = 'am'
            bar = '   |'         
            if hour == 0:
                timeStr='12am |'
            else:             
                if hour > 12:
                    hour = hour-12
                    ap = 'pm'
                if hour == 12:
                    ap = 'pm'
                if hour > 9:
                    bar = ' |'
                timeStr = str(hour) + ap + bar
            hourFrame = Frame(hourlyFrame, bg="black")
            strsFrame = Frame(hourFrame, bg="black", width=1000)
            hourLabel = Label(strsFrame, text=timeStr, font=('Helvetica', medium_text_size), fg="white", bg="black", justify="left", anchor=W)
            iconLbl = Label(strsFrame, bg="black")
            iconLbl.pack(side=RIGHT, anchor=N, padx=20)
            icon = ''
            icon_id = hourJson['icon']
            icon2 = None
            if icon_id in icon_lookup:
                icon2 = icon_lookup[icon_id]
            if icon2 is not None:
                if icon != icon2:
                    icon = icon2
                    image = Image.open(icon2)
                    image = image.resize((20, 20), Image.ANTIALIAS)
                    image = image.convert('RGB')
                    photo = ImageTk.PhotoImage(image)
                    iconLbl.config(image=photo)
                    iconLbl.image = photo
            hourLabel.pack(side=LEFT, anchor=W)
            tempStr = "%s%s" % (str(int(hourJson['temperature'])), degree_sign)
            tempLabel = Label(strsFrame, text=tempStr, font=('Helvetica', medium_text_size), fg="white", bg="black")
            tempLabel.pack(side=RIGHT, anchor=E)
            separator = Frame(hourFrame, height=1, width=1000, bg="white")
            separator.pack(side=BOTTOM, padx=5, pady=3)
            strsFrame.pack(side=TOP, fill=BOTH, expand=YES)
            hourFrame.pack()
           
        return hourlyFrame

    
		


    @staticmethod
    def convert_kelvin_to_fahrenheit(kelvin_temp):
        return 1.8 * (kelvin_temp - 273) + 32

class SpotifyDisplay(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.defaultSongName = ''
        self.defaultArtistName = ''
        self.defaultCollectionName = ''
        self.spotifyLogoLabel = Label(self, bg="black")
        self.spotifyLogoLabel.pack(side=RIGHT, anchor=S, padx=5)
        image = Image.open(icon_lookup['spotify'])
        image = image.resize((100, 100), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.spotifyLogoLabel.config(image=photo)
        self.spotifyLogoLabel.image = photo
        self.spotifyFrm1 = Frame(self, bg="black")
        self.spotifyFrm1.pack(side=BOTTOM, anchor=E)
        self.songNameLabel = Label(self.spotifyFrm1, text=self.defaultSongName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.songNameLabel.pack(side=TOP, anchor=E, padx=10)
        self.spotifyFrm2 = Frame(self.spotifyFrm1, bg="black")
        self.spotifyFrm2.pack(side=BOTTOM, anchor=E)
        self.artistNameLabel = Label(self.spotifyFrm2, text=self.defaultArtistName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.artistNameLabel.pack(side=TOP, anchor=E, padx=10)
        self.collectionNameLabel = Label(self.spotifyFrm2, text=self.defaultCollectionName, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.collectionNameLabel.pack(side=BOTTOM, anchor=E, padx=10)
        self.spotifyConnection = None
        self.spotifyToken = None
        self.getCurrentTrack()

    def getCurrentTrack(self):
        try:
            if self.spotifyConnection is None:
                self.spotifyToken = self.spotifyAuthenticateWithScope('user-read-currently-playing user-read-recently-played')
            if self.spotifyToken:
                trackResults = self.spotifyConnection.currently_playing(market='US')
                if trackResults: #User is currently listening to a song
                    track = trackResults['item']
                    self.updateUI(track)
                else: #User is not currently listening to a song
                    trackResults = self.spotifyConnection.current_user_recently_played(limit=1)
                    track = trackResults['items'][0]['track']
                    self.updateUI(track)
            else:
                self.spotifyConnection = None
        except Exception as e:
            print(e)
            self.spotifyConnection = None
        self.after(SPOTIFY_REFRESH_RATE, self.getCurrentTrack)

    def spotifyAuthenticateWithScope(self, scope):
        token = util.prompt_for_user_token(SPOTIFY_USERNAME, scope)
        if token:
            self.spotifyConnection = spotipy.Spotify(auth=token, requests_session=True, requests_timeout=SPOTIFY_REQUEST_TIMEOUT)
            #print "Successfuly retrieved token for spotify user: " + SPOTIFY_USERNAME
            return token
        else:
            print("Can't retrieve token for ", username)

    def updateUI(self, track):
        self.songNameLabel.config(text=track['name'])
        self.artistNameLabel.config(text=track['artists'][0]['name'])
        self.collectionNameLabel.config(text=track['album']['name'])

class Message(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.defaultMessage = ''
        self.messageLabel = Label(self, text=self.defaultMessage, font=('Helvetica', medium_text_size), fg="white", bg="black")
        self.messageLabel.pack(side=TOP, anchor=N, padx=10)
        self.getMessage()

    def getMessage(self):
        with setlocale(ui_locale):
            message = ''
            hourOfDay = int(time.strftime('%H'))
            if hourOfDay > 4 and hourOfDay < 11:
                message = 'Good Morning, ' + USER_FIRST_NAME
            elif hourOfDay < 17:
                message = 'Good Afternoon, ' + USER_FIRST_NAME
            else:
                message = 'Good Evening, ' + USER_FIRST_NAME
            self.messageLabel.config(text=message)
            self.after(MESSAGE_REFRESH_RATE, self.getMessage)

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topMostFrame = Frame(self.tk, background = 'black', cursor = 'none')
        self.topFrame = Frame(self.topMostFrame, background = 'black', cursor = 'none')
        self.bottomFrame = Frame(self.tk, background = 'black', cursor = 'none')
        self.topMostFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.topFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.expanded = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("<c>", self.focus_clock)
        self.tk.bind("<h>", self.focus_home)
        self.tk.bind("<w>", self.focus_weather)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=50, pady=30)
        self.largeClock = LargeClock(self.tk)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=50, pady=30)
        self.largeWeather = LargeWeather(self.tk)        
        # message
        self.message = Message(self.topMostFrame)
        self.message.pack(side=TOP, anchor=N, padx=0, pady=30)
        # spotify
        self.spotify = SpotifyDisplay(self.bottomFrame)
        self.spotify.pack(side=RIGHT, anchor=S, padx=50, pady=30)
        self.toggle_fullscreen(None)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def focus_clock(self, event=None):
        if self.expanded is False:
            self.topMostFrame.pack_forget()
            self.topFrame.pack_forget()
            self.bottomFrame.pack_forget()
            self.largeClock.pack(side=TOP, anchor=N, padx=50, pady=50)
            self.expanded = 'Clock'

    def focus_weather(self, event=None):
        if self.expanded is False:
            self.topMostFrame.pack_forget()
            self.topFrame.pack_forget()
            self.bottomFrame.pack_forget()
            self.largeWeather.pack(side=TOP, anchor=N, padx=50, pady=50)
            self.expanded = 'Weather'

    def focus_home(self, event=None):
        if self.expanded is 'Clock':
            self.largeClock.pack_forget()
        elif self.expanded is 'Weather':
            self.largeWeather.pack_forget()
        if self.expanded is not False:
            self.topMostFrame.pack(side = TOP, fill=BOTH, expand = YES)
            self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
            self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
            self.clock.pack(side=RIGHT, anchor=N, padx=50, pady=30)
            self.weather.pack(side=LEFT, anchor=N, padx=50, pady=30)
            self.message.pack(side=TOP, anchor=N, padx=0, pady=30)
            self.spotify.pack(side=RIGHT, anchor=S, padx=50, pady=30)
            self.expanded = False

@skywriter.flick()
def flick(start, finish):
    #print start + " " +finish
    if start is 'south' and finish is 'north':
        os.system("xset -display :0 dpms force on")
        w.focus_home(None)
    if start is 'north' and finish is 'south':
        os.system("xset -display :0 dpms force off") # standby
        w.focus_home(None)
    elif start is 'west' and finish is 'east':
        w.focus_clock(None)
    elif finish is 'west':
        w.focus_weather(None)

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
    
signal.pause()
