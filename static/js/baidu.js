$(document).ready(function(){
	$('input[name="s"]').on('input', function(){
		var s = $.trim($(this).val());
		
		if(s == ''){
			$('.suggest-box').hide();
			return;
		}

		$.post("/baidu",{s:s,a:'suggest'},function(data){
			data = $.trim(data);
			
			if(data != ''){
				$('.suggest-box .nav ul').html(data)
				$('.suggest-box').show();
			}else{
				$('.suggest-box').hide();
			}

			$(".suggest-box .nav ul li a").click(function(e){
				e.preventDefault();
				$('input[name="s"]').val($(this).text());
				$('.suggest-box').hide();
			});
			
		});
	});

	$('form.forms').submit(function(e){
		e.preventDefault();

		$('.suggest-box').hide();
		var s = $.trim($('input[name="s"]').val());
		
		if(s == ''){
			return;
		}

		$.post("/baidu", {s:s}, function(data){
			$(".baidu-results").html(data);
		})
	})
	
});