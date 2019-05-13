// @author rubenwardy

function appendAlbum(album) {
	let element = document.createElement("div")
	let picture = album.picture || '/dummy/?title=' + encodeURI(album.title)
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
	element.querySelector(".action-play").addEventListener("click", function() {
		player.playAlbum(album.id)
	})
}

async function showAlbums() {
	let albums = await api.getAlbums()
	for (let album of albums) {
		appendAlbum(album)
	}
}

player = null
window.onload = function() {
	showAlbums().catch(console.log)
	player = new Player()

}
