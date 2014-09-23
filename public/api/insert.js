define(['jquery'], function($) {

	function InsertModel() {
		this.modelKind = null;

		this.name = null;
		this.value = null;
		this.type = null;
		this.kind = null;

		var types = {
			0: 'string',
			1: 'date',
			2: 'key',
			3: 'list'
		};

		this.create = function(modelKind, name, value, type, kind) {
			this.modelKind = modelKind;
			this.name = name;
			this.value = value;
			this.type = types[type];
			this.kind = kind;
		}
	}

	function InsertController() {

		var fields = [];

		this.add = function(modelKind, name, value, type, kind) {
			var insert = new InsertModel();
			insert.create(modelKind, name, value, type, kind);
			fields.push(insert);
		}

		this.getAllFields = function() {
			return fields;
		}

		this.clearFields = function(){
			fields = [];
		}

		this.save = function() {
			return $.ajax({
				dataType: "json",
				contentType: 'application/json',
				type: 'POST',
				url: '/api/entity',
				data : JSON.stringify(this.toJSON())
			});
		}

		this.toJSON = function() {
			var json = {};

			json['kind'] = fields[0].modelKind;
			var new_fields = [];
			for (i in fields) {
				var item = fields[i];
				var field = {};

				field['field'] = item.name;
				field['value'] = createValueByFilter(item);
				field['type'] = item.type;

				new_fields.push(field);
			}

			json['fields'] = new_fields;

			return json;
		}

		var createValueByFilter = function(item) {
			var value = item.value;
			if (item.type == 'date')
				value = parseInt(item.value);
			else
				if (item.type == 'key') {
					value = {};
					value['kind'] = item.kind;
					value['id'] = item.value;
				}
				else 
					if (item.type == 'list') {
						var items = value.split(',')
						var all_itens = []
						for (i in items)
							all_itens.push(items[i].replace(' ',''));
						value = all_itens	
					}

			return value;
		}
	}

	function InsertView() {

		var controller = new InsertController();

		var clickAddNewField = function() {
			$('#add-field').click(function() {
				addNewField();
			});
		}

		var addNewField = function() {
			var modelKind = $('.form-control.field-kind').val();
			var name = $('.field-name').val();
			var value = $('.field-value').val();
			var type = $('#fields-types :selected').attr('data-type');
			var kind = $('#item-kind input').val();

			controller.add(modelKind, name, value, type, kind);
			$('.left .form-control.entity').val('');
			refreshList();
		}

		var save = function() {
			$('#saveEntity').click(function(){
				controller.save().complete(function(){
					clearAllFields();
					controller.clearFields();
					alert('Informacoes salvas')
				});
			});
		}

		var changeEntityKind = function() {
			$('.field-kind').change(function(){ 
				$('#title-kind-entity').text($(this).val());
			});
		}

		var refreshList = function() {
			$('#created-fields > div').remove();
			var list = $('#created-fields');

			var fields = controller.getAllFields();
			for (var i in fields) {
				var container = $('<div class="container-fluid" />');
				var item = $('<div class="navbar-header" />');

				item.append('<a class="navbar-brand" href="#">'+ fields[i].name + '</a>');
				item.append('<p class="navbar-text">'+ fields[i].value +'</p>');
				item.append('<p class="navbar-text type">'+ fields[i].type +'</p>');
				container.append(item);
				list.append(container);
			}

			$('#created-fields').show();
		};

		var showKeyField = function() {
			$('#fields-types').change(function(){
				var type = $('#fields-types option:selected').attr('data-type');

				if (type==2) {
					$('#item-kind').show();
				} else if (type==3) {
					$('.form-control.field-value.entity').attr('placeholder','ex: item1,item2,item3')
				} else {
					$('.form-control.field-value.entity').attr('value');
					$('#item-kind').hide();
				}
			});
		}

		var clearAllFields = function() {
			$('#created-fields').hide();
			$('#created-fields > div').remove();
			$('.left .form-control').val('');
			$('#title-kind-entity').text('Kind Entity');
			$('#item-kind').val('');
			$('#item-kind').hide();
		}

		var tapEnterInValue = function() {
			$('.field-value').keyup(function(e){
				if(e.keyCode == 13) {
					addNewField();
					$('.field-name').focus();
				}
			});
		}

		showKeyField();
		changeEntityKind();
		clickAddNewField();
		tapEnterInValue();
		save();
	}

	var init = function() {
		var view = new InsertView();
		return view;
	}

	return {init : init};
});
