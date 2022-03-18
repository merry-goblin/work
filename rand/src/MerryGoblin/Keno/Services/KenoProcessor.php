<?php

namespace MerryGoblin\Keno\Services;

//	Model composers
use MerryGoblin\Keno\Models\Composers\GameStatistics as GameStatisticsComposer;
use MerryGoblin\Keno\Models\Composers\FoundOnGameStatistics as FoundOnGameStatisticsComposer;

//	Model entities
use MerryGoblin\Keno\Models\Entities\Grid as GridEntity;

class KenoProcessor
{
	protected $casterlithService = null;

	protected $numberOfGridToHandleByLot = 100;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return [type]       [description]
	 */
	public function process($game)
	{
		$nbProcessed = 0;

		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		//	Selected game cells
		$gameCells = json_decode($game->cells, true);

		$grids = $gridComposer->getGridsToProcess($game, $this->numberOfGridToHandleByLot);
		foreach ($grids as $grid) {
			$gridCells = json_decode($grid->cells, true);
			$intersect = array_intersect($gameCells, $gridCells);

			//	Update grid
			$grid->status  = $gridComposer::GRID_PROCESSED_STATUS;
			$grid->nbFound = count($intersect);
			$gridComposer->updateAfterDrawProcess($grid);

			//	Statistics
			$this->updateStatisticsOfGridComparison($grid);

			$nbProcessed++;
		}

		return $nbProcessed;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	public function verifyProcessStatus($game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		$nb = $gridComposer->getNumberOfGridsToProcess($game);

		if ($nb == 0) {
			$game->active = false;
			$game->status = $gameComposer::FINISHED_STATUS;
			$gameComposer->finishDraw($game);
		}

		return null;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Grid $grid
	 * @return null
	 */
	protected function updateStatisticsOfGridComparison(GridEntity $grid)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');
		$foundOnGameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\FoundOnGameStatistics');

		//	Get game statistics of the active game
		$currentGameStatistics = $gameStatisticsComposer->getCurrentGameStatistics();

		//	Increment by one a row
		$foundOnGameStatisticsComposer->incrementNumberFoundByOne($currentGameStatistics, $grid->nbFound);

		return null;
	}
}
