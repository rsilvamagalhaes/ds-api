define(['jquery'], function($) {
	function Key() {
		var _this = this;
		if (arguments.length == 1) {
			this.raw = arguments[0];
		} else {
			var key = {};
			_this.key = key;
			var entity, id;
			for (var idx = arguments.length - 1; idx > 0; idx = idx - 2) {
				var entity = arguments[idx - 1]
				var id = arguments[idx];
				key.entity = entity;
				if (typeof id == 'string') {
					key['name'] = id;
				} else 	if (typeof id == 'number') {
					key['id'] = id;
				}
				console.info('_this.key', _this.key, idx);
				if (idx > 1) {
					var ancestor = {};
					key.ancestor = ancestor;
					key = ancestor;
				}
			};
		}
		this.toJSON = function() {
			if (this.raw) {
				var json = {};
				toSafeJSON('raw', this.raw, json);
				return json;
			} else {
				return $.extend(this.key, {});
			}
		}
	}
	Key.raw = function(rawData) {
		var key = new Key(rawData);
		return key;
	}
	function Query(kind) {

		var EQ_FILTER = '=';
		var NEQ_FILTER = '!=';
		var GT_FILTER = '>';
		var GTE_FILTER = '>=';
		var LTE_FILTER = '<=';
		var LT_FILTER = '<';
		var IN_FILTER = 'in';

		var ASC_DIRECTION = 'ASC';
		var DESC_DIRECTION = 'DESC';

		var _this = this;
		this.kind = kind;
		this.filters = [];
		this.select = function() {
			this.fields = $.makeArray(arguments);
			return this;
		}
		this.eq = function(field, value) {
			return addFilter(field, EQ_FILTER, value);
		}
		this.inEq = function() {
			var field = arguments[0];
			var value = $.makeArray(arguments).slice(1);
			return addFilter(field, IN_FILTER, value);
		}
		this.neq = function(field, value) {
			return addFilter(field, NEQ_FILTER, value);
		}
		this.gt = function(field, value) {
			return addFilter(field, GT_FILTER, value);
		}
		this.gte = function(field, value) {
			return addFilter(field, GTE_FILTER, value);
		}
		this.lt = function(field, value) {
			return addFilter(field, LT_FILTER, value);
		}
		this.lte = function(field, value) {
			return addFilter(field, LTE_FILTER, value);
		}
		var addFilter = function(field, operator, value) {
			_this.filters.push({field: field, operator: operator, value: value});
			return _this;
		}
		this.order = function() {
			this.ordering = {direction : ASC_DIRECTION, fields : $.makeArray(arguments)};
			return this;
		}
		this.orderDesc = function() {
			this.ordering = {direction : DESC_DIRECTION, fields : $.makeArray(arguments)};
			return this;
		}
		this.limit = function(lim) {
			this.lim = lim;
			return this;
		}
		this.ancestor = function(ancestor) {
			this.ancestorKey = ancestor;
			return this;
		}
		this.key = function(queryKey) {
			this.queryKey = queryKey;
			return this;
		}
		this.toJSON = function() {
			var json = {};
			toSafeJSON('kind', this.kind, json);
			toSafeJSON('fields', this.fields, json);
			toSafeJSON('order', this.ordering, json);
			toSafeJSON('limit', this.lim, json);
			if (this.ancestorKey) {
				json.ancestor = this.ancestorKey.toJSON();
			}
			if (this.queryKey) {
				json.key = this.queryKey.toJSON();
			}
			if (this.filters.length > 0) {
				json.filters = this.filters;	
			}
			return json;
		}
	}
	// utils
	var toSafeJSON = function(key, obj, json) {
		if (obj) {
			json[key] = obj;
		}
	}
	return {Query : Query, Key: Key}
});



