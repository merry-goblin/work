<?php

namespace MerryGoblin\Keno\Services;

class KenoProcessor
{
	protected $casterlithService = null;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}

	
}
