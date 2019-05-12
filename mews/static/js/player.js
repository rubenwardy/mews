class Player {
	constructor() {
		this.playlist = null
		this.playing_id = null
		this.playing = true
		this.audio = new Audio()
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
		console.log("[Player] Play pressed!")

		var playlist = this.getPlaylist()
		if (!playlist) {
			return
		}

		this.playing = true

		// Nothing playing, start from the beginning
		if (this.playing_id == null) {
			this.playing_id = playlist.getFirstID()
		}

		// TODO: add audio and actually play it
		var playing = this.getTrack()
		if (playing) {
			console.log("[Player] Started: " + playing.title)
			this.audio.play(playing.id, playing.getURL())
		}
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
		this.playing = true
		this.playlist.change(pl => this.onPlaylistChanged(pl))
	}

	onPlaylistChanged(playlist) {
		console.log("[Player] Playlist updated!")

		// Was waiting for playlist to be filled
		if (this.playing && this.playing_id == null) {
			this.play()
		}
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
