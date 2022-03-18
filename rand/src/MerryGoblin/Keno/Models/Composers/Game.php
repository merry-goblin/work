<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Game extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Game';

	CONST BETS_ARE_ALLOWED_STATUS = 1; // Game is open to bets.
	CONST DRAW_PENDING_STATUS     = 2; // Draw is pending. No process ongoing. Can be processed.
	CONST DRAW_PROCESSING_STATUS  = 3; // A process is happening we can't start another process yet.
	CONST FINISHED_STATUS         = 4; // Draw is finished.

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

	public function insertANewGame()
	{
		$dbal = $this->getDBALConnection();

		$game = new GameEntity();
		$game->cells  = null;
		$game->active = true;
		$game->status = 1;

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

		$game->id = $dbal->lastInsertId();

		return $game;
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	public function changeStatus($game)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE game
			SET   status = :status
			WHERE id = :id
		";
		$values = array(
			'status' => $game->status,
			'id'     => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	public function changeCells($game)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE game
			SET   cells = :cells
			WHERE id = :id
		";
		$values = array(
			'cells' => $game->cells,
			'id'     => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}

	/**
	 * @param  MerryGoblin\Keno\Models\Entities\Game $game
	 * @return null
	 */
	public function finishDraw($game)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE game
			SET
				status = :status,
				active = :active
			WHERE id = :id
		";
		$values = array(
			'status' => self::FINISHED_STATUS,
			'active' => false,
			'id'     => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}

}
