import { rjs } from "../rjs.js"
import { Audio } from "./audio.js"
import { PlaylistView } from "../views/playing.js"
import { Playlist } from "../models/playlist.js"

export class Player {
	constructor() {
		this.playlist = null
		this.playing_id = null
		this.playing = true
		this.audio = new Audio()
		this.plview = new PlaylistView(document.getElementById("plpanel"))
		this.audio.onEnd(this.onMusicEnd.bind(this))
	}

	// Stops and deletes current playing item
	stop() {
		this.playing = false
		this.playing_id = null
		console.log("[Player] Stop!")
		this.audio.unloadAll()
		this.updateUI()
	}

	// Plays the playlist
	//
	// If the playlist is unknown, then it will delay playing
	// If the cursor is at the end, then it will start from the begining
	// Otherwise, it will play the cursor'd song from the beginning
	// Nothing happens on no playlist
	play() {
		console.log("[Player] Play!")

		let playlist = this.getPlaylist()
		if (!playlist) {
			this.updateUI()
			return
		}

		this.playing = true

		// Nothing playing, start from the beginning
		if (this.playing_id == null) {
			this.playing_id = playlist.getFirstID()
		}

		// TODO: add audio and actually play it
		let playing = this.getTrack()
		if (playing) {
			console.log("[Player] Started: " + playing.title)
			this.audio.play(playing.id, playing.getURL())
		}

		this.updateUI()
	}

	next() {
		console.log("[Player] Next!")

		if (this.playing_id == null) {
			this.updateUI()
			return null
		}

		let playlist = this.getPlaylist()
		if (!playlist) {
			this.updateUI()
			return null
		}

		this.playing_id = playlist.getNextID(this.playing_id)
		if (this.playing_id) {
			this.play()
		} else {
			this.stop()
		}
	}

	getTrack() {
		if (this.playing_id == null) {
			return null
		}

		let playlist = this.getPlaylist()
		if (!playlist) {
			return null
		}

		return playlist.get(this.playing_id)
	}

	getNextTrack() {
		if (this.playing_id == null) {
			return null
		}

		let playlist = this.getPlaylist()
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
		this.playlist.watch(this.onPlaylistChanged.bind(this))
		this.plview.setTarget(this.playlist)
	}

	onPlaylistChanged(playlist) {
		console.log("[Player] Playlist updated!")

		// Was waiting for playlist to be filled
		if (this.playing && this.playing_id == null) {
			this.play()
		}
	}

	onMusicEnd(audio, id) {
		this.next()
	}

	updateUI() {
		rjs.notify("statechanged")
	}

	async getOrCreatePlaylist() {
		let playlist = this.getPlaylist()
		if (!playlist) {
			playlist = new Playlist()
			this.setPlaylist(playlist)
			await playlist.create()
		}

		return playlist
	}

	async addAlbum(id) {
		let playlist = await this.getOrCreatePlaylist()
		await playlist.addAlbum(id)
	}

	async playAlbum(id) {
		this.stop()
		this.playing = true

		let playlist = this.getPlaylist()
		if (playlist) {
			await playlist.playAlbum(id)
		} else {
			playlist = new Playlist()
			this.setPlaylist(playlist)

			await playlist.create()
			await playlist.addAlbum(id)
		}
	}

	async addTrack(id) {
		let playlist = await this.getOrCreatePlaylist()
		await playlist.addTrack(id)
	}

	async playTrack(id) {
		this.audio.pauseAll()
		let playlist = await this.getOrCreatePlaylist()

		let pt = playlist.getID(id)
		if (!pt) {
			await playlist.addTrack(id)
			pt = playlist.getID(id)
			console.assert(pt, "Track never added")
		}

		this.playing_id = pt
		this.play()
	}
}
