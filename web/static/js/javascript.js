function loadTicker(div, url) {
	$.get(url, function(data) {
		$(div).html(data);
	});
	timer = setTimeout(function() {
		loadTicker(url);
	}, 3000);
}

function search() {
	term = $('input#searchbox').val();
	if (term.charAt(0) == '@') {
		term = term.substring(1);
	}
	url = '/search/' + escape(term);
	$.get(url, function(data) {
		window.location = data;
	});
}

$(function() {
	$('.disconnect form a').on('click', function(e) {
		e.preventDefault();
		$(this).parent().parent().submit();
	});
});

$(function(){
	$('.tab-container li').click(function(){
		item = $(this).attr('id');
		$('.tab-container li').removeClass('tab-selected');
		$(this).addClass('tab-selected');
		
		if(item == 'printer'){
			$('.tab-batch-printer').hide();
			$('.tab-printer').show();
			$('.printer-output').show();
		}
		else{
			$('.tab-printer').hide();
			$('.printer-output').hide();
			$('.tab-batch-printer').show();
		}
	});
});
$(function(){
	$('.verify-payment').live('click',function(e){
		e.preventDefault();
		url = $(this).attr('href');
		note_id = url.split('/')[2];
		$.ajax({url:url,
				success:function(data){
					if(data.code=='200'){
						$('#3-'+note_id).hide(1000);
					}
					else{
						$('#3-'+note_id).addClass('error');
					}
				}
		});
	});
});
