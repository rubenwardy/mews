from PIL import Image, ImageDraw, ImageFont
from mews import app
from io import BytesIO
from flask import send_file, request


def get_initials(fullname):
	initials = ""
	for name in fullname.split():
		c = name[0].upper()
		if c.isalpha() or c.isnumeric():
			initials += c
			if len(initials) == 2:
				break

	return initials


@app.route("/dummy/")
def dummy_art():
	title = request.args["title"]
	# if title is None
	initials = get_initials(title)

	fnt = ImageFont.truetype('../fonts/Cantarell-Regular.otf', 70)

	img = Image.new('RGB', (240, 240), color = (73, 109, 137))
	d = ImageDraw.Draw(img)
	d.text((20,10), initials, font=fnt, fill=(255, 255, 255))

	img_io = BytesIO()
	img.save(img_io, 'PNG')
	img_io.seek(0)
	return send_file(img_io, mimetype='image/jpeg')
