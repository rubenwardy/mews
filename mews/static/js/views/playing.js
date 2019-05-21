import { rjs, ViewModel } from "../rjs.js"
import { TracksView } from "./tracks.js"
import { player } from "../main.js"

export class PlayingView extends ViewModel {
	constructor() {
		super()

		rjs.watch("statechanged", this.onStateChange.bind(this))
	}

	onStateChange() {
		console.log("[Playing] State changed!")

		this.onChange(player.getTrack())
	}

	onChange(track) {
		if (!track) {
			document.getElementById("player").style.display = "none"
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

		this.tracks_view = new TracksView(this.element.querySelector(".panel-scrolling"), "panel-block", true)

		this.element.querySelector(".panel-heading").addEventListener("click", () => {
			if (this.element.classList.contains("panel-collapsed")) {
				this.element.classList.remove("panel-collapsed")
			} else {
				this.element.classList.add("panel-collapsed")
			}
		})
	}

	onChange(playlist) {
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
