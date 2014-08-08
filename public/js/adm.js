define(['jquery', 'ds-js'], function($, ds) {

	var QueryView = function(selector) {
		this.el = $(selector);

		this.getQueryString = function() {
			return this.el.find('.query-text').val();
		}
		this.bindEvents = function(executeCB) {
			this.el.on('click', '.execute-query', executeCB);
			this.el.on('keypress', '.query-text', function(evt) {
				if (evt.which === 10) {
					executeCB.call();
				}
			});
		}
	}

	var QueryController = function(selector) {

		var _this = this;
		this.view = new QueryView(selector);
		this.queryEl = $(selector).find('.query-result');

		this.executeQuery = function() {
			var queryStr = _this.view.getQueryString();
			var query = eval(queryStr);
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
		
		this.hidePage = function(index){
			this.tbody.find("tr.page" + index).hide();
		}

		this.setQueryTitle = function(title) {
			this.el.find('h1').html(title);
		}
		this.setHeaders = function(numOfFields) {
			var headers = [];
			for (var i = 0; i < numOfFields; i++) {
				headers.push('<th></th>');
			}
			this.header.html(headers.join(''));
		};
		this.setHeader = function(fieldName, headerIndex) {
			this.header.find('th:eq(' + headerIndex + ')').html(fieldName);
		}
		this.addRow = function(currentPage, numOfFields) {
			this.lastRow = $('<tr class="page' + currentPage + '"></tr>').appendTo(this.tbody);
			var rows = [];
			for (var i = 0; i < numOfFields; i++) {
				rows.push('<td>&lt;missing&gt;</td>');
			}
			this.lastRow.html(rows.join(''));
		}
		this.setValue = function(index, value) {
			this.lastRow.find('td:eq(' + index + ')').html(value);		
		}
		this.reset = function() {
			this.tbody.html('');
			this.header.html('');
			this.el.find('.no-results').remove();
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
			jqXHR.list(processResults);
			jqXHR.done(this.process);
			jqXHR.iterate(this.append);
			return jqXHR;
		}
		this.next = function() {
			var jqXHR = this.query.next();
			jqXHR.list(processResults);
			jqXHR.iterate(this.append);
			jqXHR.done(function() {
				_this.view.hidePage(_this.query.getCurrentPage() - 1);
			});
			return jqXHR;		
		}
		this.process = function(result) {
			_this.view.setQueryTitle(_this.query.kind);
		}
		this.append = function(result) {
			_this.view.addRow(_this.query.getCurrentPage(), _this.headers.length);
			for (var i = 0; i < result.length; i++) {
				var field = result[i];
				processValue(field);
				processHeader(field);
			}
		}
		var getHeaderIndex = function(fieldName) {
			return _this.headers.indexOf(fieldName);
		}
		var addHeader = function(field) {
			var fieldName = field.field;
			if (getHeaderIndex(fieldName) < 0) {
				_this.headers.push(fieldName);
			}
		}
		var processHeader = function(field) {
			var fieldName = field.field;
			_this.view.setHeader(fieldName, getHeaderIndex(fieldName));
		}
		
		var processValue = function(field) {
			var fieldName = field.field;
			var fieldValue = field.value;
			var headerIndex = _this.headers.indexOf(fieldName);
			_this.view.setValue(headerIndex, fieldValue);
		}
		var processResults = function(results) {
			for (var i = 0; i < results.length; i++) {
				var result = results[i];
				for (var j = 0; j < result.length; j++) {
					var field = result[j];
					addHeader(field);
				}
			}
			_this.view.setHeaders(_this.headers.length);
		}
	}

	var init = function(selector) {
		var ctrl = new QueryController(selector);
		return ctrl;
	}
	return {ResultTableController : ResultTableController, init : init};
});
