define(['jquery'], function($, ds) {

	function InsertModel() {
		this.name = null;
		this.value = null;
		this.type = null;

		this.create = function(name, value, type) {
			this.name = name;
			this.value = value;
			this.type = type;
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
				field['value'] = item.value;

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
				var name = $('.field-name').val();
				var value = $('.field-value').val();
				var type = 'string';

				controller.add(name, value, type);
				$('.left .form-control.entity').val('');
				refreshList();
			});
		}

		var save = function() {

			$('#saveEntity').click(function(){
				controller.save().complete(function(){
					clearAllFields();
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

		changeEntityKind();
		clickAddNewField();
		save();
	}

	var init = function() {
		var view = new InsertView();
		return view;
	}

	return {init : init};
});
