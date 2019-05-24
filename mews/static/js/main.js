import { showAlbums } from "./views/album.js"
import { Player } from "./controllers/player.js"
import { PlayingView } from "./views/playing.js"
import { rjs } from "./rjs.js";

export let player = null
export let playing = null

class DummyPlayer {
	constructor() {
		document.getElementById("plpanel").style.display = "none"
	}

	getTrack() { return null }

	async addAlbum(_) {
		window.location.href = "/user/sign-in"
	}

	async playAlbum(_) {
		window.location.href = "/user/sign-in"
	}
}

rjs.onLoad(() => {
	showAlbums().catch(console.log)
	if (current_user) {
		player = new Player()
		playing = new PlayingView(document.getElementById("plpanel"))
	} else {
		player = new DummyPlayer()
	}

	document.querySelectorAll(".modal-close").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))

	document.querySelectorAll(".modal .delete").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))

	document.querySelectorAll(".modal-background").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))
})
