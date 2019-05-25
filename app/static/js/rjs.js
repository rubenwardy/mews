export class Model {
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

	notifyChange() {
		console.log("Changed " + this.constructor["name"] + "[" + this.id + "]: " + this)
		for (let func of this.watchers) {
			func(this)
		}
	}

	watch(func) {
		console.assert(func)
		this.watchers.push(func)
	}

	unwatch(func) {
		let index = this.watchers.indexOf(func)
		if (index > -1) {
			this.watchers.splice(index, 1)
			return true
		} else {
			return false
		}
	}
}

export class ViewModel {
	constructor(element) {
		this.element = element
		console.assert(element != null, `Null root element given to ${this.constructor["name"]}`)
		this._cb = this.onChange.bind(this)
		this.setTarget(null)
	}

	getTarget() {
		return this.target
	}

	setTarget(target) {
		if (this.target) {
			this.target.unwatch(this._cb)
		}
		if (target) {
			this.target = target
			this.target.watch(this._cb)
		}
		this.onChange(this.target)
	}

	invalidate() {
		this.onChange(this.target)
	}

	onChange(target) {}
}

let listeners = {}
let on_loads = []


window.onload = function() {
	on_loads.map(f => f())
}

export let rjs = {
	watch: function(evt, func) {
		listeners[evt] = listeners[evt] || []
		listeners[evt].push(func)
	},

	notify: function(evt, data) {
		listeners[evt].map(f => f())
	},

	onLoad: function(func) {
		on_loads.push(func)
	},

	getParentElementByClass: function(element, search, boundary) {
		const boundaryIsID = typeof(boundary) == "string"
		while (element != document.body &&
				((boundaryIsID && element.id != boundary) ||
					(!boundaryIsID && element != boundary))) {
			if (element.classList.contains(search)) {
				return element
			}

			element = element.parentNode;
		}

		return null
	}
}
