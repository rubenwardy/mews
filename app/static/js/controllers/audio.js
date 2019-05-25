export class Audio {
	constructor() {
		this.onEnds = []
	}

	getRoot() {
		return document.getElementById('audioplayer')
	}

	load(id, url) {
		console.log("[Audio] Loading " + url)
		let element = document.createElement("audio")
		element.setAttribute("src", url)
		element.setAttribute("controls", "controls")
		element.setAttribute("data-id", id)
		this.getRoot().appendChild(element)
		element.load()

		element.addEventListener("ended", this.runCB.bind(this, this.onEnds, element), false)
	}

	runCB(cb, element) {
		for (let func of cb) {
			func(this, element.getAttribute("data-id"))
		}
	}

	onEnd(func) {
		this.onEnds.push(func)
	}

	unload(id) {
		document.querySelectorAll("audio[data-id='" + id + "']").forEach(x => x.remove())
	}

	unloadAll() {
		document.querySelectorAll("audio").forEach(x => x.remove())
	}

	unloadBut(id) {
		document.querySelectorAll("audio:not([data-id='" + id + "'])").forEach(x => x.remove())
	}

	isLoaded(id) {
		return document.querySelectorAll("audio[data-id='" + id + "']").length > 0
	}

	pauseAll() {
		console.log("[Audio] Stopping all")
		document.querySelectorAll("audio").forEach(x => x.pause())
	}

	play(id, url) {
		console.log("[Audio] Playing " + url)
		if (!this.isLoaded(id)) {
			this.load(id, url)
		}

		this.pauseAll()
		this.unloadBut(id)
		document.querySelectorAll("audio[data-id='" + id + "']").forEach(x => x.play())
	}
}
