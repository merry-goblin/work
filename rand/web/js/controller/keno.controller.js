
(function($) {

	let settings = {
		nbCells: 70,
		maxSelectableCells: 10
	};

	//	All the grids
	var grids = {};

	//	Build a new grid
	$('.new-grid-button').click(function() {

		let grid = new merryGoblin.drawGrid(settings);
		let gridNumber = grid.new();
		grids["num"+gridNumber] = grid;

		//	Events
		let reactor = grid.getReactor();

		//	UI: fill grid randomly
		reactor.addEventListener('button-fill-grid-randomly-clicked', function(params) {

			grids["num"+params.gridNumber].reset();
			let jqxhr = $.get("api/player/getARandomGrid/10", function(numberList) {

				grids["num"+params.gridNumber].selectCells(numberList);
			});

		});
	});

})(jQuery);
