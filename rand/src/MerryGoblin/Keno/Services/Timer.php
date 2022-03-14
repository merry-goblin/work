<?php 

namespace MerryGoblin\Keno\Services;

class Timer
{
	protected $start = null;
	protected $currentTime = null;

	public function __construct()
	{
		$this->start = new \DateTime('now');
		$this->currentTime = new \DateTime('now');
	}

	/**
	 * currentTime will be re-initialized
	 * @return integer
	 */
	public function getTime()
	{
		$now = new \DateTime('now');
		$elapsedSeconds = $now->getTimestamp() - $this->currentTime->getTimestamp();
		$this->currentTime = $now;

		return $elapsedSeconds;
	}

	/**
	 * currentTime won't be re-initialized
	 * @return [type] [description]
	 */
	public function getFullTime()
	{
		$now = new \DateTime('now');
		$elapsedSeconds = $now->getTimestamp() - $this->start->getTimestamp();

		return $elapsedSeconds;
	}
}
