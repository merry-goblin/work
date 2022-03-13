<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Grid as GridEntity;
use MerryGoblin\Keno\Models\Entities\Game as GameEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class Grid extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\Grid';

	public function insertGrid(GameEntity $game, $selectedCells)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			INSERT INTO grid
				(`id`, `cells`, `gameId`)
			VALUES 
				(:id , :cells , :gameId )
		";
		$values = array(
			'id'     => null,
			'cells'  => $selectedCells,
			'gameId' => $game->id,
		);
		$dbal->executeUpdate($sql, $values);
	}
}
