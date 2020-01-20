
from tkinter import Frame, Canvas, SE, SW, NW
from src.python.constants.common import BLACK, WHITE, ICON_LOOKUP, MULI_BOLD
from src.python.modules.spotify.spotify_constants import DETAIL_TEXT_SIZE, SPOTIFY_REFRESH_RATE, SPOTIFY_REQUEST_TIMEOUT
from src.python.constants.user_config import SPOTIFY_MARKET, SPOTIFY_USERNAME
from PIL import Image, ImageTk
import spotipy
import spotipy.util as spotipy_util


class Spotify(Frame):
    
    def render_ui(self, track):
        self.current_track = track['name']
        self.current_album = track['album']['name']
        self.current_artist = track['artists'][0]['name']

        self.track_canvas.delete("all")
        self.track_text = self.track_canvas.create_text(0, -10, text=self.current_track, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.track_bounding_box = self.track_canvas.bbox(self.track_text)
        self.track_canvas.configure(width=self.track_bounding_box[2], height=self.track_bounding_box[3])
        self.album_canvas.delete("all")
        self.album_text = self.album_canvas.create_text(0, -10, text=self.current_album, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.album_bounding_box = self.album_canvas.bbox(self.album_text)
        self.album_canvas.configure(width=self.album_bounding_box[2], height=self.album_bounding_box[3])
        self.artist_canvas.delete("all")
        self.artist_text = self.artist_canvas.create_text(0, -10, text=self.current_artist, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.artist_bounding_box = self.artist_canvas.bbox(self.artist_text)
        self.artist_canvas.configure(width=self.artist_bounding_box[2], height=self.artist_bounding_box[3])

    def update_info(self):
        try:
            if self.spotifyConnection is None:
                self.spotifyToken = self.spotifyAuthenticateWithScope('user-read-currently-playing user-read-recently-played')
            if self.spotifyToken:
                trackResults = self.spotifyConnection.currently_playing(market=SPOTIFY_MARKET)
                if trackResults: #User is currently listening to a song
                    track = trackResults['item']
                    self.render_ui(track)
                else: #User is not currently listening to a song
                    trackResults = self.spotifyConnection.current_user_recently_played(limit=1)
                    track = trackResults['items'][0]['track']
                    self.render_ui(track)
            else:
                self.spotifyConnection = None
        except Exception as e:
            print(e)
            self.spotifyConnection = None
        self.after(SPOTIFY_REFRESH_RATE, self.update_info)

    def spotifyAuthenticateWithScope(self, scope):
        token = spotipy_util.prompt_for_user_token(SPOTIFY_USERNAME, scope)
        if token:
            self.spotifyConnection = spotipy.Spotify(auth=token, requests_session=True, requests_timeout=SPOTIFY_REQUEST_TIMEOUT)
            print("Successfuly retrieved token for spotify user: " + SPOTIFY_USERNAME)
            return token
        else:
            print("Can't retrieve token for ", SPOTIFY_USERNAME)

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg=BLACK)        
        
        self.current_track = None
        self.current_album = None
        self.current_artist = None

        self.logo_canvas = Canvas(self, bg=BLACK, height=150, width=150, bd=0, highlightthickness=0)
        self.logo_canvas.grid(row=0, column=0, rowspan=3, columnspan=1, sticky=SE, padx=20)
        self.spotify_logo = Image.open(ICON_LOOKUP["spotify"])
        self.spotify_logo = self.spotify_logo.resize((150, 150), Image.ANTIALIAS)
        self.spotify_logo = self.spotify_logo.convert('RGB')
        self.spotify_logo = ImageTk.PhotoImage(self.spotify_logo)
        self.logo_canvas.create_image(0, 0, image=self.spotify_logo, anchor=NW)

        self.track_canvas = Canvas(self, bg=BLACK, height=50, width=500, bd=0, highlightthickness=0)
        self.track_canvas.grid(row=0, column=1, rowspan=1, columnspan=2, sticky=SW)
        self.track_text = self.track_canvas.create_text(0, -10, text=self.current_track, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.track_bounding_box = self.track_canvas.bbox(self.track_text)
        self.track_canvas.configure(width=self.track_bounding_box[2], height=self.track_bounding_box[3])

        self.album_canvas = Canvas(self, bg=BLACK, height=50, width=300, bd=0, highlightthickness=0)
        self.album_canvas.grid(row=1, column=1, rowspan=1, columnspan=2, sticky=SW)
        self.album_text = self.album_canvas.create_text(0, -10, text=self.current_album, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.album_bounding_box = self.album_canvas.bbox(self.album_text)
        self.album_canvas.configure(width=self.album_bounding_box[2], height=self.album_bounding_box[3])

        self.artist_canvas = Canvas(self, bg=BLACK, height=50, width=300, bd=0, highlightthickness=0)
        self.artist_canvas.grid(row=2, column=1, rowspan=1, columnspan=2, sticky=SW)
        self.artist_text = self.artist_canvas.create_text(0, -10, text=self.current_artist, fill=WHITE, font=(MULI_BOLD, DETAIL_TEXT_SIZE), anchor=NW)  
        self.artist_bounding_box = self.artist_canvas.bbox(self.artist_text)
        self.artist_canvas.configure(width=self.artist_bounding_box[2], height=self.artist_bounding_box[3])

        self.update_info()


    