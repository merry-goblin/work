
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
					for (let i in grids) {
						grids[i].remove();
						delete grids[i];
					}
					grids = {};
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
