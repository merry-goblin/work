
/** @namespace */
var merryGoblin = merryGoblin || {};

(function($, buybox) {

	merryGoblin.drawGrid = function(settings) {

		var self = null; // Defined in "new" public function

		//	Default values
		var defaultGridContainerSelector = '.merry-goblin-draw-grid-container';
		var defaultGridSelector          = '.merry-goblin-draw-grid';
		var defaultNbCells               = 50;

		//	Grid settings
		var nbCells = null;

		var cells = [];

		//	Dom selectors
		var gridSelector = null;

		//	Dom elements
		var $gridContainer = null;

		//	Others
		var idCounter = 0; // To get a unique IDs for DOM elements

		function createNewDomGrid() {

			let id = getUniqueId();
			let $grid = $("<div class='"+gridSelector+"' id='merry-goblin-draw-grid-"+id+"'>Grid</div>").appendTo($gridContainer);

			return $grid;
		}

		function createDomCell() {

			
		}

		function getUniqueId() {

			idCounter++;
			return idCounter;
		}

		var scope = {

			configure: function($settings) {

				$gridContainer = ($settings['gridContainerSelector'] != null)  ? $($settings['gridContainerSelector'])  : $(defaultGridContainerSelector);
				gridSelector   = ($settings['gridSelector'] != null)           ? $settings['gridContainerSelector']     : defaultGridSelector;
				nbCells        = ($settings['nbCells'] != null)                ? $($settings['nbCells'])                : defaultNbCells;
			},

			/**
			 * @return null
			 */
			new: function() {

				self = this;

				//	Does configuration has been called
				if ($gridContainer == null) {
					this.configure({});
				}

				//	Create a new grid
				createNewDomGrid();
			}
		};
		return scope;
	}

})(jQuery, merryGoblin);
