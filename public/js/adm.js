define(['jquery', '../api/ds-js', '../js/doT.min'], function($, ds, dot) {

	var ResultTableView = function(selector) {

		var _this = this;
		this.el = $(selector);
		this.header = this.el.find('table thead tr:eq(0)');
		this.tbody = this.el.find('table tbody');
		
		this.setQueryTitle = function(title) {
			this.el.find('h1').html(title);
		}
		this.addHeader = function(fieldName) {
			this.header.append('<th>' + fieldName + '</th>')
		}
		this.addRow = function() {
			this.lastRow = $('<tr></tr>').appendTo(this.tbody);
		}
		this.setValue = function(index, value) {
			fillWithRows(index + 1);
			this.lastRow.find('td:eq(' + index + ')').html(value);		
		}
		var fillWithRows = function(amount) {
			var actual = _this.lastRow.find('td').length;
			var missing = amount - actual;
			if (missing > 0) {
				for (var i = 0; i < missing; i++) {
					_this.lastRow.append('<td></td>')
				}
			}
		}
	}

	var ResultTableController = function(selector, query) {

		var _this = this;
		this.view = new ResultTableView(selector);
		this.query = query;
		this.headers = [];
		this.execute = function() {
			var jqXHR = this.query.execute();
			jqXHR.iterate(this.append);
			jqXHR.done(this.process);
			return jqXHR;
		}
		this.process = function(result) {
			_this.view.setQueryTitle(this.query.kind);
		}
		this.append = function(result) {
			_this.view.addRow();
			for (var i = 0; i < result.length; i++) {
				var field = result[i];
				processHeader(field);
				processValue(field);
			}
		}
		var processHeader = function(field) {
			var fieldName = field.field;
			if (_this.headers.indexOf(fieldName) < 0) {
				_this.headers.push(fieldName);
				_this.view.addHeader(fieldName);
			}
		}
		var processValue = function(field) {
			var fieldName = field.field;
			var fieldValue = field.value;
			var headerIndex = _this.headers.indexOf(fieldName);
			_this.view.setValue(headerIndex, fieldValue);
		}
	}

	var showResults = function(selector, query) {
		var ctrl = new ResultTableController(selector, query);
		return ctrl.execute();
	}
	return {ResultTableController : ResultTableController, showResults: showResults};
});
