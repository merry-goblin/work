<?php

$routing = array(
	'base_path' => '/',
	'routes'    => array(
		'home'      => array(
			'path'      => '',
			'action'    => 'MerryGoblin\Keno\Controllers\SampleController.getAction',
			'methods'   => 'GET',
			'roles'     => 'anonymous',
		),
	),
);

return $routing;
