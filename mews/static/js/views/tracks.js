import { rjs, ViewModel } from "../rjs.js"
import { player } from "../main.js"
import { Track } from "../models/track.js"

export class TracksView extends ViewModel {
	constructor(element, classes, show_art) {
		super(element)

		this.classes = classes || ""
		this.show_art = show_art

		rjs.watch("statechanged", this.onStateChange.bind(this))

		this.element.addEventListener("click", e => {
			if (!e.target) {
				return;
			}

			console.log("A")

			const track_ele = rjs.getParentElementByClass(e.target, "track", this.element)
			if (!track_ele) {
				return
			}

			console.log("B")

			let track = Track.get(track_ele.getAttribute("data-id"))
			if (!track) {
				return
			}

			console.log("C")

			if (rjs.getParentElementByClass(e.target, "action-add", this.element)) {
				player.addTrack(track.id)
				event.stopPropagation()
			} else if (rjs.getParentElementByClass(e.target, "action-next", this.element)) {
				player.addTrackNext(track.id)
				event.stopPropagation()
			} else if (rjs.getParentElementByClass(e.target, "track", this.element)) {
				player.playTrack(track.id)
				event.stopPropagation()
			}
		})
	}

	onChange(container) {
		this.element.innerHTML = ""

		if (container && container.isKnown()) {
			const playingTrack = player && player.getTrack()
			for (let track of container.getTracks()) {
				const isPlaying = playingTrack && playingTrack.id == track.id
				this.element.appendChild(this.buildRow(track, isPlaying))
			}
		} else if (container) {
			let loading = document.createElement("span")
			loading.setAttribute("class", "button is-dark is-loading")
			loading.textContent = "Loading"
			loading.setAttribute("style", "margin:auto;")
			this.element.appendChild(loading)
		}
	}

	buildRow(track, isPlaying) {
		let row = document.createElement("a")
		row.setAttribute("class", this.classes + (isPlaying ? " track is-active" : " track"))
		row.setAttribute("data-id", track.id)

		let icon = this.show_art ? `<img class="panel-icon album-icon" src="${track.picture}"></img>` : ""
		row.innerHTML = `
			<div class="actions">
				<a class="action-add"><span class="fa fa-plus"></span></a>
				<a class="action-next"><span class="fa fa-plus-square"></span></a>
			</div>
			${icon}${track.title}`
		return row
	}

	onStateChange() {
		this.invalidate()
	}
}
