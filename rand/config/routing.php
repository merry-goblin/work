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
			'methods'   => 'GET,POST',
			'roles'     => 'anonymous',
		),
		'postGameDraw' => array(
			'path'      => 'api/game/draw',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.postGameDrawAction',
			'methods'   => 'GET,POST',
			'roles'     => 'anonymous',
		),
	),
);

return $routing;
