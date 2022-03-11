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
		$grids = json_decode(file_get_contents('php://input'), true);

		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$dbal = $orm->getDBALConnection();

		$sql = "
			INSERT INTO game
				(`id`, `cells`)
			VALUES 
				(:id,  :cells)
		";
		$values = array(
			'id'    => null,
			'cells' => null,
		);
		$dbal->executeUpdate($sql, $values);

		$response = $grids;

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}
}
