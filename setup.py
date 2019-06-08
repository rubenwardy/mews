from app.models import *
from flask_user import *

db.create_all()


def make_flask_user_password(plaintext_str):
	import bcrypt
	plaintext = plaintext_str.encode("UTF-8")
	password = bcrypt.hashpw(plaintext, bcrypt.gensalt())
	if isinstance(password, str):
		return password
	else:
		return password.decode("UTF-8")

def add_mixed_album(title):
	rep = Replacement()
	rep.album_title = title
	rep.set_artist = "Various Artists"
	assert(rep.isValid())
	db.session.add(rep)


ruben = User()
ruben.username = "rubenwardy"
ruben.password = make_flask_user_password("password")
ruben.is_admin = True
db.session.add(ruben)

add_mixed_album("Ashes to Ashes (Original Soundtrack)")
add_mixed_album("Teenage Dirtbags")
add_mixed_album("Mixtape")
add_mixed_album("Radio 1's Live Lounge")

rep = Replacement()
rep.artist_name = "Various"
rep.set_artist = "Various Artists"
assert(rep.isValid())
db.session.add(rep)

rep = Replacement()
rep.album_title = "Crossroad - The Best of Bon Jovi"
rep.set_album = "Crossroad"
assert(rep.isValid())
db.session.add(rep)

rep = Replacement()
rep.album_title = "The Very Best Of T.Rex"
rep.set_album = "The Very Best of T-Rex"
assert(rep.isValid())
db.session.add(rep)

db.session.commit()
