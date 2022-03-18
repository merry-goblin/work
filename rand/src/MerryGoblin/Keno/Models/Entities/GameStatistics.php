<?php

namespace MerryGoblin\Keno\Models\Entities;

use Monolith\Casterlith\Casterlith;
use Monolith\Casterlith\Entity\EntityInterface;

class GameStatistics implements EntityInterface
{
	public $id = null;
	public $gameId = null;
	public $nbGrids = null;

	public $game = Casterlith::NOT_LOADED;
}
