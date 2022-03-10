
/** @namespace */
var merryGoblin = merryGoblin || {};

(function($, buybox) {

	merryGoblin.drawGrid = function(p_settings) {

		var self = null; // Defined in "new" public function

		var settings = p_settings || {};

		//	Default values
		var defaultGridContainerSelector = '.merry-goblin-draw-grid-container';
		var defaultGridClassSelector     = 'merry-goblin-draw-grid';
		var defaultCellClassSelector     = 'merry-goblin-draw-grid-cell';
		var defaultNbCells               = 50;

		//	Grid settings
		var nbCells = null;
		var gridClassSelector = null;
		var cellClassSelector = null;

		//	Dom elements
		var $gridContainer = null;
		var $grid = null;

		//	Others
		var idCounter = 0; // To get a unique IDs for DOM elements

		function createNewDomGrid() {

			let gridNumber = getNumberOfGrids()+1;
			let id = getUniqueId();
			$grid = $("<div class='"+gridClassSelector+"' data-number='"+gridNumber+"' id='merry-goblin-draw-grid-"+id+"'><h4>Grid n°"+gridNumber+"</h4></div>").appendTo($gridContainer);

			createDomCells();
		}

		function createDomCells() {

			for (let i=1; i<=nbCells; i++) {
				let id = getUniqueId();
				$("<div class='"+cellClassSelector+"' data-number='"+i+"' id='merry-goblin-draw-grid-cell-"+id+"'><div>"+i+"</div></div>").appendTo($grid);
			}
		}

		function getUniqueId() {

			idCounter++;
			return idCounter;
		}

		function getNumberOfGrids() {

			return $('.'+gridClassSelector).length;
		}

		function configure() {

			$gridContainer    = (settings['gridContainerSelector'] != null)  ? $(settings['gridContainerSelector'])  : $(defaultGridContainerSelector);
			gridClassSelector = (settings['gridClassSelector'] != null)      ? settings['gridClassSelector']         : defaultGridClassSelector;
			cellClassSelector = (settings['cellClassSelector'] != null)      ? settings['cellClassSelector']         : defaultCellClassSelector;
			nbCells           = (settings['nbCells'] != null)                ? settings['nbCells']                   : defaultNbCells;
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
				createNewDomGrid();
			}
		};
		return scope;
	}

})(jQuery, merryGoblin);
