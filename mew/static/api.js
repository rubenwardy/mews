// @author rubenwardy

async function getJSON(url, method) {
	let response = await fetch(new Request(url, {
		method: method || "get",
		credentials: "same-origin",
		headers: {
			"Accept": "application/json",
		},
	}))

	let text = await response.text()
	return JSON.parse(text)
}

function appendAlbum(album) {
	let element = document.createElement("div")
	element.innerHTML = `<img src="https://i.redd.it/337x5bx7x7j11.jpg" class="is-1by1">
		<h3 class="title is-5 is-marginless">Simulation Theory</h3>
		<a class="subtitle is-6">Muse</a>`;
	element.setAttribute("class", "column is-one-fifth is-1by1")
	element.setAttribute("data-id", album.id)

	document.querySelector("#albums").appendChild(element)
}

async function getAlbums() {
	return await getJSON("/api/albums/")
}

async function showAlbums() {
	let albums = await getAlbums()
	for (let album of albums) {
		console.log("Adding album")
		appendAlbum(album)
	}
}

window.onload = function() {
	showAlbums().catch(console.log)
}
