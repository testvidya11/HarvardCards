define(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){
	var Field = function(label, field_type, field_id, display, value, cards_fields_id){
		this.label = label;
		this.field_type = field_type;
		this.field_id = field_id;
		this.display = display;
		this.value = value;
		this.cards_fields_id = cards_fields_id;
		var display_class = "display";
		if(display){
			display_class = "display";
		} else {
			display_class = "reveal";
		}
		
		if(field_type == 'T'){
			this.edit_template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+'</span> '
				+ '<input class="text-field-template" data-id="'+field_id+'" type="text"/></div> ';
			this.view_template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+':</span> '
				+ '<span class="text-field-template" type="text" data-cf_id="'+cards_fields_id+'">'+this.value+'</span></div> ';
		} else if(field_type == 'I'){
			this.edit_template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+'</span> '
				+ '<input class="img-field-template" data-id="'+field_id+'" type="text"/></div> ';
			this.view_template = '<div class="field-template '+display_class+'"><span class="mylabel">'+label+'</span> '
				+ '<img class="img-field-template" src="'+this.value+'" data-cf_id="'+cards_fields_id+'"/></div> ';
		} else {
			this.template = 'Not a valid type';
		}
	}
	
	_.extend(Field.prototype, {
		
	});
	
	return Field;
	

});