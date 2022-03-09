<?php 

namespace Monolith\Routerlith;

class Utils
{
	/**
	 * @param  string|array $param
	 * @return array
	 */
	public static function forceParamAsAnArray($param)
	{
		if (is_string($param)) {
			$params = explode(",", $param);
		}
		foreach ($params as $key => $param) {
			$params[$key] = trim($param);
		}

		return $params;
	}

	/**
	 * @return string
	 */
	public static function getRequestUrl()
	{
		$requestUrl = $_SERVER['REQUEST_URI'];

        // strip GET variables from URL
        if (($pos = strpos($requestUrl, '?')) !== false) {
            $requestUrl = substr($requestUrl, 0, $pos);
        }

        return $requestUrl;
	}

	/**
	 * To use other methods than GET or POST we post _method parameter
	 * @return string
	 */
	public static function getRequestMethod()
	{
		$requestMethod = (
            isset($_POST['_method'])
            && ($_method = strtoupper($_POST['_method']))
            && in_array($_method, array('PUT', 'PATCH', 'DELETE', 'REMOVE'))
        ) ? $_method : $_SERVER['REQUEST_METHOD'];

		return $requestMethod;
	}

	/**
	 * Like array_shift but with no re-index
	 * @param  array $array [description]
	 * @return mixed [value of removed index]
	 */
	public static function arrayShift(&$array)
	{
		reset($array);
		$firstIndex  = key($array);
		$value       = $array[$firstIndex];
		unset($array[$firstIndex]);

		return $value;
	}
}