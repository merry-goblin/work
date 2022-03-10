
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

		//	Dom elements
		var $gridContainer = null;

		function createDomCell() {

			
		}

		var scope = {

			configure: function($settings) {

				$gridContainer = ($settings['gridContainerSelector'] != null)  ? $($settings['gridContainerSelector'])  : $(defaultGridContainerSelector);
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

				
			}
		};
		return scope;
	}

})(jQuery, merryGoblin);
