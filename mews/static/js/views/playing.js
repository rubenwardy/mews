class PlayingView extends ViewModel {
	constructor() {
		super()
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

class PlaylistView extends ViewModel {
	constructor(element) {
		super(element)

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

		var tracks = playlist.getTracks()
		this.element.querySelector(".count").textContent = tracks.length
		this.element.querySelector(".title").textContent = playlist.title
		this.element.style.display = "block"
		this.element.querySelectorAll(".panel-scrolling a")
			.forEach(e => e.parentNode.removeChild(e))

		for (var track of tracks) {
			var ele_a = document.createElement("a")
			ele_a.setAttribute("class", "panel-block is-active")
			ele_a.innerHTML = `<img class="panel-icon" src="${track.picture}">${track.title}`
			this.element.querySelector(".panel-scrolling").appendChild(ele_a)
		}
	}

	onEvent(e) {

	}
}
