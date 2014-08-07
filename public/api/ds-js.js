define(['jquery'], function($) {
	function Key() {
		var _this = this;
		if (arguments.length == 1) {
			this.raw = arguments[0];
		} else {
			var key = {};
			_this.key = key;
			var kind, id;
			for (var idx = arguments.length - 1; idx > 0; idx = idx - 2) {
				var kind = arguments[idx - 1]
				var id = arguments[idx];
				key.kind = kind;
				if (typeof id == 'string') {
					key['name'] = id;
				} else 	if (typeof id == 'number') {
					key['id'] = id;
				}
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

		var DATE_TYPE = 'date';
		var KEY_TYPE = 'key'

		var API_URL = '/api/query';

		var _this = this;
		this.url = API_URL;
		this.kind = kind;
		this.filters = [];
		this.ordering = [];
		this.cursors = [];
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
			var filter = {field: field, operator: operator};
			if (value instanceof Date) {
				value = value.getTime();
				filter.type = DATE_TYPE;
			} else if (value instanceof Key) {
				value = value.toJSON();
				filter.type = KEY_TYPE;
			}
			filter.value = value;
			_this.filters.push(filter);
			return _this;
		}
		this.order = function() {
			for (var i = 0; i < arguments.length; i++) {
				this.ordering.push({field : arguments[i], direction: ASC_DIRECTION});
			}
			return this;
		}
		this.orderDesc = function() {
			for (var i = 0; i < arguments.length; i++) {
				this.ordering.push({field : arguments[i], direction: DESC_DIRECTION});
			}
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
			if (this.cursors.length > 0) {
				json.cursor = this.cursors[this.cursors.length - 1];
			}
			if (this.ordering.length > 0) {
				json.order = this.ordering;
			}
			return json;
		}
		var fetch = function() {
			var jqXHR = $.ajax({
				dataType: "json",
				type: 'get',
				url: _this.url,
				data : JSON.stringify(_this.toJSON())
			}).done(function(json) {
				_this.cursors.push(json.cursor) ;
			});
			jqXHR.list = function(cb) {
				jqXHR.done(function(json) {
					cb.call(_this, json.result);
				});
				return jqXHR;
			}
			jqXHR.iterate = function(cb) {
				jqXHR.done(function(json) {
					var result = json.result;
					for (var i = 0; i < result.length; i++) {
						cb.call(_this, result[i]);
					}
				});
				return jqXHR;
			}
			jqXHR.get = function(cb) {
				jqXHR.done(function(json) {
					var result = null;
					if (json.result.length > 0) {
						result = json.result[0];
					}
					cb.call(_this, result);
				});
				return jqXHR;
			}
			return jqXHR;
		}
		this.execute = function() {
			this.cursors = [];
			return fetch();
		}
		this.next = function() {
			return fetch();
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



