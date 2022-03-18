<?php

namespace MerryGoblin\Keno\Models\Mappers;

use Monolith\Casterlith\Entity\EntityInterface;
use Monolith\Casterlith\Mapper\AbstractMapper;
use Monolith\Casterlith\Mapper\MapperInterface;
use Monolith\Casterlith\Relations\OneToMany;
use Monolith\Casterlith\Relations\ManyToOne;

use MerryGoblin\Keno\Models\Mappers\Game as GameMapper;

class Grid extends AbstractMapper implements MapperInterface
{
	protected static $table      = 'grid';
	protected static $entity     = 'MerryGoblin\Keno\Models\Entities\Grid';
	protected static $fields     = array(
		'id'    => array('type' => 'integer', 'primary' => true, 'autoincrement' => true),
		'cells' => array('type' => 'string'),
		'gameId' => array('type' => 'integer'),
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
				'game' => new ManyToOne(new GameMapper(), 'grid', 'game', '`grid`.gameId = `game`.id', null),
			);
		}

		return self::$relations;
	}
}
