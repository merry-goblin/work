<?php

$routing = array(
	'base_path' => '/',
	'routes'    => array(
		//	Main app
		'app' => array(
			'path'      => '',
			'action'    => 'MerryGoblin\Keno\Controllers\AppController.getAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
		//	Keno API
		'test' => array(
			'path'      => 'api/test',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.testAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
		//	Keno API
		'getARandomGrid' => array(
			'path'      => 'api/player/getARandomGrid/{nb}',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.getARandomGridAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
	),
);

return $routing;
