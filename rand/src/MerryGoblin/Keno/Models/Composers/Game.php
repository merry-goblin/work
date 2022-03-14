<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Game extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Game';

	public CONST BET_ALLOWED_STATUS = 1;
	public CONST DRAW_STATUS        = 2;
	public CONST FINISHED_STATUS    = 3;

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
}
