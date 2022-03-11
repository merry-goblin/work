
/** @namespace */
var merryGoblin = merryGoblin || {};

(function($, merryGoblin, reactor) {

	merryGoblin.drawGrid = function(p_settings) {

		var self = null; // Defined in "new" public function

		var settings = p_settings || {};

		//	Default values
		var defaultGridContainerSelector = '#merry-goblin-draw-grid-container';
		var defaultGridClassSelector     = 'merry-goblin-draw-grid';
		var defaultCellClassSelector     = 'merry-goblin-draw-grid-cell';
		var defaultNbCells               = 50;
		var defaultMaxSelectableCells    = 5;

		//	Grid settings
		var nbCells = null;
		var maxSelectableCells = null;
		var gridClassSelector = null;
		var cellClassSelector = null;

		//	Dom elements
		var $gridContainer = null;
		var $grid = null;

		//	Others
		var idCounter = 0; // To get a unique IDs for DOM elements

		/* Init */

		function configure() {

			//	CSS electors
			$gridContainer     = (settings['gridContainerSelector'] != null)  ? $(settings['gridContainerSelector'])  : $(defaultGridContainerSelector);

			//	Class CSS selectors
			gridClassSelector  = (settings['gridClassSelector'] != null)      ? settings['gridClassSelector']         : defaultGridClassSelector;
			cellClassSelector  = (settings['cellClassSelector'] != null)      ? settings['cellClassSelector']         : defaultCellClassSelector;

			//	Grid parameters
			nbCells            = (settings['nbCells'] != null)                ? settings['nbCells']                   : defaultNbCells;
			maxSelectableCells = (settings['maxSelectableCells'] != null)     ? settings['maxSelectableCells']        : defaultMaxSelectableCells;
		}

		/* Graphics */

		function createNewDomGrid() {

			let gridNumber = getNumberOfGrids()+1;
			let id = getUniqueId();
			$grid = $("<div class='"+gridClassSelector+"' data-number='"+gridNumber+"' id='merry-goblin-draw-grid-"+id+"'><h4>Grid n°"+gridNumber+"</h4><div class='ui-grid'><button type='button' class='btn btn-dark fill-randomly-button'>Fill randomly</button></div></div>").appendTo($gridContainer);

			$fillRandomlyButton = $grid.find("button.fill-randomly-button");
			$fillRandomlyButton.click({gridNumber: gridNumber}, function() {

				reactor.dispatchEvent('button-fill-grid-randomly-clicked', {gridNumber: gridNumber});
			});

			createDomCells();

			return gridNumber;
		}

		function createDomCells() {

			for (let i=1; i<=nbCells; i++) {
				let id = getUniqueId();
				let $cell = $("<div class='"+cellClassSelector+"' data-number='"+i+"' id='merry-goblin-draw-grid-cell-"+id+"'><div>"+i+"</div></div>").appendTo($grid);
				$cell.click(function() {
					let number = $(this).attr('data-number');
					self.selectCell(number);
				});
			}
		}

		function selectCell(number) {

			let nbSelected = getNumberOfSelectedCells();

			let $cell = $grid.find('.'+cellClassSelector+'[data-number='+number+']');
			if ($cell.hasClass('selected')) {
				$cell.removeClass('selected');
			}
			else {
				if (nbSelected < maxSelectableCells) {
					$cell.addClass('selected');
				}
			}
		}

		function unselectCells() {

			$grid.find('.'+cellClassSelector).removeClass('selected');
		}

		/* Utilitaries */

		function getUniqueId() {

			idCounter++;
			return idCounter;
		}

		function getNumberOfGrids() {

			return $('.'+gridClassSelector).length;
		}

		function getNumberOfSelectedCells() {

			return $grid.find('.'+cellClassSelector+'.selected').length;
		}

		var scope = {

			/**
			 * @return null
			 */
			new: function() {

				self = this;

				//	Does configuration has been called
				if ($gridContainer == null) {
					configure();
				}

				//	Create a new grid
				let gridNumber = createNewDomGrid();

				return gridNumber;
			},

			reset: function() {

				unselectCells();
			},

			selectCells: function(numberList) {

				for (var i in numberList) {
					this.selectCell(numberList[i]);	
				}
			},

			selectCell: function(number) {

				selectCell(number);
			},

			getReactor: function() {

				return reactor;
			},

			doesGridCanBeSent: function() {

				let $gridIsValid = (getNumberOfSelectedCells() == maxSelectableCells);

				return $gridIsValid;
			},

			getSelectedNumbers: function() {

				let cells = [];

				$grid.find('.'+cellClassSelector+'.selected').each(function() {

					cells.push(Number($(this).attr('data-number')));
				});

				return cells;
			}
		};
		return scope;
	}

})(jQuery, merryGoblin, reactor);
