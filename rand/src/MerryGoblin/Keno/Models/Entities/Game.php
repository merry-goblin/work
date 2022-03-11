<?php

namespace MerryGoblin\Keno\Models\Entities;

use Monolith\Casterlith\Casterlith;
use Monolith\Casterlith\Entity\EntityInterface;

class Game implements EntityInterface
{
	public $id = null;
	public $cells = null;
}
