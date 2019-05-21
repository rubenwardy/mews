import { Model } from "../rjs.js"
import { api } from "../api.js"

let tracks = {}

export class Track extends Model {
	constructor(id) {
		super(id)
		this.title = "";
		this.artist = 0;
	}

	toString() {
		return this.title || "?"
	}

	async getInfo() {
		this.fromDict(await api.getTrack(this.id))
	}

	fromDict(dict) {
		this.title    = dict.title
		this.artist   = dict.artist
		this.picture  = dict.picture
		this.is_known = true
		this.notifyChange()
	}

	getURL() {
		return "/tracks/" + this.id + "/";
	}

	static get(id, dict) {
		var track = tracks[id]
		if (!track) {
			track = new Track(id)
			tracks[id] = track
			if (dict) {
				track.fromDict(dict)
			} else {
				track.getInfo()
			}
		}

		return track
	}
}
