<?php 

namespace MerryGoblin\Keno\Controllers;

//	Services
use MerryGoblin\Keno\Services\Randomizer;
use MerryGoblin\Keno\Services\Timer;
use MerryGoblin\Keno\Services\KenoProcessor;

//	Model composers
use MerryGoblin\Keno\Models\Composers\Game as GameComposer;

//	Model entities
use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

//	Exceptions
use MerryGoblin\Keno\Exceptions\DrawInProgressException;
use MerryGoblin\Keno\Exceptions\DrawNotInProgressException;
use MerryGoblin\Keno\Exceptions\DrawIsProcessingException;
use MerryGoblin\Keno\Exceptions\PublicExceptionInterface;

class KenoApiController extends AbstractController
{
	public function getARandomGridAction($nb)
	{
		//	Services
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

			//	Services
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');
			$gridComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Grid');

			//	Get the active game
			$currentGame = $this->getCurrentGameOrInsertIfNeeded($gameComposer);
			if ($currentGame->status != $gameComposer::BETS_ARE_ALLOWED_STATUS) {
				throw new DrawInProgressException();
			}

			//	Insert all grids
			foreach ($input['grids'] as $grid) {
				$gridComposer->insertGrid($currentGame, json_encode($grid));
			}
			$this->updateStatisticsOfNbGridSent($currentGame, count($input['grids']));

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
			//	Services
			$randomizerService = new Randomizer();
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');

			//	Get the active game
			$currentGame = $this->getCurrentGameOrInsertIfNeeded($gameComposer);
			if ($currentGame->status != $gameComposer::BETS_ARE_ALLOWED_STATUS) {
				throw new DrawInProgressException();
			}

			//	Draw 20 numbers out of 70
			$randomList = $randomizerService->getRandomIntegerList(20, 1, 70, false, true);
			$currentGame->cells = json_encode($randomList);
			$gameComposer->changeCells($currentGame);

			//	Change game status to :
			//	 - prevent any more bets
			//	 - to process the draw with a cron
			$currentGame->status = $gameComposer::DRAW_PENDING_STATUS;
			$gameComposer->changeStatus($currentGame);

			//	Response: success
			$response = [
				'code'    => 0,
				'message' => "Success",
				'data'    => [
					'gameId' => $currentGame->id,
				],
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
			$timer = new Timer(); // Will help to stop the process before we reach the max execution time

			//	ORM
			$orm = $this->casterlithService->getConnection('keno');
			$gameComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\Game');

			//	Get the active game
			$currentGame = $this->getCurrentGameOrInsertIfNeeded($gameComposer);
			if ($currentGame->status == $gameComposer::DRAW_PROCESSING_STATUS) {
				throw new DrawIsProcessingException();
			}
			if ($currentGame->status != $gameComposer::DRAW_PENDING_STATUS) {
				throw new DrawNotInProgressException();
			}

			//	Change game status to processing
			$currentGame->status = $gameComposer::DRAW_PROCESSING_STATUS;
			$gameComposer->changeStatus($currentGame);

			//	Processing
			$kenoProcessor = new KenoProcessor($this->casterlithService);
			$kenoProcessor->verifyProcessStatus($currentGame);
			
			if ($currentGame->status == $gameComposer::DRAW_PROCESSING_STATUS) {
				while (true) {
					$nbProcessed = $kenoProcessor->process($currentGame);
					if ($nbProcessed == 0) {
						break;
					}
					if ($timer->getFullTime() > 20) {
						break;
					}
				}

				$processStatus = 'pending';

				//	Change game status to pending
				$currentGame->status = $gameComposer::DRAW_PENDING_STATUS;
				$gameComposer->changeStatus($currentGame);
			}
			else {
				$processStatus = 'finished';
			}

			//	Response: success
			$response = [
				'code'    => 0,
				'message' => "Success",
				'data'    => [
					'gameId'  => $currentGame->id,
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

	/**
	 * @param  integer $id
	 * @return string
	 */
	public function getGameResultAction($id)
	{
		try {
			
			//	ORM
			$orm = $this->casterlithService->getConnection('keno');
			$gameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');

			$gameStatistics = $gameStatisticsComposer->getGameStatisticsByGameId($id);

			//	Response: success
			$response = [
				'code'    => 0,
				'message' => "Success",
				'data'    => [
					'gameId'        => $id,
					'nbPlayedGrids' => $gameStatistics->nbGrids,
				],
			];
			return $this->handleAPISuccess($response);
		}
		catch (\Exception $e) {
			//	Response: error
			return $this->handleAPIException($e);
		}
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Composers\Game $gameComposer
	 * @return MerryGoblin\Keno\Models\Entities\Game
	 */
	protected function getCurrentGameOrInsertIfNeeded(GameComposer $gameComposer)
	{
		//	Select
		$currentGame = $gameComposer->getCurrentGame();
		if (is_null($currentGame)) {
			//	Insert
			$currentGame = $gameComposer->insertANewGame();
			//	Statistics
			$this->addGameToStatistics($currentGame);
		}

		return $currentGame;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	protected function addGameToStatistics(GameEntity $game)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');
		$foundOnGameStatisticsComposer = $orm->getComposer('MerryGoblin\Keno\Models\Composers\FoundOnGameStatistics');

		//	Prepare statistics for this game
		$gameStatisticsComposer->addGameToStatistics($game);
		$gameStatistics = $gameStatisticsComposer->getCurrentGameStatistics();
		$foundOnGameStatisticsComposer->prerateRowsForAGameStatistics($gameStatistics);

		return null;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @param  integer $increment
	 * @return null
	 */
	protected function updateStatisticsOfNbGridSent($game, $increment)
	{
		//	ORM
		$orm = $this->casterlithService->getConnection('keno');
		$gameComposerStatistics = $orm->getComposer('MerryGoblin\Keno\Models\Composers\GameStatistics');

		//	Prepare statistics for this game
		$gameComposerStatistics->incrementGridNumber($game, $increment);

		return null;
	}
}
