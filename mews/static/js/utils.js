class Model {
	constructor(id) {
		this.id = id
		this.is_known = false
		this.watchers = []
		console.log("Created " + this.constructor["name"] + "[" + this.id + "]: " + this)
	}

	isKnown() {
		return this.is_known
	}

	toString() {
		return "?"
	}

	change(func) {
		if (func) {
			this.watchers.push(func)
		} else {
			console.log("Changed " + this.constructor["name"] + "[" + this.id + "]: " + this)
			for (func of this.watchers) {
				func(this)
			}
		}
	}
}

class Audio {
	getElement() {
		return document.getElementById('audio_player');
	}

	load(id, url) {
		console.log("[Audio] Loading " + url)
		var element = document.createElement("source")
		element.setAttribute("src", url)
		this.getElement().appendChild(element)
		this.getElement().load()
	}

	isLoaded(id) {
		return document.querySelectorAll("source[data-id='" + id + "']").length > 0
	}

	play(id, url) {
		console.log("[Audio] Playing " + url)
		if (!this.isLoaded(id)) {
			this.load(id, url)
		}

		this.getElement().play()
	}
}
