
(function($) {

	var jqxhr = $.get("api/player/getARandomGrid/10", function(data) {
		console.log(data);
	});

})(jQuery);
