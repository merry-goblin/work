<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;
use MerryGoblin\Keno\Models\Entities\GameStatistics as GameStatisticsEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class GameStatistics extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\GameStatistics';

	public function addGameToStatistics(GameEntity $game)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			INSERT INTO game_statistics
				(`id`, `gameId`, `nbGrids`)
			VALUES 
				(:id , :gameId , :nbGrids )
		";
		$values = array(
			'id'      => null,
			'gameId'  => $game->id,
			'nbGrids' => 0,
		);
		$dbal->executeUpdate($sql, $values);
	}

	public function incrementGridNumber(GameEntity $game, $increment)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE game_statistics
			SET nbGrids = nbGrids + :increment
			WHERE gameId = :gameId
		";
		$values = array(
			'increment' => $increment,
			'gameId'    => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}
}
