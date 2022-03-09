<?php 

namespace Monolith\Routerlith;

class Route
{
	protected $model;
	protected $parameters; // will be an array, maybe empty, but an array anyway

	public function __construct($model, array $parameters)
	{
		$this->model       = $model;
		$this->parameters  = $parameters;
	}

	public function getModel()
	{
		return $this->model;
	}

	public function getParameters()
	{
		return $this->parameters;
	}
}
