
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

			let resultContent = "<b>number of sent grid:</b> "+statistics.nbPlayedGrids+"<br>";

			resultContent += "<table class='table'><thead><tr><th>Numbers that match draw</th><th>Count</th></tr></thead><tbody>";
			for (var i=0, ln=statistics.stats.length; i<ln; i++) {
				let nbStat = statistics.stats[i];
				let cssClass = (nbStat.count > 0) ? 'positive' : '';
				resultContent += "<tr class='"+cssClass+"'><td class='nb-found'>"+nbStat.nbFound+"</td><td class='count'>"+nbStat.count+"</td></tr>"
			}
			resultContent += "</tbody></table>";

			$resultContainer.html(resultContent);
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
