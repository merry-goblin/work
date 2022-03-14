<?php 

namespace MerryGoblin\Keno\Controllers;

use MerryGoblin\Keno\Services\Randomizer;

use MerryGoblin\Keno\Exceptions\PublicExceptionInterface;

abstract class AbstractController
{
	protected $casterlithService = null;

	public function __construct($casterlithService)
	{
		$this->casterlithService = $casterlithService;
	}

	/**
	 * @param  array   $response
	 * @return string
	 */
	protected function handleAPISuccess($response)
	{
		header("HTTP/1.1 200 OK");
		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}

	/**
	 * @param  Exception $e
	 * @return string
	 */
	protected function handleAPIException($e)
	{
		error_log($e);

		if ($e instanceof PublicExceptionInterface && $e->isPublic()) {
			$errorCode    = $e->getCode();
			$errorMessage = $e->getMessage();
			$httpCode     = "403 Forbidden";
		}
		else {
			$errorCode    = 9999;
			$errorMessage = "An unexpected error occured";
			$httpCode     = "500 Bad Gateway";
		}
		$response = [
			'code'    => $errorCode,
			'message' => $errorMessage,
		];
		header("HTTP/1.1 ".$httpCode);
		header('Content-Type: application/json; charset=utf-8');
		return json_encode($response);
	}
}
