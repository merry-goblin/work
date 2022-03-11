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
		'getARandomGrid' => array(
			'path'      => 'api/player/grid/random/{nb}',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.getARandomGridAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
		'postGrids' => array(
			'path'      => 'api/player/grids',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.postGridsAction',
			'methods'   => 'POST',
			'roles'     => 'anonymous',
		),
	),
);

return $routing;
