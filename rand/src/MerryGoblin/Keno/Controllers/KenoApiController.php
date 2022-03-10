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
}
