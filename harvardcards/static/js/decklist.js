require(['jquery', 'lodash', 'bootstrap'], function($, _, bootstrap){

	var DeckList = function(){
		var deckCount = 0;
		this.init(deckCount);
	};
	
	_.extend(DeckList.prototype, {
		init: function(deckCount){
			this.addNew(deckCount);
			this.editableText();
			this.mouseoverMenu();
			this.deleteButton();
	
		},
		
		addNew: function(deckCount){
			$('.new-deck-btn').click(function(){
				// new temporary ID for the element
				tempId = 'tmpdeck'+deckCount;
				// create a new <li> there
				var deckTmpl = '<li class="deck"><div id="'+tempId+'" class="deck-text">Deck Name</div></li>';
				$(this).parent().append(deckTmpl);
				var collection_id = $(this).data('collection_id');
				//console.log("collection_id: "+ collection_id);
				// add the editable field
				$('#'+tempId).editable(function(value, settings){
					return value;
				}, { 
					tooltip   : 'Click to edit...',
					cssclass: 'editable',
					style: 'inherit',
					onblur: 'submit',
					// save it when done editing...
					callback: function(value, settings){
						// send ajax to save it
						$.ajax({
							type: 'POST',
							url: '/deck/create/',
							data: {title: $('#'+tempId).html(), collection_id: collection_id},
							success: function(data, statusText){
								if(data.success){
						
								} else {
									alert("Error: "+data.message)
								}
							},
							error: function(request, statusText){
								alert("Request failed.");
							}
						});
				
						// add data to element
				
					}
				});
				// activate it
				$('#'+tempId).trigger('click');
				
				deckCount++;
			});
		
		},
		
		editableText: function(){
			$('.deck-text').editable(function(value, settings){
				return value;
			}, { 
				tooltip   : 'Click to edit...',
				cssclass: 'editable',
				style: 'inherit',
				onblur: 'submit',
				// save it when done editing...
				callback: function(value, settings){
					// send ajax to save it
					$.ajax({
						type: 'POST',
						url: '/deck/create/',
						data: {title: $(this).html(), deck_id: $(this).data('deck_id')},
						success: function(data, statusText){
							if(data.success){
					
							} else {
								alert("Error: "+data.message)
							}
						},
						error: function(request, statusText){
							alert("Request failed.");
						}
					});
			
					// add data to element
			
				}
			});
			
		},
		
		mouseoverMenu: function(){
			$('.deck').mouseover(function(){
				$(this).children('.deck-controls').removeClass('hide');
				$(this).children('.deck-delete-btn').removeClass('hide');
		
			});
			$('.deck').mouseout(function(){
				$(this).children('.deck-controls').addClass('hide');
				$(this).children('.deck-delete-btn').addClass('hide');
		
			});
	
		},
		
		deleteButton: function(){
			$('.deck-delete-btn').click(function(){
				listItem = $(this).parent();
				$.ajax({
					type: 'POST',
					url: '/deck/delete/',
					data: {deck_id: listItem.data('deck_id')},
					success: function(data, statusText){
						if(data.success){
							listItem.remove();
						} else {
							alert("Error: "+data.message)
						}
					},
					error: function(request, statusText){
						alert("Request failed.");
					}
				});
			});
			
		}
		
	});
	
	return new DeckList();
	
	
});