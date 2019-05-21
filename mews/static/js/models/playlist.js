import { Model } from "../rjs.js"
import { api } from "../api.js"
import { Track } from "../models/track.js"

export class Playlist extends Model {
	constructor() {
		super(null)

		this.title = null
		this.playlist_tracks = []
	}

	toString() {
		return this.title || "?"
	}

	async create() {
		var playlist = await api.createPlaylist(this.title)
		this.id    = playlist.id
		this.title = playlist.title
		this.is_known = true
		this.notifyChange()
		return this
	}

	async syncTracks() {
		this.setTracks(await api.getPlaylistTracks(this.id))
	}

	setTracks(tracks) {
		console.log("Updated tracks for Playlist " + this.id)
		this.playlist_tracks = tracks.map(track => {
			return { "track": Track.get(track.id, track), "id": track.pt_id }
		})
		this.notifyChange()
	}

	get(pt_id) {
		if (pt_id == null) {
			return null
		}

		for (var pt of this.playlist_tracks) {
			if (pt.id == pt_id) {
				return pt.track
			}
		}

		return null
	}

	getNext(pt_id) {
		var isNext = false
		for (var i = 0; i < this.playlist_tracks.length; i++) {
			if (isNext) {
				return this.playlist_tracks[i].track
			} else if (this.playlist_tracks[i].id == pt_id) {
				isNext = true
			}
		}

		return null
	}

	getNextID(pt_id) {
		var isNext = false
		for (var i = 0; i < this.playlist_tracks.length; i++) {
			if (isNext) {
				return this.playlist_tracks[i].id
			} else if (this.playlist_tracks[i].id == pt_id) {
				isNext = true
			}
		}

		return null
	}

	getFirstID() {
		if (this.playlist_tracks.length > 0) {
			return this.playlist_tracks[0].id
		}
	}

	getTracks() {
		return this.playlist_tracks.map(x => x.track)
	}

	getNumTracks() {
		return this.playlist_tracks.length
	}

	async addAlbum(id) {
		this.setTracks(await api.updatePlaylistTracks(this.id, { albums: [id] }))
	}

	async playAlbum(id) {
		this.setTracks(await api.updatePlaylistTracks(this.id, { clear: true, albums: [id] }))
	}
}
