<?php 

namespace MerryGoblin\Keno\Exceptions;

class DrawInProgressException extends \Exception implements PublicExceptionInterface
{
	protected $message = "Draw in progress. No bet allowed";
	protected $code = 1001;

	/**
	 * @return boolean
	 */
	public function isPublic()
	{
		return true;
	}
}
