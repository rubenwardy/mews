from PIL import Image, ImageDraw, ImageFont
from mews import app
from io import BytesIO
from flask import send_file, request
import random, os

def get_initials(fullname):
	initials = ""
	for name in fullname.split():
		c = name[0].upper()
		if c.isalpha() or c.isnumeric():
			initials += c
			if len(initials) == 2:
				break

	return initials


COLORS = [
	"#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
	"#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
	"#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
	"#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"]


@app.route("/dummy/")
def dummy_art():
	title = request.args["title"]
	# if title is None
	initials = get_initials(title)

	dir_path = os.path.dirname(os.path.realpath(__file__))
	fnt = ImageFont.truetype(os.path.join(dir_path, "../fonts/Cantarell-Regular.otf"), 70)

	color = random.choice(COLORS).lstrip("#")
	color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

	textcolor = (255,255,255)
	luminance = (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2])/255
	if luminance > 0.5:
		textcolor = (0,0,0)


	img = Image.new("RGB", (240, 240), color=color)
	d = ImageDraw.Draw(img)
	d.text((20,10), initials, font=fnt, fill=textcolor)

	img_io = BytesIO()
	img.save(img_io, "PNG")
	img_io.seek(0)
	return send_file(img_io, mimetype="image/jpeg")
