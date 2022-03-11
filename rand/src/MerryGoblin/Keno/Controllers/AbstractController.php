<?php 

namespace MerryGoblin\Keno\Controllers;

use MerryGoblin\Keno\Services\Randomizer;

abstract class AbstractController
{
	protected $casterlithService = null;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}
}
