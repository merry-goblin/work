<?php 

namespace Monolith\Routerlith;

use Monolith\Routerlith\RouteModel;
use Monolith\Routerlith\Utils;

class RoutingBuilder
{
	/**
	 * $routing :
	 * - basePath
	 * - routes
	 *   - << routeName >>
	 *     - basePath
	 *     - path
	 *     - action
	 *     - methods
	 *     - roles
	 *
	 * @param  array $routing
	 * @return null
	 */
	public static function buildRouting(array $routing)
	{
		$routeModels = array();

		//	Base path
		$basePath = "";
		if (isset($routing['base_path'])) {
			$basePath = $routing['base_path'];
		}

		//	Routes
		if (isset($routing['routes']) && is_array($routing['routes'])) {
			foreach ($routing['routes'] as $routeName => $routeInfos) {
				if (!isset($routeInfos['base_path'])) {
					$routeInfos['base_path'] = $basePath;
				}
				$routeModels[$routeName] = static::buildRoute($routeInfos);
			}
		}

		return $routeModels;
	}

	/**
	 * @param  array  $routeInfos
	 * @return null
	 */
	protected static function buildRoute(array $routeInfos)
	{
		$path     = static::getPath($routeInfos);
		$action   = static::getAction($routeInfos);
		$methods  = static::getMethods($routeInfos);
		$roles    = static::getRoles($routeInfos);
		$filters  = static::getFilters($routeInfos);
		$extra    = static::getExtra($routeInfos);

		return new RouteModel($path, $action, $methods, $roles, $filters, $extra);
	}

	/**
	 * @param  array  $routeInfos
	 * @return string
	 */
	protected static function getPath(array $routeInfos)
	{
		$path      = (isset($routeInfos['path']))      ? $routeInfos['path']      : '';
		$basePath  = (isset($routeInfos['base_path'])) ? $routeInfos['base_path'] : '';

		return $basePath.$path;
	}

	/**
	 * @param  array  $routeInfos
	 * @return string
	 */
	protected static function getAction(array $routeInfos)
	{
		$action = (isset($routeInfos['action'])) ? $routeInfos['action'] : '';

		return $action;
	}

	/**
	 * @param  array  $routeInfos
	 * @return array
	 */
	protected static function getMethods(array $routeInfos)
	{
		$methods = (isset($routeInfos['methods'])) ? $routeInfos['methods'] : '';
		$methods = Utils::forceParamAsAnArray($methods);

		foreach ($methods as $method) {
			if (!in_array($method, RouteModel::availableMethods)) {
				$method = @iconv('UTF-8', 'ISO-8859-1//IGNORE', $method);
				throw new \Exception("Method ".$method." isn't available");
			}
		}

		return $methods;
	}

	/**
	 * @param  array  $routeInfos
	 * @return array
	 */
	protected static function getRoles(array $routeInfos)
	{
		$roles = (isset($routeInfos['roles'])) ? $routeInfos['roles'] : '';
		$roles = Utils::forceParamAsAnArray($roles);

		return $roles;
	}

	/**
	 * @param  array  $routeInfos
	 * @return array
	 */
	protected static function getFilters(array $routeInfos)
	{
		$filters = (isset($routeInfos['filters'])) ? $routeInfos['filters'] : array();
		$filters = (is_array($filters))            ? $filters               : array($filters);

		return $filters;
	}

	/**
	 * @param  array  $routeInfos
	 * @return string
	 */
	protected static function getExtra(array $routeInfos)
	{
		$extra = (isset($routeInfos['extra'])) ? $routeInfos['extra'] : null;

		return $extra;
	}

}