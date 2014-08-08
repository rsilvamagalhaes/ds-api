define(['jquery', 'ds-js'], function($, ds) {

	var QueryView = function(selector) {
		this.el = $(selector);

		this.getQueryString = function() {
			return this.el.find('.query-text').val();
		}
		this.bindEvents = function(executeCB) {
			this.el.on('click', '.execute-query', executeCB);
		}
	}

	var QueryController = function(selector) {

		var _this = this;
		this.view = new QueryView(selector);
		this.queryEl = $(selector).find('.query-result');

		this.executeQuery = function() {
			var queryStr = _this.view.getQueryString();
			var query = eval(queryStr);
			console.info('queryStr', queryStr, query);
			var ctrl = new ResultTableController(_this.queryEl, query);
			return ctrl.execute();
		}
		this.view.bindEvents(this.executeQuery);
	}

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
		this.reset = function() {
			this.tbody.html('');
			this.header.html('');
		}
	}

	var ResultTableController = function(selector, query) {

		var _this = this;
		this.view = new ResultTableView(selector);
		this.query = query;
		this.headers = [];
		this.execute = function() {
			this.view.reset();
			var jqXHR = this.query.execute();
			jqXHR.iterate(this.append);
			jqXHR.done(this.process);
			return jqXHR;
		}
		this.process = function(result) {
			_this.view.setQueryTitle(_this.query.kind);
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

	var init = function(selector) {
		var ctrl = new QueryController(selector);
		return ctrl;
	}
	return {ResultTableController : ResultTableController, init : init};
});
