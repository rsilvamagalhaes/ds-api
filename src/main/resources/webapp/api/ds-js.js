function Query(kind) {
	this.kind = kind;
	this.toJSON = function() {
		return {kind: this.kind};
	}
}
