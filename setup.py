from mews.models import *
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

ruben = User()
ruben.username = "rubenwardy"
ruben.password = make_flask_user_password("password")
db.session.add(ruben)
db.session.commit()
