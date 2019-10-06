import { rjs, ViewModel } from "../rjs.js"
import { TracksView } from "./tracks.js"
import { player, playing } from "../main.js"
import { api } from "../api.js";

export class PlayingView extends ViewModel {
	constructor(element) {
		super(element)

		rjs.watch("statechanged", this.onStateChange.bind(this))
	}

	onStateChange() {
		console.log("[Playing] State changed!")

		this.onChange(player.getTrack())
	}

	onChange(track) {
		if (!this.element) {
			return
		}
		if (!track) {
			this.element.style.display = "none"
			return
		}

		document.getElementById("player").style.display = "block"
		document.getElementById("player-art").setAttribute("src", track.picture)
		document.getElementById("player-track").text  = track.title
		document.getElementById("player-artist").text = track.artist
	}
}

export class PlaylistView extends ViewModel {
	constructor(element) {
		super(element)

		this.tracks_view = new TracksView(this.element.querySelector(".panel-scrolling"), "panel-block",
				true, { type: "playlist", album: null })

		this.element.querySelector(".panel-heading").addEventListener("click", e => {
			if (!rjs.getParentElementByClass(e.target, "actions", this.element)) {
				this.element.classList.toggle("panel-collapsed")
			}
		})

		this.element.querySelector(".clear-upcoming").addEventListener("click", () => {
			var playlist = this.getTarget()

			const playingID = player && player.getPlayingID()
			var playingPlaylist = player.getPlaylist()
			if (playingPlaylist == playlist && playingID) {
				playlist.clearTracksAfter(playingID)
			}
		})
	}

	onChange(playlist) {
		if (this.tracks_view) {
			this.tracks_view.setSource({ type: "playlist", album: playlist })
		}

		if (!playlist) {
			this.element.style.display = "none"
			return
		}

		this.element.querySelector(".count").textContent = playlist.getNumTracks()
		this.element.querySelector(".title").textContent = playlist.title
		this.element.style.display = "block"
		this.element.querySelectorAll(".panel-scrolling a")
			.forEach(e => e.remove())
	}

	setTarget(target) {
		super.setTarget(target)
		if (this.tracks_view) {
			this.tracks_view.setTarget(target)
		}
	}
}
