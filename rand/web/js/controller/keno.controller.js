
(function($, reactor) {

	let settings = {
		nbCells: 70,
		maxSelectableCells: 10
	};

	//	All the grids
	var grids = {};

	function newGrid() {

		//	Build a new grid
		let grid = new merryGoblin.drawGrid(settings);
		let gridNumber = grid.new();
		grids["num"+gridNumber] = grid;
	}
	newGrid();

	//	Display a new grid & listen of events triggered when this button is clicked
	$('.new-grid-button').click(function() {

		newGrid();
	});

	//	Send all grids when this button is clicked
	$('.send-grids-button').click(function() {

		let params = {
			test: 'test'
		};

		var jqxhr = $.post(
			'api/player/grids',
			params,
			function(data) {
				console.log('post successful');
			},
			'json'
		);
	});

	//	UI: fill grid randomly
	reactor.registerEvent('button-fill-grid-randomly-clicked');
	reactor.addEventListener('button-fill-grid-randomly-clicked', function(params) {

		grids["num"+params.gridNumber].reset();
		$ressource = 'api/player/grid/random/10';
		let jqxhr = $.get($ressource, function(numberList) {

			if (Array.isArray(numberList)) {
				grids["num"+params.gridNumber].selectCells(numberList);
			}
			else {
				console.log("An error occured. Ressource "+$ressource+" didn't sent back an expected response");
			}
		});

	});

})(jQuery, reactor);
