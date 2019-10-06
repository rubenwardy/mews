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
		let playlist = await api.createPlaylist(this.title)
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
			return { "track": Track.getOrCreate(track.id, track), "id": track.pt_id }
		})
		this.notifyChange()
	}

	get(pt_id) {
		if (pt_id == null) {
			return null
		}

		for (let pt of this.playlist_tracks) {
			if (pt.id == pt_id) {
				return pt.track
			}
		}

		return null
	}

	getID(id) {
		if (id == null) {
			return null
		}

		for (let pt of this.playlist_tracks) {
			if (pt.track.id == id) {
				return pt.id
			}
		}

		return null
	}

	getNext(pt_id) {
		let isNext = false
		for (let i = 0; i < this.playlist_tracks.length; i++) {
			if (isNext) {
				return this.playlist_tracks[i].track
			} else if (this.playlist_tracks[i].id == pt_id) {
				isNext = true
			}
		}

		return null
	}

	getNextID(pt_id) {
		let isNext = false
		for (let i = 0; i < this.playlist_tracks.length; i++) {
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

	async addTrack(id) {
		this.setTracks(await api.updatePlaylistTracks(this.id, { tracks: [id] }))
	}

	async addTrackAfter(id, pt_id) {
		this.setTracks(await api.updatePlaylistTracks(this.id, { after: pt_id, tracks: [id] }))
	}

	async clearTracksAfter(pt_id) {
		this.setTracks(await api.updatePlaylistTracks(this.id, { clear_after: pt_id }))
	}
}
