// @author rubenwardy
//
// Class for representing a playlist

class Playlist extends Model {
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
		this.change()
		return this
	}

	async syncTracks() {
		this.setTracks(await api.getPlaylistTracks(this.id))
	}

	setTracks(tracks) {
		console.log("Updated tracks for Playlist " + this.id)
		this.playlist_tracks = tracks.map(track => {
			var ret = Track.get(track.id)
			if (!ret.isKnown()) {
				ret.fromDict(track)
			}
			return { "track": ret, "id": track.pt_id }
		})
		this.change()
	}

	get(pt_id) {
		for (pt of this.playlist_tracks) {
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

	async addAlbum(id) {
		this.setTracks(await api.addAlbumToPlaylist(this.id, id))
	}
}
