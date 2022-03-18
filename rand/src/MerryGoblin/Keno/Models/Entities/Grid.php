<?php

namespace MerryGoblin\Keno\Models\Entities;

use Monolith\Casterlith\Casterlith;
use Monolith\Casterlith\Entity\EntityInterface;

class Grid implements EntityInterface
{
	public $id = null;
	public $cells = null;
	public $gameId = null;

	public $game  = Casterlith::NOT_LOADED;
}
