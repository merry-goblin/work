<?php 

namespace MerryGoblin\Keno\Controllers;

use MerryGoblin\Keno\Services\Randomizer;

class KenoApiController extends AbstractController
{
	public function getARandomGridAction($nb)
	{
		$randomizerService = new Randomizer();

		$randomList = $randomizerService->getRandomIntegerList($nb, 1, 70, false, true);

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($randomList);
	}

	public function postGridsAction()
	{
		//	Input paramaters
		$input = json_decode(file_get_contents('php://input'), true);

		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		//	Active game
		$currentGame = $gameComposer->getCurrentGameOrInsertItNeeded();

		//	Insert all grids
		foreach ($input['grids'] as $grid) {

			$gridComposer->insertGrid($currentGame, json_encode($grid));
		}

		$response = 'success';

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}
}
