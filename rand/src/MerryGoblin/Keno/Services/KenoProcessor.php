<?php

namespace MerryGoblin\Keno\Services;

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
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	protected function updateGridComparisonToStatistics(GameEntity $game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameComposerStatistics = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');

		//	Prepare statistics for this game
		$gameComposerStatistics->addGameToStatistics($game);

		return null;
	}

}
