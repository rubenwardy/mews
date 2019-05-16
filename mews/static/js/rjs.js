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

	notifyChange() {
		console.log("Changed " + this.constructor["name"] + "[" + this.id + "]: " + this)
		for (var func of this.watchers) {
			func(this)
		}
	}

	watch(func) {
		console.assert(func)
		this.watchers.push(func)
	}

	unwatch(func) {
		var index = this.watchers.indexOf(func)
		if (index > -1) {
			this.watchers.splice(index, 1)
			return true
		} else {
			return false
		}
	}
}

class ViewModel {
	constructor(element) {
		this.element = element
		this._cb = this.onChange.bind(this)
		this.setTarget(null)
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

	onChange(target) {}
}

rjs = (function() {
	var listeners = {}

	return {
		watch: function(evt, func) {
			listeners[evt] = listeners[evt] || []
			listeners[evt].push(func)
		},

		notify: function(evt, data) {
			for (let func of listeners[evt]) {
				func(data)
			}
		},
	}
})()
