<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Game extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Game';

	public CONST BETS_ARE_ALLOWED_STATUS = 1; // Game is open to bets.
	public CONST DRAW_PENDING_STATUS     = 2; // Draw is pending. No process ongoing. Can be processed.
	public CONST DRAW_PROCESSING_STATUS  = 3; // A process is happening we can't start another process yet.
	public CONST FINISHED_STATUS         = 4; // Draw is finished.

	public function getCurrentGameOrInsertItNeeded()
	{
		$currentGame = $this->getCurrentGame();
		if (is_null($currentGame)) {
			$this->insertCurrentGame();
			$currentGame = $this->getCurrentGame();
		}

		return $currentGame;
	}

	public function getCurrentGame()
	{
		$currentGame = $this
			->select('game')
			->where($this->expr()->eq('game.active', ':active'))
			->setParameter('active', true)
			->first()
		;

		return $currentGame;
	}

	public function insertCurrentGame()
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			INSERT INTO game
				(`id`, `cells`, `active`, `status`)
			VALUES 
				(:id , :cells , :active , :status )
		";
		$values = array(
			'id'     => null,
			'cells'  => null,
			'active' => true,
			'status' => 1,
		);
		$dbal->executeUpdate($sql, $values);
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @param  integer $status
	 * @return null
	 */
	public function changeGameStatus($game, $status)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE game
			SET   status = :status
			WHERE id = :id
		";
		$values = array(
			'status' => $status,
			'id'     => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}
}
