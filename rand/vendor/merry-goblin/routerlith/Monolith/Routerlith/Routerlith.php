<?php 

namespace Monolith\Routerlith;

use Monolith\Routerlith\RoutingBuilder;
use Monolith\Routerlith\RouteModel;
use Monolith\Routerlith\Route;
use Monolith\Routerlith\Utils;

class Routerlith
{
	protected $routes;

	/**
	 * @param array $routing
	 */
	public function __construct(array $routing = null)
	{
		$this->modelList = array();
		if (!is_null($routing)) {
			$this->addRouteModels($routing);
		}
	}

	/**
	 * @param  array $routing
	 * @return null
	 */
	public function addRouteModels(array $routing)
	{
		$modelList = RoutingBuilder::buildRouting($routing);

		$this->modelList = array_merge($this->modelList, $modelList);
	}

	/**
	 * @return Monolith\Routerlith\Route | null
	 */
	public function getCurrentRoute()
	{
		$requestUrl    = Utils::getRequestUrl();
		$requestMethod = Utils::getRequestMethod();

		return $this->getRoute($requestUrl, $requestMethod);
	}

	/**
	 * @param  string $requestUrl
	 * @param  string $requestMethod
	 * @return Monolith\Routerlith\Route | null
	 */
	protected function getRoute($requestUrl, $requestMethod = 'GET')
	{
		$route = null;

		foreach ($this->modelList as $modelName => $model) {

			//	Compare server request method with model's allowed http methods
			if (!in_array($requestMethod, $model->getMethods())) {
				continue;
			}

			$currentDir = dirname($_SERVER['SCRIPT_NAME']);
			if ($currentDir != '/') {
			    $requestUrl = str_replace($currentDir, '', $requestUrl);
			}

			$parameters = array();
			$matches = array();
			if (preg_match_all($model->getRegex(), $requestUrl, $matches)) {

				unset($matches[0]);
				if (count($matches) !== $model->getParameterNumber()) {
					continue;
				}

				foreach ($matches as $match) {
					$parameters[] = $match[0];
				}

				$route = new Route($model, $parameters);
				break;
			}
		}

		return $route;
	}

	/**
	 * @param  string  $routeName
	 * @param  array   $parameters [array of index]
	 * @return \PHPRouter\Route | null
	 */
	public function getRouteByName($routeName, array $parameters = array())
	{
		$route = null;

		if (isset($this->modelList[$routeName])) {
			$model = $this->modelList[$routeName];
			if ($model->getParameterNumber() != count($parameters)) {
				throw new \Exception("nb parameters doesn't match the excepected number of parameters (method : getRouteByName)");
			}
			$route = new Route($model, $parameters);
		}
		else {
			throw new \Exception("route name doesn't exist (method : getRouteByName)");
		}

		return $route;
	}

	/**
	 * @param  Monolith\Routerlith\Route  $route
	 * @return string
	 */
	public function generate(Route $route)
	{
		$model            = $route->getModel();
		$parameterValues  = $route->getParameters();
		$modelPath        = $model->getPath();
		$parameterKeys    = $model->getParameterKeys();

		$relativePath = $modelPath;
		foreach ($parameterKeys as $key) {
			$relativePath = preg_replace_callback("#{".$key."}#", function($matches) use (&$parameterValues) {
				$value = Utils::arrayShift($parameterValues);
				return $value;
			}, $relativePath);
		}

		return $relativePath;
	}

	/**
	 * @param  Monolith\Routerlith\Route $route
	 * @return mixed
	 */
	public function dispatch($route, array $dependencies = null)
	{
		if (is_null($route)) {
			throw new \Exception("route parameter is null (method : dispatch)");
		}

		//	Action to call
		$model = $route->getModel();
		$tab = explode('.', $model->getAction());
		list($className, $methodName) = explode('.', $model->getAction());

		//	Controller
		$reflection = new \ReflectionClass($className); 
		$controller = $reflection->newInstanceArgs($dependencies);

		//	If controller needs the route as dependency
		if (method_exists($controller, "loadRouteAsDependency")) {
			$controller->loadRouteAsDependency($route);
		}

		return call_user_func_array(array($controller, $methodName), $route->getParameters());
	}
}