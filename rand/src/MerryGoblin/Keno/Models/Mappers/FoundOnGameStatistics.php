<?php

namespace MerryGoblin\Keno\Models\Mappers;

use Monolith\Casterlith\Entity\EntityInterface;
use Monolith\Casterlith\Mapper\AbstractMapper;
use Monolith\Casterlith\Mapper\MapperInterface;
use Monolith\Casterlith\Relations\OneToMany;
use Monolith\Casterlith\Relations\ManyToOne;

use MerryGoblin\Keno\Models\Mappers\GameStatistics as GameStatisticsMapper;

class FoundOnGameStatistics extends AbstractMapper implements MapperInterface
{
	protected static $table      = 'found_on_game_statistics';
	protected static $entity     = 'MerryGoblin\Keno\Models\Entities\FoundOnGameStatistics';
	protected static $fields     = array(
		'id'                => array('type' => 'integer', 'primary' => true, 'autoincrement' => true),
		'gameStatisticsId'  => array('type' => 'integer'),
		'number'            => array('type' => 'integer'),
		'count'             => array('type' => 'integer'),
	);
	protected static $relations   = null;

	public static function getPrimaryKey()
	{
		return 'id';
	}

	public static function getRelations()
	{
		if (is_null(self::$relations)) {
			self::$relations = array(
				'gameStatistics' => new ManyToOne(new GameStatistics(), 'foundOnGameStatistics', 'gameStatistics', '`foundOnGameStatistics`.gameStatisticsId = `gameStatistics`.id', null),
			);
		}

		return self::$relations;
	}
}
