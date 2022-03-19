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
		'postGameDraw' => array(
			'path'      => 'api/game/draw',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.postGameDrawAction',
			'methods'   => 'POST',
			'roles'     => 'anonymous',
		),
		//	Process can be called by the FRONT ...
		'postGameDrawProcess' => array(
			'path'      => 'api/game/draw/process',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.postGameDrawProcessAction',
			'methods'   => 'GET,POST',
			'roles'     => 'anonymous',
		),
		//	... or called by a crontab by the BACK
		'postGameDrawProcessByCron' => array(
			'path'      => null,
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.postGameDrawProcessAction',
			'methods'   => 'GET,POST',
			'roles'     => 'anonymous',
		),
		//	Get game result after process is finished
		'getGameResult' => array(
			'path'      => 'api/game/{id}/result',
			'action'    => 'MerryGoblin\Keno\Controllers\KenoApiController.getGameResultAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
	),
);

return $routing;
