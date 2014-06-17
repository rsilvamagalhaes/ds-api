define(['jquery'], function($) {
	function Query(kind) {

		var EQ_FILTER = '=';
		var GT_FILTER = '>';
		var LT_FILTER = '<';

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
		this.gt = function(field, value) {
			return addFilter(field, GT_FILTER, value);
		}
		this.lt = function(field, value) {
			return addFilter(field, LT_FILTER, value);
		}
		var addFilter = function(field, operator, value) {
			_this.filters.push({field: field, operator: operator, value: value});
			return _this;
		}
		this.toJSON = function() {
			var json = {};
			toSafeJSON('kind', this.kind, json);
			toSafeJSON('fields', this.fields, json);
			if (this.filters.length > 0) {
				json.filters = this.filters;
			}
			return json;
		}
		var toSafeJSON = function(key, obj, json) {
			if (obj) {
				json[key] = obj;
			}
		}
	}
	return {Query : Query}
});



