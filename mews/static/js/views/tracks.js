import { ViewModel } from "../rjs.js"

export class TracksView extends ViewModel {
	constructor(element, classes) {
		super(element)

		this.classes = classes || ""
	}

	onChange(container) {
		this.element.innerHTML = ""

		if (container && container.isKnown()) {
			for (var track of container.getTracks()) {
				var row = document.createElement("a")
				row.setAttribute("class", this.classes)
				row.text = track.title
				this.element.appendChild(row)
			}
		} else if (container) {
			var loading = document.createElement("span")
			loading.setAttribute("class", "button is-dark is-loading")
			loading.textContent = "Loading"
			loading.setAttribute("style", "margin:auto;")
			this.element.appendChild(loading)
		}
	}
}
