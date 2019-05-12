// @author rubenwardy

function appendAlbum(album) {
	let element = document.createElement("div")
	let picture = album.picture || '/dummy/?title=' + encodeURI(album.title)
	element.innerHTML = `<img src="${picture}" class="is-1by1">
		<h3 class="title is-5 is-marginless">${album.title}</h3>
		<a class="subtitle is-6">${album.artist}</a>`;
	element.setAttribute("class", "column is-one-fifth is-1by1")
	element.setAttribute("data-id", album.id)

	document.querySelector("#albums").appendChild(element)
}

async function showAlbums() {
	let albums = await api.getAlbums()
	for (let album of albums) {
		appendAlbum(album)
	}
}

window.onload = function() {
	showAlbums().then(function() {
		player.playAlbum(148)
	}).catch(console.log)
}
