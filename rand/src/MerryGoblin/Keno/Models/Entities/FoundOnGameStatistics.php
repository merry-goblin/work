<?php

namespace MerryGoblin\Keno\Models\Entities;

use Monolith\Casterlith\Casterlith;
use Monolith\Casterlith\Entity\EntityInterface;

class FoundOnGameStatistics implements EntityInterface
{
	public $id = null;
	public $gameStatisticsId = null;
	public $number = null;
	public $count = null;

	public $gameStatistics = Casterlith::NOT_LOADED;
}
