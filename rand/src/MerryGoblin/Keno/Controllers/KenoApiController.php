<?php 

namespace MerryGoblin\Keno\Controllers;

//	Services
use MerryGoblin\Keno\Services\Randomizer;

//	Exceptions
use MerryGoblin\Keno\Exceptions\DrawInProgressException;
use MerryGoblin\Keno\Exceptions\DrawNotInProgressException;
use MerryGoblin\Keno\Exceptions\DrawIsProcessingException;
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
			if ($currentGame->status != $gameComposer::BETS_ARE_ALLOWED_STATUS) {
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
		try {
			//	ORM
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');

			//	Active game
			$currentGame = $gameComposer->getCurrentGameOrInsertItNeeded();
			if ($currentGame->status != $gameComposer::BETS_ARE_ALLOWED_STATUS) {
				throw new DrawInProgressException();
			}

			//	Change game status to :
			//	 - prevent any more bets
			//	 - to process the draw with a cron
			$status = $gameComposer::DRAW_PENDING_STATUS;
			$gameComposer->changeGameStatus($currentGame, $status);

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

	public function postGameDrawProcessAction()
	{
		try {
			//	ORM
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');

			//	Active game
			$currentGame = $gameComposer->getCurrentGameOrInsertItNeeded();
			if ($currentGame->status == $gameComposer::DRAW_PROCESSING_STATUS) {
				throw new DrawIsProcessingException();
			}
			if ($currentGame->status != $gameComposer::DRAW_PENDING_STATUS) {
				throw new DrawNotInProgressException();
			}

			//	Change game status to processing
			$status = $gameComposer::DRAW_PROCESSING_STATUS;
			$gameComposer->changeGameStatus($currentGame, $status);

			//	Processing
			//	todo

			$processStatus = 'pending'; // 'finished'

			//	Change game status to pending
			$status = $gameComposer::DRAW_PENDING_STATUS;
			$gameComposer->changeGameStatus($currentGame, $status);

			//	Response: success
			$response = [
				'code'    => 0,
				'message' => "Success",
				'data'    => [
					'process' => $processStatus,
				],
			];
			return $this->handleAPISuccess($response);
		}
		catch (\Exception $e) {
			//	Response: error
			return $this->handleAPIException($e);
		}
	}
}
