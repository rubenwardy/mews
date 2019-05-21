import { rjs, ViewModel } from "../rjs.js"
import { player } from "../main.js"

export class TracksView extends ViewModel {
	constructor(element, classes, show_art) {
		super(element)

		this.classes = classes || ""
		this.show_art = show_art

		rjs.watch("statechanged", this.onStateChange.bind(this))
	}

	onChange(container) {
		this.element.innerHTML = ""

		if (container && container.isKnown()) {
			const playingTrack = player && player.getTrack()
			for (var track of container.getTracks()) {
				const isPlaying = playingTrack && playingTrack.id == track.id
				this.element.appendChild(this.buildRow(track, isPlaying))
			}
		} else if (container) {
			var loading = document.createElement("span")
			loading.setAttribute("class", "button is-dark is-loading")
			loading.textContent = "Loading"
			loading.setAttribute("style", "margin:auto;")
			this.element.appendChild(loading)
		}
	}

	buildRow(track, isPlaying) {
		var row = document.createElement("a")
		row.setAttribute("class", this.classes + (isPlaying ? " is-active" : ""))
		if (this.show_art) {
			row.innerHTML = `<img class="panel-icon album-icon" src="${track.picture}">${track.title}`
		} else {
			row.text = track.title
		}

		return row
	}

	onStateChange() {
		this.invalidate()
	}
}
