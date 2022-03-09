<?php 

namespace Monolith\Routerlith;

class RouteModel
{
	CONST availableMethods = array('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'REMOVE');

	protected $path             = null;
	protected $action           = null;
	protected $methods          = null;
	protected $roles            = null;
	protected $filters          = null;
	protected $extra            = null;
	protected $regex            = null;
	protected $parameterKeys    = null;
	protected $parameterNumber  = null;

	public function __construct($path, $action, $methods, $roles, $filters, $extra)
	{
		$this->path      = $path;
		$this->action    = $action;
		$this->methods   = $methods;
		$this->roles     = $roles;
		$this->filters   = $filters;
		$this->extra     = $extra;
	}

	public function getPath()
	{
		return $this->path;
	}

	public function getAction()
	{
		return $this->action;
	}

	public function getMethods()
	{
		return $this->methods;
	}

	public function getRoles()
	{
		return $this->roles;
	}

	public function getFilters()
	{
		return $this->filters;
	}

	public function getExtra()
	{
		return $this->extra;
	}

	public function getRegex()
	{
		if (is_null($this->regex)) {
			$this->parameterKeys    = array();

			$this->regex = preg_replace_callback("#{([\w-%]+)}#", array($this, "replaceParamaterKeyByRegex"), $this->path, -1, $this->parameterNumber);
			$this->regex = "#^".$this->regex."$#";
		}

		return $this->regex;
	}

	/**
	 * This method does two things :
	 * - List every parameters keys present in this model route
	 * - Apply a custom filter instead of the generic regex
	 * 
	 * @param  array $matches
	 * @return string
	 */
	public function replaceParamaterKeyByRegex($matches)
	{
		$key = $matches[1];
		$this->parameterKeys[] = $key;

		if (isset($this->filters[$key])) {
			$replacer = $this->filters[$key];
		}
		else  {
			$replacer = "([\w-%]+)";
		}

		return $replacer;
	}

	public function getParameterKeys()
	{
		if (is_null($this->parameterKeys)) {
			if (is_null($this->regex)) {
				$this->getRegex();
			}
		}

		return $this->parameterKeys;
	}

	public function getParameterNumber()
	{
		if (is_null($this->parameterNumber)) {
			if (is_null($this->regex)) {
				$this->getRegex();
			}
		}

		return $this->parameterNumber;
	}
}
