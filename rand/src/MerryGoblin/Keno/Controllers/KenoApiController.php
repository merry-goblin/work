<?php 

namespace MerryGoblin\Keno\Controllers;

use MerryGoblin\Keno\Services\Randomizer;

class KenoApiController
{
	public function testAction()
	{
		error_log("testAction");
		return "testAction";
	}

	public function getARandomGridAction($nb)
	{
		$randomizerService = new Randomizer();

		$randomList = $randomizerService->getRandomIntegerList($nb, 1, 70, false, true);

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($randomList);
	}

	public function postGridsAction()
	{
		error_log("--------------------");
		$grids = file_get_contents('php://input');
		error_log(print_r($grids, true));
		$grids = json_decode(file_get_contents('php://input'), true);
		error_log(print_r($grids, true));

		$response = $grids;

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}
}
