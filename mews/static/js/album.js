albums = {}

class Album extends Model {
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

	setTracks(tracks) {
		console.log("Updated tracks for album " + this.id)
		this.tracks = tracks.map(track => Track.get(track.id, track))
		this.is_known = true
		this.notifyChange()
	}

	static get(id) {
		var album = albums[id]
		if (!album) {
			album = new Album(id)
			albums[id] = album
		}

		return album
	}
}
