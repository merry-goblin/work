<?php

namespace MerryGoblin\Keno\Services\Keno;

class KenoProcessor
{
	protected $casterlithService = null;

	protected $numberOfGridToHandleByLot = 100;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}

	public function process($game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		$grids = $gridComposer->getGridsToProcess($game, $max);
		foreach ($grids as $grid) {

		}

		return 0;
	}

	public function verifyProcessStatus($game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		$nb = $gridComposer->getNumberOfGridsToProcess($game);

		return $nb;
	}
}
