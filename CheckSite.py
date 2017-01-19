"""
Simple script that checks if the HTML of a site has changed and if it has
sends a notification via pushbullet with the URL. 
"""
import urllib.request, urllib.error, urllib.parse
from pushbullet import Pushbullet

API_KEY = ""
SITE = ""

response = urllib.request.urlopen(SITE)
html = response.read()

with open('.lastreadsite', 'r+') as f:
  read_data = f.read()
  if str(html) != str(read_data):
    pb = Pushbullet(API_KEY)
    push = pb.push_link("Site changed", SITE)
    f.truncate()
    f.write(str(html))
