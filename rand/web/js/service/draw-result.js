
/** @namespace */
var merryGoblin = merryGoblin || {};

(function($, merryGoblin) {

	merryGoblin.drawResult = function(p_settings) {

		var self = null; // Defined in "new" public function

		var settings = p_settings || {};

		//	Default values
		var defaultResultContainerSelector = '#merry-goblin-result-container';
		var defaultResultClassSelector     = 'merry-goblin-result-container';

		//	Dom elements
		var $resultContainer = null;

		/* Init */

		function configure() {

			//	CSS electors
			$resultContainer = (settings['resultContainerSelector'] != null)  ? $(settings['resultContainerSelector'])  : $(defaultResultContainerSelector);
		}

		/* Graphics */

		function resetContainer() {

			$resultContainer.empty();
		}

		function fillContainer(statistics) {


		}

		/* Utilitaries */

		function destroy() {

			self = null;
			settings = null;
			defaultResultContainerSelector = null;
			defaultResultClassSelector = null;
			$resultContainer = null;
		}

		var scope = {

			/**
			 * @return null
			 */
			displayStatistics: function(statistics) {

				self = this;

				//	Does configuration has been called
				if ($resultContainer == null) {
					configure();
				}

				resetContainer();
				fillContainer(statistics);
			}
		};
		return scope;
	}

})(jQuery, merryGoblin, reactor);
