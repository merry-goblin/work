<?php

namespace MerryGoblin\Keno\Models\Mappers;

use Monolith\Casterlith\Entity\EntityInterface;
use Monolith\Casterlith\Mapper\AbstractMapper;
use Monolith\Casterlith\Mapper\MapperInterface;
use Monolith\Casterlith\Relations\OneToMany;
use Monolith\Casterlith\Relations\ManyToOne;

class Game extends AbstractMapper implements MapperInterface
{
	protected static $table      = 'game';
	protected static $entity     = 'MerryGoblin\Keno\Entities\Game';
	protected static $fields     = array(
		'id'    => array('type' => 'integer', 'primary' => true, 'autoincrement' => true),
		'cells' => array('type' => 'string'),
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
				
			);
		}

		return self::$relations;
	}
}
