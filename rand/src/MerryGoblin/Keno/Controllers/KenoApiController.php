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
		$gameComposer  = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');

		$currentGame = $gameComposer->getCurrentGame();

		var_dump($currentGame);

		exit();

		$dbal = $orm->getDBALConnection();

		/*foreach ($grids as $grid) {
			$sql = "
				INSERT INTO participation
					(`id`, `cells`, `game_id`)
				VALUES 
					(:id,  :cells)
			";
			$values = array(
				'id'    => null,
				'cells' => json_encode($grid),
			);
			$dbal->executeUpdate($sql, $values);
		}*/

		$response = $grids;

		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}
}
