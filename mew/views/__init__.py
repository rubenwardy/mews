from flask import render_template
from mew import app

@app.route("/")
def hello():
    return render_template("home.html")

from . import sass, api
