class AlbumTracksView extends ViewModel {
	constructor(element) {
		super(element)
	}

	onChange(album) {
		if (!album) {
			this.element.classList.remove("is-active")
			return
		}

		this.element.classList.add("is-active")
		this.element.querySelector(".modal-card-title").textContent = album.title + " by " + album.artist
		this.element.querySelector("section").innerHTML = ""

		var section = this.element.querySelector("section")
		if (album.isKnown()) {
			for (var track of album.tracks) {
				var row = document.createElement("a")
				row.setAttribute("class", "column is-half")
				row.text = track.title
				section.appendChild(row)
			}
		} else {
			var loading = document.createElement("span")
			loading.setAttribute("class", "button is-dark is-loading")
			loading.textContent = "Loading"
			loading.setAttribute("style", "margin:auto;")
			section.appendChild(loading)
		}
	}
}

var alview = new AlbumTracksView(document.getElementById("albummodal"))

function appendAlbum(album) {
	let element = document.createElement("div")
	let picture = album.picture || "/dummy/?title=" + encodeURI(album.title)
	element.innerHTML = `<img src="${picture}" class="is-1by1">
		<div class="actions">
			<a class="action-play"><span class="fa fa-play"></span></a>
			<a class="action-add"><span class="fa fa-plus"></span></a>
		</div>
		<h3 class="title is-5 is-marginless">${album.title}</h3>
		<a class="subtitle is-6">${album.artist}</a>`;
	element.setAttribute("class", "column is-one-fifth is-1by1 album")
	element.setAttribute("data-id", album.id)
	document.querySelector("#albums").appendChild(element)
	element.querySelector(".action-play").addEventListener("click", function(event) {
		player.playAlbum(album.id)
		event.stopPropagation()
	})
	element.querySelector(".action-add").addEventListener("click", function(event) {
		player.addAlbum(album.id)
		event.stopPropagation()
	})
	element.addEventListener("click", function(event) {
		alview.setTarget(album)
		if (!album.isKnown()) {
			album.syncTracks()
		}
		event.stopPropagation()
	})
}

async function showAlbums() {
	let albums = await api.getAlbums()
	for (let dict of albums) {
		var album = Album.get(dict.id)
		album.fromDict(dict)
		appendAlbum(album)
	}
}
