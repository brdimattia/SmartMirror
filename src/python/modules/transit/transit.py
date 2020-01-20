
from tkinter import Frame, Canvas, SE, SW, NW, CENTER
from src.python.constants.common import BLACK, WHITE, ICON_LOOKUP, FRANK_RUHL_LIBRE_BLACK, MULI
from src.python.modules.transit.transit_constants import GREEN, TITLE_TEXT_SIZE, NEXT_TRAIN_TEXT_SIZE, TRANSIT_API_ENDPOINT
from src.python.constants.user_config import TRANSIT_LINE
from PIL import Image, ImageTk
import traceback
import requests
import json

class Transit(Frame):
    
    def render_ui(self, track):
        pass
        # self.current_track = track['name']
        # self.current_next_train_one = track['next_train_one']['name']
        # self.current_artist = track['artists'][0]['name']

        # self.track_canvas.delete("all")
        # self.track_text = self.track_canvas.create_text(0, -10, text=self.current_track, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        # self.track_bounding_box = self.track_canvas.bbox(self.track_text)
        # self.track_canvas.configure(width=self.track_bounding_box[2], height=self.track_bounding_box[3])
        # self.next_train_one_canvas.delete("all")
        # self.next_train_one_text = self.next_train_one_canvas.create_text(0, -10, text=self.current_next_train_one, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        # self.next_train_one_bounding_box = self.next_train_one_canvas.bbox(self.next_train_one_text)
        # self.next_train_one_canvas.configure(width=self.next_train_one_bounding_box[2], height=self.next_train_one_bounding_box[3])
        # self.artist_canvas.delete("all")
        # self.artist_text = self.artist_canvas.create_text(0, -10, text=self.current_artist, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        # self.artist_bounding_box = self.artist_canvas.bbox(self.artist_text)
        # self.artist_canvas.configure(width=self.artist_bounding_box[2], height=self.artist_bounding_box[3])

    def update_info(self):
        pass
        # try:
        #     transit_req_url = TRANSIT_API_ENDPOINT % (WEATHER_API_TOKEN, self.latitude, self.longitude, WEATHER_LANG, WEATHER_UNIT)
        #     r = requests.get(transit_req_url)
        #     transit_obj = json.loads(r.text)

        # except Exception as e:
        #     traceback.print_exc()
        #     print("Error: %s. Cannot get transit data." % e)

    # def spotifyAuthenticateWithScope(self, scope):
    #     token = spotipy_util.prompt_for_user_token(SPOTIFY_USERNAME, scope)
    #     if token:
    #         self.spotifyConnection = spotipy.Spotify(auth=token, requests_session=True, requests_timeout=SPOTIFY_REQUEST_TIMEOUT)
    #         print("Successfuly retrieved token for spotify user: " + SPOTIFY_USERNAME)
    #         return token
    #     else:
    #         print("Can't retrieve token for ", SPOTIFY_USERNAME)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg=BLACK, height=100)        
        
        self.tranit_line_title = "%s ARRIVES IN:" % TRANSIT_LINE.upper()
        self.next_train_one = "3 minutes"
        self.next_train_two = "5 minutes"

        self.logo_canvas = Canvas(self, bg=BLACK, height=110, width=110, bd=0, highlightthickness=0)
        self.logo_canvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=SE, padx=20)
        self.spotify_logo = Image.open(ICON_LOOKUP["transit"])
        self.spotify_logo = self.spotify_logo.resize((110, 110), Image.ANTIALIAS)
        self.spotify_logo = self.spotify_logo.convert('RGB')
        self.spotify_logo = ImageTk.PhotoImage(self.spotify_logo)
        self.logo_canvas.create_image(0, 0, image=self.spotify_logo, anchor=NW)

        self.tranit_line_title_frame = Frame(self, bg=BLACK, height=30)
        self.tranit_line_title_frame.grid(row=0, column=1, rowspan=1, columnspan=2, sticky=SW)
        self.transit_line_title_canvas = Canvas(self.tranit_line_title_frame, bg=BLACK, height=30, width=412, bd=0, highlightthickness=0)
        self.transit_line_title_canvas.pack()
        self.transit_line_title_text = self.transit_line_title_canvas.create_text(15, -8, text=self.tranit_line_title, fill=WHITE, font=(FRANK_RUHL_LIBRE_BLACK, TITLE_TEXT_SIZE), anchor=NW)  
        self.transit_line_title_bounding_box = self.transit_line_title_canvas.bbox(self.transit_line_title_text)
        self.transit_line_title_underline = self.transit_line_title_canvas.create_rectangle(0, self.transit_line_title_bounding_box[3]-10, self.transit_line_title_bounding_box[2]+15, self.transit_line_title_bounding_box[3], outline=GREEN, fill=GREEN)

        self.next_train_one_canvas = Canvas(self, bg=BLACK, height=50, width=300, bd=0, highlightthickness=0)
        self.next_train_one_text = self.next_train_one_canvas.create_text(0, -5, text=self.next_train_one, fill=WHITE, font=(MULI, NEXT_TRAIN_TEXT_SIZE), anchor=NW, justify=CENTER)  
        self.next_train_one_bounding_box = self.next_train_one_canvas.bbox(self.next_train_one_text)
        self.next_train_one_canvas.configure(width=412, height=self.next_train_one_bounding_box[3]-5)
        left_offset = self.transit_line_title_bounding_box[2]/2 - self.next_train_one_bounding_box[2]/2
        self.next_train_one_canvas.move(self.next_train_one_text, left_offset, 0)
        self.next_train_one_canvas.grid(row=1, column=1, rowspan=1, columnspan=2, sticky=SW)

        self.next_train_two_canvas = Canvas(self, bg=BLACK, height=50, width=300, bd=0, highlightthickness=0)
        self.next_train_two_text = self.next_train_two_canvas.create_text(0, -5, text=self.next_train_two, fill=WHITE, font=(MULI, NEXT_TRAIN_TEXT_SIZE), anchor=NW, justify=CENTER)  
        self.next_train_two_bounding_box = self.next_train_two_canvas.bbox(self.next_train_two_text)
        self.next_train_two_canvas.configure(width=412, height=self.next_train_two_bounding_box[3]-5)
        left_offset = self.transit_line_title_bounding_box[2]/2 - self.next_train_two_bounding_box[2]/2
        self.next_train_two_canvas.move(self.next_train_two_text, left_offset, 0)
        self.next_train_two_canvas.grid(row=2, column=1, rowspan=1, columnspan=2, sticky=SW)

        self.update_info()


    