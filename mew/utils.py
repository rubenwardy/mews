import os
from tinytag import TinyTag
import json


ALLOWED_EXT = [".mp3", ".m4a", ".wav", ".ogg"]
def getMusicInfo(path):
	_, ext = os.path.splitext(path.lower())
	if ext in ALLOWED_EXT:
		return { "path": path, "meta": TinyTag.get(path) }
	else:
		return None


def scanForMusic(root):
	ret = []
	for dir, _, files in os.walk(root):
		for file in files:
			path = os.path.join(dir, file)
			info = getMusicInfo(path)
			if info is not None:
				ret.append(info)

	return ret
