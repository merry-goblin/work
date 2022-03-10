
(function($) {

	let settings = {
		nbCells: 70
	};
	var grid = new merryGoblin.drawGrid(settings);
	grid.new();

	var jqxhr = $.get("api/player/getARandomGrid/10", function(data) {
		console.log(data);
	});

})(jQuery);
