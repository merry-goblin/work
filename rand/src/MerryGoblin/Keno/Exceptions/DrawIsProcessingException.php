<?php 

namespace MerryGoblin\Keno\Exceptions;

class DrawIsProcessingException extends \Exception implements PublicExceptionInterface
{
	protected $message = "Draw is processing. Another process can't be started yet";
	protected $code = 1003;

	/**
	 * @return boolean
	 */
	public function isPublic()
	{
		return true;
	}
}
