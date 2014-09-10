define(['jquery', 'ds-js'], function($, ds) {

	var QueryView = function(selector) {

		var _this = this;
		this.el = $(selector);

		this.getQueryString = function() {
			return this.el.find('.query-text').val();
		}
		this.bindEvents = function(delegate) {
			this.el.on('click', '.execute-query', delegate.execute);
			this.el.on('keypress', '.query-text', function(evt) {
				if (evt.which === 10) {
					delegate.execute.call();
				}
			});
			this.el.on('click', '.next-page', delegate.next);
		}
		this.showSuccess = function(msg) {
			showMessage(msg, 'success');
		};
		this.showWarning = function(msg) {
			showMessage(msg, 'warning');
		};
		var showMessage = function(msg, level) {
			var msgs = _this.el.find('.messages');
			msgs.html('');
			var msg = $('<div class="alert alert-' + level + '" role="alert">' + msg + '</div>').appendTo(msgs);
			window.setTimeout(function() {
				msg.slideUp('fastest');
			}, 2000);
		};
	}

	var QueryController = function(selector) {

		var _this = this;
		this.view = new QueryView(selector);
		this.queryEl = $(selector).find('.query-result');
		this.ctrl = null;

		this.execute = function() {
			try {
				var query = _this.parseQuery();
				if (query) {		
					_this.ctrl = new ResultTableController(_this.queryEl, query);
					var jqXHR = _this.ctrl.execute();
					jqXHR.fail(function(jqXHR, status, error) {
						_this.view.showWarning(error);
					});
					return jqXHR;
				}
			} catch (e) {
				_this.view.showWarning(e.toString());
			}
		}
		this.parseQuery = function() {
			var queryStr = _this.view.getQueryString().trim();
			if (queryStr) {
				return eval(queryStr);
			} else {
				return null;
			}
		}
		this.next = function() {
			if (_this.ctrl) {
				return _this.ctrl.next();
			}
		}
		this.view.bindEvents(this);
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

			for (i in result['fields']) {
				var field = result['fields'][i];
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
				var fields = results[i]['fields'];
				for (var j = 0; j < fields.length; j++) {
					var field = fields[j];
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
