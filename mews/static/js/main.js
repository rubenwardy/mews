import { showAlbums } from "./views/album.js"
import { Player } from "./controllers/player.js"
import { PlayingView } from "./views/playing.js"

export let player = null
export let playing = null

window.onload = function() {
	showAlbums().catch(console.log)
	player = new Player()
	playing = new PlayingView()

	document.querySelectorAll(".modal-close").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))

	document.querySelectorAll(".modal .delete").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))

	document.querySelectorAll(".modal-background").forEach(modal => modal.addEventListener("click", function() {
		document.querySelectorAll(".modal").forEach(ele => ele.classList.remove("is-active"))
	}))

	setTimeout(() => {
		document.querySelectorAll(".notifications").forEach(x => x.remove())
	}, 5000)
}

document.addEventListener("DOMContentLoaded", () => {
	(document.querySelectorAll(".notification .delete") || []).forEach((del) => {
		notif = del.parentNode
		del.addEventListener("click", () => {
			notif.remove()
		})
	})
})
