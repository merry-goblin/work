<?php 

namespace MerryGoblin\Keno\Exceptions;

class DrawNotInProgressException extends \Exception implements PublicExceptionInterface
{
	protected $message = "Draw not in progress. Draw can't be processed";
	protected $code = 1002;

	/**
	 * @return boolean
	 */
	public function isPublic()
	{
		return true;
	}
}
