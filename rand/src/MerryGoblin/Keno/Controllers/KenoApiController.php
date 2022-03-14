<?php 

namespace MerryGoblin\Keno\Controllers;

//	Services
use MerryGoblin\Keno\Services\Randomizer;

//	Exceptions
use MerryGoblin\Keno\Exceptions\DrawInProgressException;
use MerryGoblin\Keno\Exceptions\PublicExceptionInterface;

class KenoApiController extends AbstractController
{
	public function getARandomGridAction($nb)
	{
		$randomizerService = new Randomizer();

		$randomList = $randomizerService->getRandomIntegerList($nb, 1, 70, false, true);

		//	Response: success
		$response = [
			'code'    => 0,
			'message' => "Success",
			'data'    => $randomList
		];
		return $this->handleAPISuccess($response);
	}

	public function postGridsAction()
	{
		try {
			//	Input paramaters
			$input = json_decode(file_get_contents('php://input'), true);

			//	ORM
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');
			$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

			//	Active game
			$currentGame = $gameComposer->getCurrentGameOrInsertItNeeded();
			if ($currentGame->status != $gameComposer::BET_ALLOWED_STATUS) {
				throw new DrawInProgressException();
			}

			//	Insert all grids
			foreach ($input['grids'] as $grid) {
				$gridComposer->insertGrid($currentGame, json_encode($grid));
			}

			//	Response: success
			$response = [
				'code'    => 0,
				'message' => "Success",
			];
			return $this->handleAPISuccess($response);
		}
		catch (\Exception $e) {
			//	Response: error
			return $this->handleAPIException($e);
		}
	}

	public function postGameDrawAction()
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');
		$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

		//	Active game
		$currentGame = $gameComposer->getCurrentGameOrInsertItNeeded();



		//	Response: success
		$response = [
			'code'    => 0,
			'message' => "Success",
		];
		return $this->handleAPISuccess($response);
	}
}
