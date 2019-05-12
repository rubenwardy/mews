from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("../config.cfg")

from pylast import LastFMNetwork
lastfm = LastFMNetwork(api_key=app.config["LASTFM_API_KEY"], api_secret=app.config["LASTFM_API_SECRET"])

from . import views, models
