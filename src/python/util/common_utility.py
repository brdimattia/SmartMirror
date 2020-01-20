
import locale
import threading
import traceback
import requests
import json
from contextlib import contextmanager
from src.python.constants.user_config import GEO_IP_TOKEN

LOCALE_LOCK = threading.Lock()

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

def convert_fahrenheit_to_celcius(fahrenheit_temp):
    return int((fahrenheit_temp - 32) * 5.0/9.0)

def convert_fahrenheit_to_kelvin(fahrenheit_temp):
    return convert_fahrenheit_to_celcius(fahrenheit_temp) + 273

def get_ip():
    try:
        ip_url = "http://api.ipify.org?format=json"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
    except Exception as e:
        traceback.print_exc()
        print("Error: %s. Cannot get ip." % e)
        return ''

def get_location(ip):
    try:
        location_req_url = "http://api.ipstack.com/%s?access_key=%s" % (ip, GEO_IP_TOKEN)
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)
        lat = location_obj['latitude']
        lon = location_obj['longitude']
        city_region = "%s, %s" % (location_obj['city'], location_obj['region_code'])
        return lon, lat, city_region
    except Exception as e:
        traceback.print_exc()
        print("Error: %s. Cannot get location." % e)
        return '', '', ''