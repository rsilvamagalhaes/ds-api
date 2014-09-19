define(['jquery'], function($, ds) {

	function InsertModel() {
		this.name = null;
		this.value = null;
		this.type = null;

		var types = {
			0: 'string',
			1: 'date'
		};

		this.create = function(name, value, type) {
			this.name = name;
			this.value = value;
			this.type = types[type];
		}
	}

	function InsertController() {

		var fields = [];

		this.add = function(name, value, type) {
			var insert = new InsertModel();
			insert.create(name, value, type)

			fields.push(insert);
		}

		this.getAllFields = function() {
			return fields;
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

			json['kind'] = 'User';
			var new_fields = [];
			for (i in fields) {

				var item = fields[i];
				var field = {};

				field['field'] = item.name;

				var value = item.value;
				if (item.type == 'date')
					value = parseInt(item.value);
				
				field['value'] = value;
				field['type'] = item.type;

				new_fields.push(field);
			}

			json['fields'] = new_fields;

			return json;
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
			var name = $('.field-name').val();
			var value = $('.field-value').val();
			var type = $('#fields-types :selected').attr('data-type');

			controller.add(name, value, type);
			$('.left .form-control.entity').val('');
			refreshList();
		}

		var save = function() {

			$('#saveEntity').click(function(){
				controller.save().complete(function(){
					clearAllFields();
					alert('Informacoes salvas :)')
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

		var clearAllFields = function() {
			$('#created-fields').hide();
			$('#created-fields > div').remove();
			$('.left .form-control').val('');
			$('#title-kind-entity').text('Kind Entity');
		}

		var tapEnterInValue = function() {
			$('.field-value').keyup(function(e){
				if(e.keyCode == 13) {
					addNewField();
					$('.field-name').focus();
				}
			});
		}

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
