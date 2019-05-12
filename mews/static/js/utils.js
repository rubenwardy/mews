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
