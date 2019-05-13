// @author rubenwardy
api = (function() {
	async function getJSON(url, method, body) {
		let response = await fetch(new Request(url, {
			method: method || "get",
			credentials: "same-origin",
			body: body,
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json",
			},
		}))

		let text = await response.text()
		return JSON.parse(text)
	}

	async function getTrack(id) {
		return await getJSON("/api/tracks/" + id + "/")

	}

	async function getAlbums() {
		return await getJSON("/api/albums/")
	}

	async function getPlaylists() {
		return await getJSON("/api/playlists/")
	}

	async function getPlaylistTracks(id) {
		return await getJSON("/api/playlists/" + id + "/tracks/")
	}

	async function createPlaylist(title) {
		return await getJSON("/api/playlists/new/", "post", JSON.stringify({ title: title }))
	}

	async function updatePlaylistTracks(id, data) {
		return await getJSON("/api/playlists/" + id + "/tracks/", "post", JSON.stringify(data))
	}

	return {
		getTrack: getTrack,
		getAlbums: getAlbums,
		getPlaylists: getPlaylists,
		getPlaylistTracks: getPlaylistTracks,
		createPlaylist: createPlaylist,
		updatePlaylistTracks: updatePlaylistTracks,
	}
})()
