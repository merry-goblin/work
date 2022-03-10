
(function($) {

	let settings = {
		nbCells: 70,
		maxSelectableCells: 10
	};

	var grids = {};

	let grid = new merryGoblin.drawGrid(settings);
	let gridNumber = grid.new();
	grids["num"+gridNumber] = grid;

	var reactor = grid.getReactor();
	reactor.addEventListener('button-fill-grid-randomly-clicked', function(params) {

		grids["num"+params.gridNumber].reset();
		var jqxhr = $.get("api/player/getARandomGrid/10", function(numberList) {

			grids["num"+params.gridNumber].selectCells(numberList);
		});

	});

})(jQuery);
