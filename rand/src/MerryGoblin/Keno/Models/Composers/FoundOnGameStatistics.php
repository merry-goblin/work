<?php

namespace MerryGoblin\Keno\Models\Composers;

use MerryGoblin\Keno\Models\Entities\Game as GameEntity;
use MerryGoblin\Keno\Models\Entities\GameStatistics as GameStatisticsEntity;

use Monolith\Casterlith\Composer\ComposerInterface;
use Monolith\Casterlith\Composer\AbstractComposer;

class FoundOnGameStatistics extends AbstractComposer implements ComposerInterface
{
	protected static $mapperName  = 'MerryGoblin\\Keno\\Models\\Mappers\\FoundOnGameStatistics';

	public function prerateRowsForAGameStatistics(GameStatisticsEntity $gameStatistics)
	{
		$dbal = $this->getDBALConnection();

		for ($i=0; $i<=10; $i++) {
			$sql = "
				INSERT INTO found_on_game_statistics
					(`id`, `gameStatisticsId`, `number`, `count`)
				VALUES 
					(:id , :gameStatisticsId , :number , :count )
			";
			$values = array(
				'id'                => null,
				'gameStatisticsId'  => $gameStatistics->id,
				'number'            => $i,
				'count'             => 0,
			);
			$dbal->executeUpdate($sql, $values);
		}
	}

	public function incrementNumberFoundByOne(GameStatisticsEntity $gameStatistics, $number)
	{
		$dbal = $this->getDBALConnection();

		$sql = "
			UPDATE found_on_game_statistics
			SET count = count + 1
			WHERE gameStatisticsId = :gameStatisticsId
			  AND number = :number
		";
		$values = array(
			'gameStatisticsId' => $gameStatistics->id,
			'number'           => $number,
		);
		$dbal->executeUpdate($sql, $values);
	}
}
