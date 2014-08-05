define(['jquery'], function($) {
	function Query(kind) {

		var EQ_FILTER = '=';
		var NEQ_FILTER = '!=';
		var GT_FILTER = '>';
		var GTE_FILTER = '>=';
		var LTE_FILTER = '<=';
		var LT_FILTER = '<';
		var IN_FILTER = 'in';

		var _this = this;
		this.kind = kind;
		this.filters = [];
		this.order = [];
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
			this.order = $.makeArray(arguments);
			return this;
		}
		this.toJSON = function() {
			var json = {};
			toSafeJSON('kind', this.kind, json);
			toSafeJSON('fields', this.fields, json);
			if (this.filters.length > 0) {
				json.filters = this.filters;
			}
			if (this.order.length > 0) {
				json.order = this.order;
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



