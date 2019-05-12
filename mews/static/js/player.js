class Player {
	constructor() {
		this.playlist = null
		this.playing_id = null
	}

	// Stops and deletes current playing item
	stop() {

	}

	// Plays the playlist
	//
	// If the playlist is unknown, then it will delay playing
	// If the cursor is at the end, then it will start from the begining
	// Nothing happens on no playlist
	play() {
		var playlist = this.getPlaylist()
	}

	getTrack() {
		if (this.playing_id == null) {
			return null
		}

		var playlist = this.getPlaylist()
		if (!playlist) {
			return null
		}

		return playlist.get(this.playing_id)
	}

	getNextTrack() {
		if (this.playing_id == null) {
			return null
		}

		var playlist = this.getPlaylist()
		if (!playlist) {
			return null
		}

		return playlist.getAfter(this.playing_id)
	}

	getPlaylist() {
		return this.playlist
	}

	setPlaylist(playlist) {
		this.stop()
		this.playlist = playlist
		this.playlist.change(pl => this.onPlaylistChanged)
	}

	onPlaylistChanged(playlist) {

	}

	async playAlbum(id) {
		var playlist = this.getPlaylist()
		if (playlist) {
			playlist.addAlbum(id)
		} else {
			playlist = new Playlist()
			playlist.create().then(_ => playlist.addAlbum(id))
			this.setPlaylist(playlist)
		}
	}
}

player = new Player()
