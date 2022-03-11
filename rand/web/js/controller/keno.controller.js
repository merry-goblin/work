
(function($, reactor) {

	let settings = {
		nbCells: 70,
		maxSelectableCells: 10
	};

	//	All the grids
	var grids = {};

	//	Display a new grid & listen of events triggered when a button is clicked
	$('.new-grid-button').click(function() {

		//	Build a new grid
		let grid = new merryGoblin.drawGrid(settings);
		let gridNumber = grid.new();
		grids["num"+gridNumber] = grid;

		//	UI: fill grid randomly
		reactor.addEventListener('button-fill-grid-randomly-clicked', function(params) {

			grids["num"+params.gridNumber].reset();
			let jqxhr = $.get("api/player/getARandomGrid/10", function(numberList) {

				grids["num"+params.gridNumber].selectCells(numberList);
			});

		});
	});

})(jQuery, reactor);
