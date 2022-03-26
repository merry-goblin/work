
(function($, reactor) {

	//	All the grids
	var grids = {};
	var result = new merryGoblin.drawResult();

	function newGrid() {

		let settings = {
			nbCells: 70,
			maxSelectableCells: 10
		};

		//	Build a new grid
		let grid = new merryGoblin.drawGrid(settings);
		let gridNumber = grid.new();
		grids["num"+gridNumber] = grid;
	}
	newGrid();

	//	UI: display a new grid & listen of events triggered when this button is clicked
	$('.new-grid-button').click(function() {

		newGrid();
	});

	//	UI: send all grids when this button is clicked
	$('.send-grids-button').click(function() {

		//	All grids have to be valid so we can accept to send those
		let gridsAreValid = true;
		for (let i in grids) {
			gridsAreValid = grids[i].doesGridCanBeSent();
			if (!gridsAreValid) {
				break;
			}
		}

		if (gridsAreValid) {

			//	Each numbers of each grids we will be sent as parameters of a ajax call with post for method of sending
			let params = {
				grids: []
			};
			for (let i in grids) {
				params.grids.push(grids[i].getSelectedNumbers());
			}

			var jqxhr = $.post(
				'api/player/grids',
				JSON.stringify(params),
				function(data) {
					//	Current grids are destroyed
					for (let i in grids) {
						grids[i].remove();
						delete grids[i];
					}
					grids = {};

					//	A new and empty grid is added
					newGrid();
				},
				'json'
			);
		}
		else {
			console.log("Grids are not fully filled for sending")
		}
	});

	//	UI: fill grid randomly
	reactor.registerEvent('button-fill-grid-randomly-clicked');
	reactor.addEventListener('button-fill-grid-randomly-clicked', function(params) {

		grids["num"+params.gridNumber].reset();
		$resource = 'api/player/grid/random/10';
		let jqxhr = $.get($resource, function(response) {

			let numberList = response.data;
			if (Array.isArray(numberList)) {
				grids["num"+params.gridNumber].selectCells(numberList);
			}
			else {
				console.log("An error occured. Resource "+$resource+" didn't sent back an expected response");
			}
		});

	});

	//	UI: draw
	$('.draw-button').click(function() {

		var jqxhr = $.post(
			'api/game/draw',
			null,
			function(data) {
				console.log("Draw response");
				console.log(data);
			},
			'json'
		);
	});

	//	UI: process
	$('.draw-process-button').click(function() {

		var jqxhr = $.post(
			'api/game/draw/process',
			null,
			function(response) {
				if (response.data.process == 'finished') {
					reactor.dispatchEvent('draw_prossessing_finished', {gameId: response.data.gameId});
				}
			},
			'json'
		);
	});

	reactor.registerEvent('draw_prossessing_finished');
	reactor.addEventListener('draw_prossessing_finished', function(params) {

		$resource = 'api/game/'+params.gameId+'/result';
		let jqxhr = $.get($resource, function(response) {

			
		});

	});

})(jQuery, reactor);
