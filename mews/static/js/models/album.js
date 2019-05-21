import { Model } from "../rjs.js"
import { api } from "../api.js"
import { Track } from "../models/track.js"

let albums = {}

export class Album extends Model {
	constructor(id) {
		super(id)
		this.title  = ""
		this.artist = null
		this.tracks = []
	}

	toString() {
		return this.title || "?"
	}

	fromDict(dict) {
		this.title    = dict.title
		this.artist   = dict.artist
		this.picture  = dict.picture
		this.notifyChange()
	}

	async syncTracks() {
		this.setTracks(await api.getAlbumTracks(this.id))
	}

	getTracks() {
		return this.tracks
	}

	setTracks(tracks) {
		console.log("Updated tracks for album " + this.id)
		this.tracks = tracks.map(track => Track.get(track.id, track))
		this.is_known = true
		this.notifyChange()
	}

	static get(id) {
		return albums[id]
	}

	static getOrCreate(id) {
		var album = this.get(id)
		if (!album) {
			album = new Album(id)
			albums[id] = album
		}

		return album
	}
}
