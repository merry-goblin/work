<?php

namespace MerryGoblin\Keno\Services;

class CasterlithService
{
	protected $connections;
	protected $config;

	/**
	 * @param  array $config
	 */
	public function __construct($config)
	{
		$this->connections = array();
		$this->config = $config;
	}

	/**
	 * @param  string $databaseKey
	 * @return Monolith\Casterlith\Casterlith
	 */
	public function getConnection($databaseKey)
	{
		if (!isset($this->connections[$databaseKey])) {
			if (!isset($this->config[$databaseKey])) {
				throw new \Exception("No database configuration found");
			}
			$pdoConfig = $this->config[$databaseKey];
			$this->connections[$databaseKey] = $this->connect($pdoConfig);
		}

		return $this->connections[$databaseKey];
	}

	/**
	 * @param  array[string] $config
	 * @return Monolith\Casterlith\Casterlith
	 */
	public function connect($config)
	{
		try {
			$ormConfiguration = new \Monolith\Casterlith\Configuration();
			$ormConfiguration->setSelectionReplacer("_cl");

			$orm = new \Monolith\Casterlith\Casterlith($config, $ormConfiguration);
		}
		catch(\Exception $e) {
			trigger_error($e->getMessage(), E_USER_ERROR);
		}

		return $orm;
	}
}
