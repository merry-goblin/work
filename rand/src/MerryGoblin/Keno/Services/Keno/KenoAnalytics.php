<?php

namespace MerryGoblin\Keno\Services\Keno;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

class KenoAnalytics
{
	protected $casterlithService = null;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}

	public function addGameToStatistics(GameEntity $game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');

		$gameStatisticsComposer->addGameToStatistics($game);
	}	
}
